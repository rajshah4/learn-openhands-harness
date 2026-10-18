#!/usr/bin/env python3
"""Prepare private, pinned Canvas dependencies for an installed workshop archive."""
import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--install', action='store_true', help='Download dependencies; default prints plan')
    args = parser.parse_args()
    store = args.store.expanduser().resolve()
    if not (store / '.workshop-install.json').is_file():
        parser.error('Install examples into a new dedicated store first')
    if sys.version_info < (3, 12):
        parser.error('Python 3.12 or newer required; tested with Python 3.13')
    if not shutil.which('npm'):
        parser.error('Install Node.js/npm before preparing Canvas; offline HTML needs neither')
    if any((store / name).exists() for name in ('.venv', 'ui')):
        parser.error('Runtime destination already exists; use a fresh archive store')
    env = dict(os.environ, PYTHON_DOTENV_DISABLED='1', PIP_DISABLE_PIP_VERSION_CHECK='1')
    commands = [
        [sys.executable, '-m', 'venv', str(store / '.venv')],
        [str(store / '.venv/bin/python'), '-m', 'pip', 'install',
         'openhands-agent-server==1.53.0', 'openhands-sdk==1.53.0',
         'openhands-tools==1.53.0', 'openhands-workspace==1.53.0'],
        ['npm', 'install', '--prefix', str(store / 'ui'), '--ignore-scripts', '--no-audit', '--no-fund',
         '@openhands/agent-canvas@1.27.1']]
    for command in commands:
        print(shlex.join(command), flush=True)
        if args.install:
            subprocess.run(command, check=True, env=env)
    print('Start with:')
    print(shlex.join([str(store / '.venv/bin/python'), str(Path(__file__).with_name('view_canvas.py')),
                     '--store', str(store), '--canvas', str(store / 'ui/node_modules/@openhands/agent-canvas')]))


if __name__ == '__main__':
    main()
