#!/usr/bin/env python3
"""Serve verified workshop transcripts on loopback without model or Canvas dependencies."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from setup_examples import ROOT, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=28081)
    args = parser.parse_args()
    verify(ROOT / 'package')
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / 'package'))
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'Open http://127.0.0.1:{server.server_port}/ . Stop with Ctrl-C.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
