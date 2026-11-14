# Work in progress

## Done: deploys move to the new Jenkins, ci-3 (2026-11-14)

The `house-of-pi` job on ci-3 replaces CI-2's MH1.1 and MH2.1 (now disabled). It tests in
`python:3.13-trixie` and deploys with `deploy/deploy-to-pi.sh` and `deploy/pi-deploy.sh` (see the
README's "Deploying"). First deploy on 2026-11-14 at 00:19 UTC: 119 tests passed, the app answered
after an 89s gap, and lights and thermostat were checked by hand. ci-3's key is in
`~/.ssh/authorized_keys`, limited to ci-3's address.

Follow-ups:
1. Change the `pi` password: the old CI-2 box logged in with it.
2. Turn off password logins from the internet (keep them on the LAN).
3. Prepare the new copy alongside the running one, then switch, to cut the ~90s daily gap.
4. Pin the Python packages; each deploy installs the latest of each.

## Done: idle clients freezing the Pi web server (2026-11-11)

**Symptom:** Alexa often spins about 30s, then says "the requested skill did not provide a
valid response". A redeploy of the Pi app makes it go away for a while.

**Root cause:** the app served HTTPS straight from Werkzeug's dev server. That server
does the TLS handshake on its single accept thread with no timeout, so one client
that connects and says nothing freezes every later request. Such a client is usually
an internet scanner, or a MyHouse connection queued while the app was already stuck.
- Seen live on 2026-11-11: frozen for about 4h by one scanner connection, with 52
  connections queued behind it.
- MyHouse made it worse: its Pi calls had no timeouts, so Alexa got no answer and all
  three scheduled-task threads hung for good.

**Fix:**
- HouseOfPi: nginx terminates TLS on :5000 and proxies to Flask on 127.0.0.1:5001.
  It's set up by hand; see [deploy/nginx/README.md](../deploy/nginx/README.md).
- HouseOfPi: `util-scripts/stall_test.py` is the acceptance test. It FAILS on
  Werkzeug+TLS and PASSES behind nginx.
- MyHouse: Pi calls time out after 2s (connect) / 5s (read).
- MyHouse: Alexa answers "couldn't reach the house" only when the command certainly
  didn't run. Otherwise it says "may still have worked".

**Status: done, cut over on 2026-11-11 at 23:41 UTC.**
- [x] Code: HouseOfPi (119 tests) and MyHouse (267 tests) are committed, reviewed and deployed.
- [x] Cutover: nginx 1.26.3 is enabled on :5000 and Flask is on 127.0.0.1:5001. The old
      settings are backed up at `~/house-env/env-vars.sh.pre-nginx` on the Pi.
- [x] Verified in the real thing:
  - the stall test, which FAILED against the Pi earlier the same day, PASSES (3 idle
    clients dropped after ~10s, every probe 200)
  - the served cert is unchanged (SHA256 F6:02:D3…)
  - MyHouse scheduled jobs and Alexa lights/temperature commands work through nginx
  - with Flask stopped, nginx returns a 502 and Alexa says "Sorry, I couldn't reach the
    house" immediately; a scheduled job hit the same 502, logged it and kept running
  - slowest real `/house/command` so far: 1.26s (`urt=` in the nginx access log)

## Follow-ups (most important first)
1. Timeouts on the Pi's own `requests` calls (thermostat, Hue, WeMo, MyHouse) in
   `app/server/api.py`. Without them, a hung device piles up Flask threads.
2. MyHouse `PiMessager` / `HueMessager` treat non-2xx responses (e.g. an nginx 502) as
   success, and never close those responses.
3. A systemd unit for the app, so it starts at boot. nginx already does.
4. Calibrate MyHouse's 2s/5s timeouts against nginx's `rt=`/`urt=` access-log timings
   after about a week.
5. Coverage tooling (pytest-cov), so "coverage didn't drop" can be measured.
6. Optional: `ProxyFix`, so Flask sees the real client IP.

## Running the tests locally
See the top-level README. On macOS, use `NO_PROXY='*'`.
