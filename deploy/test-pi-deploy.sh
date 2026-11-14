#!/usr/bin/env bash
# Tests deploy/deploy-to-pi.sh and deploy/pi-deploy.sh against a stand-in Pi: a python:3.13-trixie
# container (the Pi runs Python 3.13 on Debian trixie) with a pi user, made-up settings and cert,
# and a sudo that allows only killall, as on the real Pi. Deploys what's committed (git archive
# HEAD), like Jenkins, so commit first. Needs Docker; takes several minutes, mostly pip installs.
#
#   deploy/test-pi-deploy.sh
set -uo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
pi="pi-deploy-test-$RANDOM"
work=$(mktemp -d)   # a clone to commit broken versions in
out=$(mktemp)       # every deploy's output, appended, to check nothing secret is ever shown
last=$(mktemp)      # the latest deploy's output
fails=0

docker run -d --name "$pi" python:3.13-trixie sleep infinity >/dev/null || { echo "couldn't start the stand-in Pi"; exit 1; }
trap 'docker rm -f "$pi" >/dev/null 2>&1; rm -rf "$work" "$out" "$last"' EXIT

as_root() { docker exec -i "$pi" bash -c "$1"; }
on_pi() { docker exec -i -u pi -e HOME=/home/pi "$pi" bash -c "$1"; }
check() { # description, then a command that must succeed
    local desc=$1; shift
    if "$@"; then echo "ok    $desc"; else echo "FAIL  $desc"; fails=$((fails + 1)); fi
}
setup() { "$@" >/dev/null 2>&1 || { echo "setup failed: $*"; exit 1; }; }
deploy_from() { # repo dir; deploys its HEAD the way the Jenkinsfile does
    "$1/deploy/deploy-to-pi.sh" docker exec -i -u pi -e HOME=/home/pi "$pi" bash -c > "$last" 2>&1
    local rc=$?
    cat "$last" >> "$out"
    return $rc
}
deploy() { deploy_from "$repo"; }
commit_in_work() { # a shell command run in the clone, then committed
    (cd "$work" && git reset -q --hard origin/HEAD && bash -c "$1" && git commit -qam "test change")
}
app_pid() { on_pi "pgrep -f '[.]/run[.]py'" 2>/dev/null; }
answers_on() { # url; polls, as the app takes a few seconds to start
    for _ in $(seq 1 30); do
        on_pi "curl -fsSk --max-time 5 '$1'" 2>/dev/null | grep -q 'Hi there!' && return 0
        sleep 2
    done
    return 1
}
answers() { answers_on http://127.0.0.1:5001/; }
said() { grep -q "$1" "$last"; }

# The stand-in Pi: killall, pgrep, curl and flock as on Raspberry Pi OS; sudo that runs only killall.
setup as_root 'apt-get update -qq && apt-get install -y -qq psmisc procps curl util-linux openssl'
setup as_root 'useradd -m -s /bin/bash pi'
setup as_root 'printf "%s\n" "#!/bin/sh" "[ \"\$1\" = -n ] && shift" "[ \"\$1\" = killall ] || { echo \"sudo: a password is required\" >&2; exit 1; }" "exec \"\$@\"" > /usr/local/bin/sudo && chmod 755 /usr/local/bin/sudo'
setup on_pi 'mkdir -p ~/certs ~/house-env && echo made-up-cert > ~/certs/server.csr && echo made-up-key > ~/certs/server.key
  printf "%s\n" "export AUTHENTICATION_SECRET=made-up" "export MY_HOUSE_URL=http://127.0.0.1:9" \
    "export PYTHON_SSL_ON=false" "export PYTHON_HOST=127.0.0.1" "export PYTHON_PORT=5001" > ~/house-env/env-vars.sh'
setup git clone -q "$repo" "$work"

# 1. First deploy: nothing running, no old copy.
deploy; rc=$?
check "first deploy succeeds" test "$rc" -eq 0
check "  the app answers" answers
check "  says so" said 'Deployed: the app answers on http://127.0.0.1:5001/'
check "  runs as pi" test "$(on_pi "ps -o user= -p \$(pgrep -f '[.]/run[.]py')" | tr -d ' ')" = pi
check "  real GPIO library installed" on_pi '~/HouseOfPi/env/bin/python -m pip show -q rpi.gpio'
check "  cert, key and settings copied in" on_pi 'cmp -s ~/certs/server.csr ~/HouseOfPi/cert.crt && cmp -s ~/certs/server.key ~/HouseOfPi/key.key && cmp -s ~/house-env/env-vars.sh ~/HouseOfPi/env-vars.sh'
check "  only the app's files copied" on_pi 'cd ~/HouseOfPi && ! test -e test && ! test -e mock_services && ! test -e docs && test -e run.py && test -e wemo.py && test -e app/server/api.py'
check "  no old copy to keep" on_pi '! test -e ~/HouseOfPi.previous'

# 2. Second deploy: replaces the running app and keeps the first copy.
first_pid=$(app_pid)
setup on_pi 'touch ~/HouseOfPi/good-copy'
deploy; rc=$?
check "second deploy succeeds" test "$rc" -eq 0
check "  the old app was stopped" test "$(app_pid)" != "$first_pid"
check "  exactly one app running" test "$(app_pid | wc -l | tr -d ' ')" = 1
check "  the new one answers" answers
check "  the old copy is kept" on_pi 'test -e ~/HouseOfPi.previous/good-copy'
check "  the new copy is fresh" on_pi '! test -e ~/HouseOfPi/good-copy'
setup on_pi 'touch ~/HouseOfPi/good-copy'

# 3. Missing settings, or an empty cert: fails before touching the running app.
running=$(app_pid)
setup on_pi 'mv ~/house-env/env-vars.sh ~/house-env/env-vars.sh.away'
deploy; rc=$?
check "missing settings: fails" test "$rc" -ne 0
check "  names the file" said 'house-env/env-vars.sh is missing or empty'
check "  the running app is untouched" test "$(app_pid)" = "$running"
setup on_pi 'mv ~/house-env/env-vars.sh.away ~/house-env/env-vars.sh && cp ~/certs/server.csr /tmp/csr && : > ~/certs/server.csr'
deploy; rc=$?
check "empty cert: fails" test "$rc" -ne 0
check "  names the file" said 'certs/server.csr is missing or empty'
check "  the running app is untouched" test "$(app_pid)" = "$running"
check "  its copy is untouched" on_pi 'test -e ~/HouseOfPi/good-copy'
setup on_pi 'cp /tmp/csr ~/certs/server.csr'

# 4. The copy step didn't happen (pi-deploy.sh run on its own): fails before touching anything.
on_pi 'cp ~/jenkins-ssh-home/deploy/pi-deploy.sh /tmp/pd.sh && rm -rf ~/jenkins-ssh-home && bash /tmp/pd.sh' > "$last" 2>&1; rc=$?
check "nothing copied: fails" test "$rc" -ne 0
check "  says why" said "copy step didn't run"
check "  the running app is untouched" test "$(app_pid)" = "$running"

# 5. The old app won't stop (sudo refuses): fails, changes nothing.
setup as_root 'cp /usr/local/bin/sudo /tmp/sudo.real && printf "%s\n" "#!/bin/sh" "exit 1" > /usr/local/bin/sudo'
deploy; rc=$?
check "old app won't stop: fails" test "$rc" -ne 0
check "  says why" said 'still running after 10s'
check "  the running app is untouched" test "$(app_pid)" = "$running"
check "  its copy is untouched" on_pi 'test -e ~/HouseOfPi/good-copy'
setup as_root 'cp /tmp/sudo.real /usr/local/bin/sudo'

# 6. Packages fail to install: the good copy is put back and answers.
setup commit_in_work 'printf "%s\n" "#!/bin/sh" "python3 -m venv env" > env-setup/install-server-env'
deploy_from "$work"; rc=$?
check "failed install: fails" test "$rc" -ne 0
check "  says why" said 'Python packages are missing'
check "  puts the good copy back" on_pi 'test -e ~/HouseOfPi/good-copy'
check "  which answers" answers
check "  and says so" said 'previous copy is running again and answers'
check "  keeps the failed copy" on_pi 'test -d ~/HouseOfPi.failed'

# 7. A new version that doesn't start, twice in a row: the good copy survives both.
setup commit_in_work 'echo "raise SystemExit(\"made-up startup failure\")" > run.py'
deploy_from "$work"; rc=$?
check "app that won't start: fails" test "$rc" -ne 0
check "  points at the failed copy's log" said "doesn't answer on http://127.0.0.1:5001/ after 60s.*HouseOfPi.failed/log.txt"
check "  puts the good copy back" on_pi 'test -e ~/HouseOfPi/good-copy'
check "  which answers" answers
check "  the failed copy's log says why" on_pi 'grep -q "made-up startup failure" ~/HouseOfPi.failed/log.txt'
deploy_from "$work"; rc=$?
check "the same failure again: fails" test "$rc" -ne 0
check "  the good copy is still put back" on_pi 'test -e ~/HouseOfPi/good-copy'
check "  and answers" answers

# 8. A deploy already running on the Pi: refuses, changes nothing.
running=$(app_pid)
on_pi 'exec 9>~/.pi-deploy.lock; flock 9; sleep 30' & holder=$!
sleep 2
deploy; rc=$?
check "deploy already running: refuses" test "$rc" -ne 0
check "  says why" said 'another deploy is still running'
check "  the running app is untouched" test "$(app_pid)" = "$running"
kill "$holder" 2>/dev/null; on_pi 'pkill -f "sleep 30"' 2>/dev/null; wait "$holder" 2>/dev/null

# 9. The connection drops mid-deploy: the deploy on the Pi carries on and finishes.
deploy & client=$!
sleep 15
kill "$client" 2>/dev/null; pkill -f "docker exec -i -u pi -e HOME=/home/pi $pi bash -c" 2>/dev/null; wait "$client" 2>/dev/null
on_pi 'for _ in $(seq 1 120); do [ -s ~/pi-deploy.status ] && break; sleep 2; done'
check "dropped connection: the deploy still finishes" test "$(on_pi 'cat ~/pi-deploy.status')" = 0
check "  and the app answers" answers
check "  and replaced the good copy" on_pi '! test -e ~/HouseOfPi/good-copy && test -e ~/HouseOfPi.previous/good-copy'

# 10. The documented undo in pi-deploy.sh's header puts the previous copy back.
undo=$(sed -n '/To put it back:/,/^set /p' "$repo/deploy/pi-deploy.sh" | grep -v 'To put it back:\|^set ' | sed 's/^#  *//; s/ *\\$//' | tr '\n' ' ')
on_pi "$undo" >/dev/null 2>&1
check "the documented undo restores the old copy" on_pi 'test -e ~/HouseOfPi/good-copy'
check "  and it answers" answers

# 11. HTTPS on all addresses and the default port (the settings before nginx): the check follows them.
setup on_pi 'cd ~/certs && openssl req -x509 -newkey rsa:2048 -nodes -subj /CN=made-up -days 1 -keyout server.key -out server.csr
  printf "%s\n" "export AUTHENTICATION_SECRET=made-up" "export PYTHON_SSL_ON=True" > ~/house-env/env-vars.sh'
deploy; rc=$?
check "https on the default port: succeeds" test "$rc" -eq 0
check "  checked the right address" said 'Deployed: the app answers on https://127.0.0.1:5000/'
check "  which answers" answers_on https://127.0.0.1:5000/

# 12. Nothing secret is ever shown, in any deploy's output.
check "output never shows a setting's value" bash -c "! grep -q made-up '$out'"

echo
if [ "$fails" -eq 0 ]; then echo "all passed"; else echo "$fails failed"; exit 1; fi
