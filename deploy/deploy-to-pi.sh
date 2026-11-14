#!/usr/bin/env bash
# Copies the committed app files to the Pi and runs deploy/pi-deploy.sh there, then waits for it
# and shows its output. Exits non-zero if the deploy failed.
#
#   deploy/deploy-to-pi.sh <command that runs a shell command on the Pi>
#   deploy/deploy-to-pi.sh ssh -o ... pi@<pi>                      # the Jenkinsfile
#   deploy/deploy-to-pi.sh docker exec -i -u pi <container> bash -c   # deploy/test-pi-deploy.sh
#
# pi-deploy.sh runs detached on the Pi, holding a lock, so a dropped connection or an aborted build
# can't stop it halfway, and a second deploy can't start while one is running. The files are the
# ones the old Jenkins job copied, from git archive HEAD (not the workspace, which has the test
# stage's env/ and caches).
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "usage: $(basename "$0") <command that runs a shell command on the Pi>..." >&2
    exit 2
fi
cd "$(dirname "$0")/.."

# shellcheck disable=SC2016  # these run on the Pi, so they expand there
git archive --format=tar HEAD app env-setup util-scripts deploy/pi-deploy.sh $(git ls-files ':(glob)*.py') \
    | "$@" '
        exec 9>~/.pi-deploy.lock
        flock -n 9 || { echo "DEPLOY FAILED: another deploy is still running on the Pi." >&2; exit 3; }
        rm -rf ~/jenkins-ssh-home ~/pi-deploy.status
        mkdir ~/jenkins-ssh-home && tar -x -C ~/jenkins-ssh-home
        # The detached deploy inherits fd 9, so it holds the lock until it finishes.
        setsid bash -c "bash ~/jenkins-ssh-home/deploy/pi-deploy.sh > ~/pi-deploy.log 2>&1; echo \$? > ~/pi-deploy.status" \
            < /dev/null > /dev/null 2>&1 &
        echo "Started the deploy on the Pi"'

# pi-deploy.sh takes about 2 minutes, mostly pip. 15 minutes is far past anything normal.
"$@" '
    for _ in $(seq 1 450); do
        [ -s ~/pi-deploy.status ] && break
        sleep 2
    done
    cat ~/pi-deploy.log
    [ -s ~/pi-deploy.status ] || { echo "DEPLOY FAILED: no result after 15 minutes; see ~/pi-deploy.log on the Pi." >&2; exit 1; }
    exit "$(cat ~/pi-deploy.status)"'
