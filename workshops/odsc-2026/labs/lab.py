#!/usr/bin/env python3
"""Prepare fresh workshop workspaces and run independent local checks."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CASES = {
    'w1': ('pagination', 'w1', None),
    'w2': (None, 'w2', None),
    'w3-none': ('memory', 'w3', 'no-guidance'),
    'w3-older': ('memory', 'w3', 'outdated'),
    'w3-current': ('memory', 'w3', 'current'),
    'w4-rename': ('rename', 'w4-rename', None),
    'w4-pagination': ('pagination', 'w4-pagination', None),
    'w4-async': ('async', 'w4-async', None),
    'w4-security': ('security', 'w4-security', None),
    'w5': ('goals', 'w5', None),
    'w6-single': ('async', 'w6-single', None),
    'w6-validator': ('async', 'w6-validator', None),
}
IGNORED = {'.git', '.venv', '__pycache__', '.pytest_cache'}

def files(folder):
    return {str(p.relative_to(folder)): p for p in folder.rglob('*')
            if p.is_file() and not any(x in IGNORED for x in p.relative_to(folder).parts)
            and p.suffix != '.pyc'}

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prompt(case):
    _, name, guidance = CASES[case]
    text = (ROOT / 'prompts' / f'{name}.txt').read_text()
    text = text.replace('{python}', json.dumps(sys.executable))
    if case == 'w5':
        text += '\nFor imports and tests set PYTHONPATH=src in this workspace.\n'
    if guidance:
        notes = (ROOT / 'guidance' / f'{guidance}.md').read_text()
        if notes.strip():
            text = 'Supplied project notes (verify against newer accepted records):\n\n' + notes + '\n\nTask:\n' + text
    return text

def prepare(case, workspace):
    if workspace.exists():
        raise ValueError('Workspace already exists. Choose a new path; preparation never overwrites work.')
    if workspace == ROOT or ROOT in workspace.parents:
        raise ValueError('Choose a workspace outside the lab package.')
    fixture, _, _ = CASES[case]
    if fixture:
        shutil.copytree(ROOT / 'starters' / fixture, workspace)
    else:
        workspace.mkdir(parents=True)
    # Ignore generated artifacts; this git baseline exists only for local diff inspection.
    (workspace / '.gitignore').write_text('__pycache__/\n.pytest_cache/\n.venv/\n*.pyc\n')
    for command in [
        ['git', 'init', '-q'], ['git', 'add', '.'],
        ['git', '-c', 'user.name=Workshop baseline', '-c', 'user.email=workshop@example.invalid',
         '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Fresh workshop fixture'],
    ]:
        subprocess.run(command, cwd=workspace, check=True)
    print(f'Prepared {case}: {workspace}\nOpen only this workspace in your agent.\n\n{prompt(case)}')

def scope(case, workspace):
    fixture = CASES[case][0]
    baseline = files(ROOT / 'starters' / fixture)
    current = files(workspace)
    allowed = {'toyapp/pagination.py'} if fixture in ('pagination', 'rename') else set()
    if fixture == 'async': allowed = {'toyapp/async_jobs.py'}
    if fixture == 'memory':
        allowed = {'toyapp/pagination.py', 'toyapp/catalog.py', 'toyapp/tokens.py'}
        allowed.update(k for k in current if k.startswith('tests/') and k.endswith('.py'))
    if fixture == 'goals': allowed = {'src/slugify.py', 'tests/test_slugify.py'}
    if fixture == 'security': allowed = {'SECURITY_REVIEW.md'}
    changed = {k for k in baseline.keys() | current.keys()
               if k not in baseline or k not in current or hash_file(baseline[k]) != hash_file(current[k])}
    forbidden = changed - allowed - {'.gitignore'}
    if forbidden: raise AssertionError('Out-of-scope changes: ' + ', '.join(sorted(forbidden)))
    return sorted(changed)

def check(case, workspace):
    if not workspace.is_dir(): raise ValueError('Workspace does not exist.')
    if CASES[case][0] is None:
        raise ValueError('Exercise 2 requires the human evidence rubric, not a code checker.')
    changed = scope(case, workspace)
    fixture = CASES[case][0]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if fixture == 'memory':
        result = subprocess.run([sys.executable, str(ROOT / 'checks/memory.py'), '--repo', str(workspace)], env=env)
        if result.returncode: raise AssertionError('Memory public API or compatibility check failed.')
    else:
        sys.path.insert(0, str(workspace / 'src' if fixture == 'goals' else workspace))
        if fixture in ('pagination', 'rename'):
            p = importlib.import_module('toyapp.pagination')
            for n in range(12):
                for size in range(1, 5):
                    items = list(range(n)); before = items[:]
                    seen = []
                    for page in range(1, max(1, (n + size - 1) // size) + 1):
                        result = p.paginate(items, page, size)
                        assert result.items == items[(page - 1)*size:page*size]
                        seen.extend(result.items)
                    assert seen == items and items == before
            for page, size in [(0,1),(1,0)]:
                try: p.paginate([1],page,size)
                except ValueError: pass
                else: raise AssertionError('Invalid bounds accepted.')
            if fixture == 'rename':
                names = {n.id for n in ast.walk(ast.parse((workspace/'toyapp/pagination.py').read_text())) if isinstance(n,ast.Name)}
                assert 'source_items' in names and 'raw_items' not in names
        elif fixture == 'async':
            import asyncio
            a = importlib.import_module('toyapp.async_jobs')
            # Repeated correctness plus relative concurrency at a larger work delay.
            for _ in range(20): assert a.run_batch_sync(50) == 50
            a.WORK_DELAY_SECONDS = 0.02
            start = time.monotonic()
            assert asyncio.run(a.run_batch(30)) == 30
            elapsed = time.monotonic() - start
            assert elapsed < 0.30, f'Work serialized or host overloaded: {elapsed:.3f}s. Retry on an idle host.'
        elif fixture == 'goals':
            s = importlib.import_module('slugify').slugify
            for given, wanted in [('api.v1 endpoint','api.v1-endpoint'),('Hello World!','hello-world'),
                                  ('Café déjà vu!','cafe-deja-vu'),('Straße der Erinnerung','strasse-der-erinnerung'),
                                  ('Special @#$% Characters!','special-characters'),('', ''),(None,'')]:
                assert s(given) == wanted, f'{given!r}: wanted {wanted!r}, got {s(given)!r}'
        elif fixture == 'security':
            report = (workspace/'SECURITY_REVIEW.md').read_text().lower()
            groups = {'debug-header bypass':['x-debug-user','bypass'], 'Bearer parsing':['bearer','replace'],
                      'timing-safe comparison':['timing','compare_digest'], 'hardcoded tokens':['hardcoded','token'],
                      'health prefix':['health','prefix'], 'remediation':['fix']}
            missing = [k for k, terms in groups.items() if not all(t in report for t in terms)]
            assert not missing, 'Missing rubric terms: ' + ', '.join(missing)
            print('Coverage screen only. A human must verify each finding and fix against source.')
    print(json.dumps({'case':case,'passed':True,'changed_files':changed},indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','prepare','prompt','check'])
    parser.add_argument('case',choices=list(CASES),nargs='?')
    parser.add_argument('--workspace',type=Path)
    args=parser.parse_args()
    try:
        if args.action=='list': print('\n'.join(CASES));return 0
        if not args.case: parser.error('case is required')
        if args.action=='prompt': print(prompt(args.case));return 0
        if not args.workspace: parser.error('--workspace is required')
        workspace=args.workspace.expanduser().resolve()
        if args.action=='prepare': prepare(args.case,workspace)
        else: check(args.case,workspace)
        return 0
    except (AssertionError, ValueError, OSError, ImportError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'passed':False,'detail':str(exc)},indent=2),file=sys.stderr)
        return 1

if __name__=='__main__': sys.exit(main())
