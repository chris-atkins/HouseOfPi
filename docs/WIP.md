# Work in progress

## Current: idle clients freezing the Pi web server (2026-11-11)

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

**Status:**
- [x] Code: HouseOfPi (119 tests) and MyHouse (267 tests) are committed, reviewed and deployed.
- [ ] Cutover on the Pi: runbook steps 3–6 need sudo, so the user runs them.
- [ ] Verify in the real thing:
  - stall test PASS against the Pi
  - authenticated requests go through nginx
  - Alexa lights and temperature commands work
  - failure modes: Flask down gives a 502 and "couldn't reach the house"
  - MyHouse scheduled jobs log again

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
