# HouseOfPi

<a href='http://45.55.61.213:8080/job/MH1.1-Build.HouseOfPi'><img src='http://45.55.61.213:8080/job/MH1.1-Build.HouseOfPi/badge/icon'></a>

Python app meant to run on a Raspberry Pi.  

It takes data from sensors and pushes them to the cloud (see MyHouse project), and responds to requests using physical outputs attached to the Pi.

## Running on the Pi

nginx terminates TLS on port 5000 and proxies to the app on `127.0.0.1:5001`. That
setup is manual (it is not in the Jenkins jobs) and is documented in
[deploy/nginx/README.md](deploy/nginx/README.md). The app reads where to listen from
`PYTHON_HOST`, `PYTHON_PORT`, `PYTHON_SSL_ON` and `PYTHON_DEBUG_ON`; see
`app/server/server_options.py`.

## Running the tests locally (macOS)

```sh
NO_PROXY='*' env/bin/pytest ./test
```
Without `NO_PROXY`, `requests` looks up the macOS system proxy settings inside the
forked test server, which crashes it, and about 50 integration tests fail with
`RemoteDisconnected`. CI runs on Linux and doesn't need this.
