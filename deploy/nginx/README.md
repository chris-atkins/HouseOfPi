# nginx in front of HouseOfPi

nginx terminates TLS on the Pi's port 5000 and proxies to the Flask app, which
listens on `127.0.0.1:5001` over plain HTTP. This setup is done by hand on the Pi.
It is **not** part of the Jenkins jobs, so after an SD-card rebuild, redo it from
this page.

## Why

Werkzeug's dev server (what `app.run()` uses) does the TLS handshake on its single
accept thread, with no timeout. One client that connects and then says nothing
blocks every later request, until the process is restarted. Examples of such a
client: an internet scanner, or a MyHouse connection that was queued while the
server was already stuck.

Alexa then reports *"the requested skill did not provide a valid response"*.

This was confirmed on 2026-11-11. The app had been frozen for about 4 hours by
one scanner connection, with 52 connections queued behind it.

nginx handles each connection on its own and drops idle clients after
`client_header_timeout`, which also covers the TLS handshake. Flask only ever
receives complete requests from nginx.

`util-scripts/stall_test.py` is the check: it FAILS against Werkzeug+TLS and
PASSES behind nginx.

```
Internet / MyHouse ──https:5000──▶ nginx ──http──▶ Flask (run.py) on 127.0.0.1:5001
```

The outside contract does not change:
- same URL and port
- same certificate (MyHouse pins it in its truststore)
- the `auth-secret` header is passed through untouched (it has a hyphen; nginx
  only drops headers with underscores)

## Files

| Where | What |
|---|---|
| `deploy/nginx/houseofpi.conf` (this repo) | the site config; source of truth |
| `/etc/nginx/sites-available/houseofpi` (Pi) | installed copy, symlinked from `sites-enabled/` |
| `/home/pi/certs/server.csr`, `server.key` (Pi) | cert (despite the name) and key, read by nginx |
| `/home/pi/house-env/env-vars.sh` (Pi) | sourced by the Jenkins deploy; tells Flask where to listen |
| `/var/log/nginx/houseofpi.access.log`, `.error.log` (Pi) | logs; rotated daily by Debian's logrotate, 14 days kept |

## Setup (fresh Pi, or redoing it)

Commands with `sudo` need the pi user's password. Run them in an SSH session on the Pi.

1. **Deploy the app as usual** (Jenkins MH1.1 → MH2.1), so this repo is on the Pi
   at `~/HouseOfPi`.

2. **Install nginx and the site.** Debian starts nginx on install with its default
   site on :80; we remove that site and stop nginx until the cutover.
   ```sh
   sudo apt install -y nginx
   sudo cp ~/HouseOfPi/deploy/nginx/houseofpi.conf /etc/nginx/sites-available/houseofpi
   sudo ln -sf /etc/nginx/sites-available/houseofpi /etc/nginx/sites-enabled/houseofpi
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo systemctl stop nginx
   ```
   Copy the file rather than symlinking into `~/HouseOfPi`: the deploy wipes that
   directory.

3. **Check before any downtime.** This checks that the cert and key parse and match,
   without binding port 5000:
   ```sh
   sudo nginx -t
   sudo crontab -l          # nothing should start run.py at boot
   openssl x509 -noout -fingerprint -sha256 -in ~/certs/server.csr
   ```
   The fingerprint must be the cert MyHouse's truststore pins. Compare it with what
   the app serves today:
   ```sh
   openssl s_client -connect localhost:5000 </dev/null 2>/dev/null | openssl x509 -noout -fingerprint -sha256
   ```
   This only works while the app still serves TLS itself.

4. **Move Flask to localhost without TLS.** Edit `~/house-env/env-vars.sh`. Keep the
   `export`s; the deploy `source`s this file:
   ```sh
   export PYTHON_SSL_ON=false
   export PYTHON_HOST=127.0.0.1
   export PYTHON_PORT=5001
   ```
   Then run Jenkins **MH2.1-Deploy.HouseOfPi**. Its log should show
   `STARTING SERVER on 127.0.0.1:5001 (ssl=False, debug=False)` in `~/HouseOfPi/log.txt`.

5. **Start nginx on 5000**, enabled so it comes back after a reboot:
   ```sh
   sudo systemctl enable --now nginx
   ```
   The app is unreachable between step 4's deploy and this step, which takes seconds.

## Verify

From any LAN machine with this repo:
```sh
curl -sk https://192.168.1.30:5000/                                # Hi there!
python3 util-scripts/stall_test.py https://192.168.1.30:5000/ --idle 3 --hold 20   # PASS
```
Expected stall-test result: every probe is HTTP 200, and "idle closed by server"
reaches 3/3 after about 10s.

On the Pi:
```sh
systemctl is-enabled nginx                     # enabled
ss -ltn '( sport = :5000 or sport = :5001 )'   # 0.0.0.0:5000 (nginx), 127.0.0.1:5001 (python)
tail -f /var/log/nginx/houseofpi.access.log    # rt= total time, urt= time spent in Flask
```
Then ask Alexa for something (lights, a temperature check).

## Rollback

The order matters. If Flask is moved back to :5000 while nginx still holds the
port, Flask fails to bind, and the only sign is in `~/HouseOfPi/log.txt`.

1. `sudo systemctl disable --now nginx`
2. In `~/house-env/env-vars.sh`, set `export PYTHON_SSL_ON=true` and delete the
   `PYTHON_HOST` / `PYTHON_PORT` lines.
3. Run Jenkins MH2.1.

## Maintenance

- **Cert rotation.** After replacing `~/certs/server.csr` / `server.key`, run
  `sudo nginx -t && sudo systemctl reload nginx`. The other rotation steps are
  unchanged (new truststore to CI-2, rebuild MyHouse). The deploy still copies the
  cert into `~/HouseOfPi` too; that copy is unused while `PYTHON_SSL_ON=false`.
- **Config change.** Edit `deploy/nginx/houseofpi.conf` here, commit, deploy, then
  repeat the `cp` from step 2 and `sudo nginx -t && sudo systemctl reload nginx`.
- **Logs.** Debian's `/etc/logrotate.d/nginx` rotates `/var/log/nginx/*.log` daily
  and keeps 14 compressed copies, so they don't grow without bound.
- **Timing data.** `rt=` / `urt=` in the access log is what MyHouse's client
  timeouts (2s connect, 5s read) are sized against. If `/house/command` requests
  regularly come close to 5s, revisit those numbers.
