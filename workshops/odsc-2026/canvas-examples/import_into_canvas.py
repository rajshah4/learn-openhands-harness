#!/usr/bin/env python3
"""Import lecture histories into a stopped local npm Agent Canvas installation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import tempfile
import uuid
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
TAG = {'lecture': 'odsc2026'}
PREVIOUS_MANIFEST_SHA = '78315a2843d8a888140c3816c0abd275166c9c7e16c961f5644b11d34f87db3e'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_symlinks(path):
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('Symlink destinations are not supported: ' + str(path))

def verify_package(package):
    no_symlinks(package)
    m = read(package / 'manifest.json')
    actual = {p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    assert actual == set(m['files']), 'Missing or unexpected package files'
    for name, checksum in m['files'].items():
        rel = Path(name)
        assert not rel.is_absolute() and '..' not in rel.parts, 'Unsafe package path'
        p = package / rel
        no_symlinks(p)
        assert sha(p) == checksum, 'Package checksum mismatch: ' + name
    assert len(m['examples']) == 16 and sum(x['events'] for x in m['examples']) == 526, 'Unexpected lecture selection'
    return m

def stopped_backend(url):
    p = urlparse(url)
    if p.scheme != 'http' or p.hostname not in ('localhost', '127.0.0.1', '::1'):
        raise ValueError('Use the local backend URL printed by Agent Canvas')
    try:
        with socket.create_connection((p.hostname, p.port or 80), timeout=2):
            raise ValueError('Canvas backend is running. Stop Agent Canvas with Ctrl-C before importing, then restart it afterward.')
    except ConnectionRefusedError:
        pass

def rebase(obj, workspace, persistence):
    if isinstance(obj, dict):
        return {k: str(workspace) if k == 'working_dir' else str(persistence) if k == 'persistence_dir' else rebase(v, workspace, persistence) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rebase(x, workspace, persistence) for x in obj]
    return obj

def compatible_event(event):
    """Preserve content while mapping historical custom types to reader types."""
    edits = []
    if event.get('observation', {}).get('kind') == 'RouteObservation':
        event['observation']['kind'] = 'ClientToolObservation'
        edits.append('RouteObservation -> ClientToolObservation')
    if event.get('action', {}).get('kind') in ('ListAction', 'ReadAction', 'SearchAction', 'WriteAction', 'CheckAction'):
        old = event['action']
        event['action'] = {'kind': 'MCPToolAction', 'data': {k: v for k, v in old.items() if k != 'kind'}}
        edits.append(old['kind'] + ' -> generic action data wrapper')
    if event.get('kind') == 'SystemPromptEvent':
        for tool in event.get('tools', []):
            if tool.get('kind') in ('ListTool', 'ReadTool', 'SearchTool', 'WriteTool', 'CheckTool'):
                old_kind, old_action = tool['kind'], tool['action_type']
                tool.update(kind='ClientTool', client_tool_name=tool['title'], input_schema={'type': 'object', 'description': 'Archive compatibility wrapper for recorded ' + old_action}, action_type='MCPToolAction', observation_type='ClientToolObservation', meta={**(tool.get('meta') or {}), 'archive_original_tool_kind': old_kind, 'archive_original_action_type': old_action, 'archive_original_observation_type': 'RouteObservation'})
                edits.append(old_kind + ' -> generic tool metadata wrapper')
    return edits

def install(package, store, backend_url, apply=False):
    manifest = verify_package(package)
    no_symlinks(store)
    store = store.absolute()
    if store.name not in ('conversations', 'dev_conversations') or len(store.parts) < 4:
        raise ValueError('Choose the conversations or dev_conversations directory of your local Canvas installation')
    receipt = store.parent / 'odsc-lecture-import.json'
    expected = {uuid.UUID(x['id']).hex for x in manifest['examples']}
    if receipt.exists():
        old = read(receipt)
        assert set(old['ids']) == expected and old['source_manifest_sha256'] in (sha(package / 'manifest.json'), PREVIOUS_MANIFEST_SHA), 'Different import already recorded'
        for cid, files in old['installed_event_hashes'].items():
            for name, digest in files.items():
                assert sha(store / cid / 'events' / name) == digest, 'Installed history changed; refusing to overwrite'
        updates = []
        for row in manifest['examples']:
            meta_path = store / uuid.UUID(row['id']).hex / 'meta.json'
            meta = read(meta_path)
            if meta.get('title') != row['title'] or meta.get('tags', {}).get('lecture') != 'odsc2026':
                updates.append((meta_path, meta, row))
        if updates and apply:
            stopped_backend(backend_url)
            for meta_path, meta, row in updates:
                old.setdefault('previous_titles', {})[uuid.UUID(row['id']).hex] = meta.get('title')
                meta['title'] = row['title']
                meta['tags'] = {**meta.get('tags', {}), **TAG}
                meta['autotitle'] = False
                write(meta_path, meta)
            old['source_manifest_sha256'] = sha(package / 'manifest.json')
            write(receipt, old)
        return {'status': 'labels updated' if updates and apply else 'label update preview' if updates else 'already installed', 'histories': len(expected), 'labels': len(updates), 'filter': 'lecture=odsc2026'}
    collisions = sorted(cid for cid in expected if (store / cid).exists())
    if collisions:
        raise ValueError('Existing conversation IDs would collide; nothing overwritten: ' + ', '.join(collisions))
    summary = {'status': 'preview', 'store': str(store), 'histories': 16, 'events': 526, 'filter': 'lecture=odsc2026'}
    if not apply:
        return summary
    stopped_backend(backend_url)
    store.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.odsc-stage-', dir=store.parent))
    imported, changes, installed_hashes, created_workspaces = [], [], {}, []
    try:
        for row in manifest['examples']:
            cid = uuid.UUID(row['id']).hex
            src, dst = package / 'conversations' / cid, staging / cid
            shutil.copytree(src, dst)
            workspace = store.parent / 'odsc-lecture-workspaces' / cid
            tags = {**row.get('tags', {}), **TAG}
            no_symlinks(workspace)
            if workspace.exists():
                raise ValueError('Archive workspace already exists; refusing to reuse it: ' + str(workspace))
            workspace.mkdir(parents=True)
            created_workspaces.append(workspace)
            for filename in ('meta.json', 'base_state.json'):
                d = rebase(read(dst / filename), workspace, store / cid)
                d['tags'] = tags
                d['confirmation_policy'] = {'kind': 'AlwaysConfirm'}
                if filename == 'meta.json':
                    d.update(title=row['title'], autotitle=False, secrets={}, hook_config=None, plugins=None, tool_module_qualnames={}, client_tools=[])
                else:
                    assert d['execution_status'] == 'finished'
                    assert not d['agent']['llm'].get('api_key') and not d['agent']['tools']
                    d['agent']['agent_context'] = {k: False for k in ('load_public_skills', 'load_user_skills', 'load_project_skills', 'load_memory')}
                    d['max_iterations'] = 1
                write(dst / filename, d)
            for f in (dst / 'events').glob('*.json'):
                e = read(f)
                edits = compatible_event(e)
                if edits:
                    write(f, e)
                    changes.append({'conversation': cid, 'file': f.name, 'changes': edits, 'original_sha256': sha(src / 'events' / f.name)})
            installed_hashes[cid] = {f.name: sha(f) for f in (dst / 'events').glob('*.json')}
        for cid in sorted(expected):
            target = store / cid
            target.mkdir()  # No overwrite if another process races this import.
            imported.append(target)
            for f in (staging / cid).iterdir():
                f.rename(target / f.name)
        write(receipt, {'format': 1, 'ids': sorted(expected), 'source_manifest_sha256': sha(package / 'manifest.json'), 'installed_event_hashes': installed_hashes, 'compatibility_changes': changes, 'filter': 'lecture=odsc2026', 'originals': str(package)})
    except BaseException:
        for target in imported:
            shutil.rmtree(target)
        for workspace in created_workspaces:
            workspace.rmdir()
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return {**summary, 'status': 'installed', 'next': 'Restart agent-canvas. View > Filter by tags > lecture=odsc2026. Click More to expand the list.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=ROOT / 'package')
    parser.add_argument('--store', type=Path, default=Path(os.environ.get('OH_CONVERSATIONS_PATH', str(Path(os.environ.get('OH_CANVAS_SAFE_STATE_DIR', str(Path.home() / '.openhands/agent-canvas'))) / 'dev_conversations'))))
    parser.add_argument('--backend-url', default='http://127.0.0.1:18000')
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.package, args.store, args.backend_url, args.install), indent=2))
    except (ValueError, AssertionError, OSError) as e:
        parser.exit(1, str(e) + '\n')

if __name__ == '__main__':
    main()
