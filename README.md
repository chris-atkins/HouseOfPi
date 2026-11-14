# HouseOfPi

Python app meant to run on a Raspberry Pi.  

It takes data from sensors and pushes them to the cloud (see MyHouse project), and responds to requests using physical outputs attached to the Pi.

## Running on the Pi

nginx terminates TLS on port 5000 and proxies to the app on `127.0.0.1:5001`. That
setup is manual (it is not in the Jenkins jobs) and is documented in
[deploy/nginx/README.md](deploy/nginx/README.md). The app reads where to listen from
`PYTHON_HOST`, `PYTHON_PORT`, `PYTHON_SSL_ON` and `PYTHON_DEBUG_ON`; see
`app/server/server_options.py`. Debug mode no longer forces plain HTTP:
`PYTHON_SSL_ON` applies in debug mode too.

## Deploying

The `house-of-pi` Jenkins job (on ci-3, defined in do-k8s-cluster) runs the tests in
`python:3.13-trixie`, then deploys to the Pi over SSH: it copies the app files to
`~/jenkins-ssh-home` and runs [deploy/pi-deploy.sh](deploy/pi-deploy.sh) there, detached from the
SSH session ([deploy/deploy-to-pi.sh](deploy/deploy-to-pi.sh)). It runs on every push to master and
daily at 07:33 UTC, which also restarts the app. If the new copy doesn't answer, the previous one is
put back and started, and the build fails and emails. After a good deploy the previous copy is kept
as `~/HouseOfPi.previous`; pi-deploy.sh's header has the commands to put it back by hand.
`deploy/test-pi-deploy.sh` tests both scripts against a stand-in Pi in Docker (commit first; it
deploys `HEAD`).

## Running the tests locally (macOS)

```sh
NO_PROXY='*' env/bin/pytest ./test
```
Without `NO_PROXY`, `requests` looks up the macOS system proxy settings inside the
forked test server, which crashes it, and about 50 integration tests fail with
`RemoteDisconnected`. CI runs on Linux and doesn't need this.
