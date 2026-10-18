#!/usr/bin/env python3
"""Install a verified classroom archive into a new, dedicated directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid

ROOT = Path(__file__).resolve().parent
VERSIONS = {'canvas': '1.27.1', 'sdk': '1.53.0', 'server': '1.53.0'}
TOKEN = '${WORKSHOP_ROOT}'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def verify(package):
    if package.is_symlink():
        raise ValueError('Package symlinks are forbidden')
    manifest = read(package / 'manifest.json')
    if manifest['format'] != 1 or manifest['versions'] != VERSIONS:
        raise ValueError('Unsupported package format or producing versions')
    expected = manifest['files']
    actual = set()
    for path in package.rglob('*'):
        if path.is_symlink():
            raise ValueError('Package symlinks are forbidden')
        if path.is_file() and path.relative_to(package).as_posix() != 'manifest.json':
            actual.add(path.relative_to(package).as_posix())
    if actual != set(expected):
        raise ValueError('Package has missing or unexpected files')
    for name, checksum in expected.items():
        path = package / name
        if Path(name).is_absolute() or '..' in Path(name).parts or digest(path) != checksum:
            raise ValueError('Unsafe path or checksum mismatch: ' + name)
    for row in manifest['examples']:
        folder = package / 'conversations' / uuid.UUID(row['id']).hex
        state = read(folder / 'base_state.json')
        meta = read(folder / 'meta.json')
        if state['execution_status'] != 'finished' or state['id'] != meta['id']:
            raise ValueError('Invalid archival state')
        events = [read(p) for p in sorted((folder / 'events').glob('event-*.json'))]
        ids = {e['id'] for e in events}
        if len(ids) != len(events) or len(events) != row['events']:
            raise ValueError('Duplicate or missing events')
        for event in events:
            parent = event.get('parent_id')
            if parent and parent != '__root__' and parent not in ids:
                raise ValueError('Unresolved event parent')
    return manifest


def safe_destination(raw):
    path = Path(raw).expanduser()
    if not path.is_absolute() or path.name in ('', '.', '..'):
        raise ValueError('Choose an absolute dedicated destination')
    # Do not follow even an ancestor symlink when choosing an install location.
    for part in [path, *path.parents]:
        if part.is_symlink():
            raise ValueError('Destination cannot contain symlinks')
    path = path.resolve()
    if path == Path.home() or len(path.parts) < 4:
        raise ValueError('Destination is too broad')
    if path.exists():
        raise ValueError('Destination already exists; use a new directory')
    if any(part in ('.openhands', 'dev_conversations', '.git') for part in path.parts):
        raise ValueError('Refusing a live store or repository control directory')
    if not path.parent.is_dir():
        raise ValueError('Destination parent must already exist')
    return path


def rebase(value, destination):
    """Rebase only structural locations, never historical commands or evidence."""
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key in ('working_dir', 'persistence_dir') and isinstance(item, str):
                if not item.startswith(TOKEN + '/'):
                    raise ValueError('Unexpected structural path')
                suffix = Path(item[len(TOKEN) + 1:])
                if '..' in suffix.parts or suffix.is_absolute():
                    raise ValueError('Unsafe structural path')
                result[key] = str(destination / suffix)
            else:
                result[key] = rebase(item, destination)
        return result
    if isinstance(value, list):
        return [rebase(item, destination) for item in value]
    return value


def install(package, destination, dry_run=True):
    manifest = verify(package)
    destination = safe_destination(str(destination))
    summary = {'destination': str(destination), 'examples': len(manifest['examples']),
               'events': sum(e['events'] for e in manifest['examples']), 'dry_run': dry_run}
    if dry_run:
        return summary
    stage = Path(tempfile.mkdtemp(prefix='.workshop-stage-', dir=destination.parent))
    try:
        shutil.copytree(package, stage / 'archive')
        for path in (stage / 'archive/conversations').rglob('*.json'):
            if path.name in ('meta.json', 'base_state.json'):
                write(path, rebase(read(path), destination))
        (stage / 'conversations').mkdir()
        for path in (stage / 'archive/conversations').iterdir():
            path.rename(stage / 'conversations' / path.name)
        shutil.rmtree(stage / 'archive/conversations')
        write(stage / '.workshop-install.json', {'format': 1, 'package_manifest_sha256': digest(package / 'manifest.json'),
              'versions': VERSIONS, 'ids': [e['id'] for e in manifest['examples']]})
        # mkdir is the no-overwrite commit. A racing creator wins, and we abort.
        destination.mkdir(mode=0o700)
        try:
            for path in stage.iterdir():
                path.rename(destination / path.name)
        except BaseException:
            shutil.rmtree(destination)
            raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=ROOT / 'package')
    parser.add_argument('--destination', required=True)
    parser.add_argument('--install', action='store_true', help='Write files; default is dry-run')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.package, args.destination, not args.install), indent=2))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
