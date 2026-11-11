#!/usr/bin/env python3
"""Checks that idle clients cannot freeze the HouseOfPi web server.

Opens some TCP connections to the server that never send anything (what an
internet scanner, or a caller that gave up mid-handshake, looks like), then
makes normal requests while those connections are held open.

Werkzeug's dev server with TLS fails this: it does the TLS handshake on its
single accept thread with no timeout, so one idle connection blocks every
request after it. Behind nginx it should pass, and nginx should drop the idle
connections after client_header_timeout.

Stdlib only, so it runs anywhere:
    python3 util-scripts/stall_test.py https://192.168.1.30:5000/
    python3 util-scripts/stall_test.py https://192.168.1.30:5000/ --idle 3 --hold 30

Exit code 0 = PASS, 1 = FAIL.
"""
import argparse
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit


def open_idle_connections(host, port, count):
    return [socket.create_connection((host, port), timeout=5) for _ in range(count)]


def count_closed_by_server(connections):
    closed = 0
    for conn in connections:
        conn.setblocking(False)
        try:
            if conn.recv(1, socket.MSG_PEEK) == b'':
                closed += 1
        except BlockingIOError:
            pass  # still open, nothing to read
        except OSError:
            closed += 1  # reset by the server
    return closed


def probe(url, timeout):
    """Returns (ok, description). Certificate checks are off: this is a liveness probe of a pinned self-signed cert."""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    started = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout, context=context) as response:
            return 200 <= response.status < 300, f'HTTP {response.status} in {time.monotonic() - started:.2f}s'
    except urllib.error.HTTPError as e:
        return False, f'HTTP {e.code} in {time.monotonic() - started:.2f}s'
    except (OSError, urllib.error.URLError) as e:
        return False, f'{type(e).__name__}: {e} after {time.monotonic() - started:.2f}s'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('url', help='URL to probe, e.g. https://192.168.1.30:5000/')
    parser.add_argument('--idle', type=int, default=1, help='idle connections to hold open (default 1)')
    parser.add_argument('--hold', type=float, default=0, help='keep probing for this many seconds (default: one probe)')
    parser.add_argument('--timeout', type=float, default=5, help='per-probe timeout in seconds (default 5)')
    args = parser.parse_args(argv)
    if args.idle < 1:
        parser.error('--idle must be at least 1')

    target = urlsplit(args.url)
    port = target.port or (443 if target.scheme == 'https' else 80)

    baseline_ok, baseline = probe(args.url, args.timeout)
    print(f'baseline probe (no idle clients): {baseline}')
    if not baseline_ok:
        print('FAIL: server is not healthy even without idle clients; fix that first')
        return 1

    idle = open_idle_connections(target.hostname, port, args.idle)
    print(f'opened {len(idle)} idle connection(s) to {target.hostname}:{port}')
    try:
        time.sleep(1)  # let the server accept them before probing
        all_ok = True
        deadline = time.monotonic() + args.hold
        while True:
            ok, description = probe(args.url, args.timeout)
            all_ok = all_ok and ok
            print(f'  probe with idle clients open: {description}  '
                  f'(idle closed by server: {count_closed_by_server(idle)}/{len(idle)})')
            if time.monotonic() >= deadline:
                break
            time.sleep(5)
    finally:
        for conn in idle:
            conn.close()

    print('PASS' if all_ok else 'FAIL: idle clients blocked normal requests')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
