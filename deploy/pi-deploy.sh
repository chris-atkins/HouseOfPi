#!/usr/bin/env bash
# Runs on the Pi, as pi: replaces the running app with the files in ~/jenkins-ssh-home.
# deploy/deploy-to-pi.sh copies those files over (this script among them) and starts this script
# detached from its SSH session, so a dropped connection or an aborted build can't stop it halfway.
#
# The cert, key and settings live only on the Pi (~/certs, ~/house-env/env-vars.sh). nginx serves
# TLS on :5000 and proxies to the app (deploy/nginx/README.md); this script doesn't touch nginx.
#
# If anything fails after the running app was stopped, the copy it replaced is put back and
# started, and the deploy still fails. The failed copy is kept as ~/HouseOfPi.failed (its log.txt
# says why). After a good deploy, the replaced copy is kept as ~/HouseOfPi.previous. To put it back:
#   sudo killall python; cd ~ && rm -rf HouseOfPi && mv HouseOfPi.previous HouseOfPi && cd HouseOfPi \
#     && . ./env-vars.sh && (setsid ./env-setup/run-server < /dev/zero &> log.txt &)
set -euo pipefail
exec </dev/null
cd "$HOME"

say() { echo "$(date -u +%H:%M:%S) $*"; }
fail() { say "DEPLOY FAILED: $*" >&2; exit 1; }

# pi may run only killall without a password (sudoers). The app runs as env/bin/python ./run.py.
# killall exits non-zero when nothing was running, which is fine here.
stop_app() {
    sudo -n killall run.py python 2>/dev/null || true
    for _ in $(seq 1 20); do
        pgrep -f '[.]/run[.]py' >/dev/null || return 0
        sleep 0.5
    done
    return 1
}

# Both run in an app copy's directory. env-vars.sh is the Pi's own file, so -u is off while it's read.
# 9>&- : the app mustn't inherit the deploy lock (deploy-to-pi.sh), or it would hold it for good.
start_app() {
    (set +u; . ./env-vars.sh; setsid ./env-setup/run-server < /dev/zero &> log.txt 9>&- &)
}
app_url() {
    (
        set +u
        . ./env-vars.sh >/dev/null 2>&1
        scheme=http
        case "$(echo "${PYTHON_SSL_ON:-}" | tr '[:upper:]' '[:lower:]' | tr -d ' ')" in true|yes) scheme=https ;; esac
        host=$(echo "${PYTHON_HOST:-}" | tr -d ' ')
        case "$host" in ''|0.0.0.0) host=127.0.0.1 ;; esac
        port=$(echo "${PYTHON_PORT:-}" | tr -d ' ')
        echo "$scheme://$host:${port:-5000}/"
    )
}
answers() {
    for _ in $(seq 1 30); do
        curl -fsSk --max-time 5 -o /dev/null "$1" 2>/dev/null && return 0
        sleep 2
    done
    return 1
}

# Called on any failure once the old app has been stopped.
restore() {
    set +e
    trap - EXIT
    cd "$HOME"
    say "Putting the previous copy back"
    stop_app
    rm -rf HouseOfPi.failed
    [ -d HouseOfPi ] && mv HouseOfPi HouseOfPi.failed
    if [ ! -d HouseOfPi.previous ]; then
        say "There's no previous copy to put back. THE APP IS NOT RUNNING."
        return
    fi
    mv HouseOfPi.previous HouseOfPi
    cd HouseOfPi
    start_app
    if answers "$(app_url)"; then
        say "The previous copy is running again and answers."
    else
        say "The previous copy doesn't answer either. THE APP IS NOT RUNNING; see ~/HouseOfPi/log.txt."
    fi
}

# Check everything the new copy needs before stopping the running app.
[ -f jenkins-ssh-home/run.py ] || fail "~/jenkins-ssh-home/run.py is missing; the copy step didn't run."
for f in certs/server.csr certs/server.key house-env/env-vars.sh; do
    [ -s "$f" ] || fail "~/$f is missing or empty."
done

say "Stopping the app"
stop_app || fail "the old app is still running after 10s, so the new one couldn't take its port. Nothing was changed."
trap 'rc=$?; if [ "$rc" -ne 0 ]; then restore; fi; exit "$rc"' EXIT

say "Keeping the old copy as ~/HouseOfPi.previous"
rm -rf HouseOfPi.previous
if [ -d HouseOfPi ]; then mv HouseOfPi HouseOfPi.previous; fi

mkdir HouseOfPi
cp -a jenkins-ssh-home/. HouseOfPi
cp certs/server.csr HouseOfPi/cert.crt
cp certs/server.key HouseOfPi/key.key
cp house-env/env-vars.sh HouseOfPi/env-vars.sh
cd HouseOfPi
chmod a+x env-setup/install-server-env env-setup/run-server

say "Installing the Python packages"
./env-setup/install-server-env
# install-server-env carries on past a failed pip install, so check the results here. Without
# rpi.gpio the app would quietly fall back to fake GPIO.
env/bin/python -c 'import flask, flask_apscheduler, requests, lxml, pywemo' \
    || fail "Python packages are missing after install-server-env; see the output above."
env/bin/python -m pip show -q rpi.gpio >/dev/null 2>&1 \
    || fail "rpi.gpio didn't install, so the app would run with fake GPIO; see the output above."

say "Starting the app"
start_app
url=$(app_url)
answers "$url" || fail "the new copy doesn't answer on $url after 60s; its output is in ~/HouseOfPi.failed/log.txt."

trap - EXIT
rm -rf "$HOME/HouseOfPi.failed"
say "Deployed: the app answers on $url"
