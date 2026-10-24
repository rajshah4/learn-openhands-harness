#!/usr/bin/env python3
"""Prepare fresh workshop workspaces and run independent local checks."""
from __future__ import annotations
import argparse
import ast
import contextlib
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import re
import subprocess
import sys
import time
import uuid
import classroom

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
    'w5-goal': ('goals', 'w5-goal', None),
    'w5-goal-capped': ('goals', 'w5-goal-capped', None),
    'w6-single': ('async', 'w6-single', None),
    'w6-validator': ('async', 'w6-validator', None),
}
IGNORED = {'.git', '.venv', '__pycache__', '.pytest_cache'}

# Folder names match the exercise pages. Each comparison owns its own copy.
WORKSPACES = [
    ('w1', 'w1-openhands', 'Workshop-OpenHands'),
    ('w1', 'w1-pi', 'Workshop-Pi'),
    ('w1', 'w1-opencode', 'Workshop-OpenCode'),
    *[('w2', 'w2-' + mode, 'Workshop-OpenHands; tools: ' + mode)
      for mode in ('terminal', 'primitive', 'broad', 'task-shaped')],
    *[(case, case, 'Workshop-OpenHands')
      for case in ('w3-agreement-none', 'w3-agreement-draft', 'w3-agreement-accepted')],
    *[('w4-async', 'w4-counter-' + tier, tier + ' model profile')
      for tier in ('flash', 'pro')],
    *[('w4-controlled-security', 'w4-security-' + tier, tier + ' model profile')
      for tier in ('flash', 'pro')],
    ('w5-checkpoint-ordinary', 'w5-checkpoint-ordinary', 'Workshop-OpenHands; ordinary conversation'),
    ('w5-checkpoint-goal', 'w5-checkpoint-goal', 'Workshop-OpenHands; native goal mode'),
    ('w6-reservation-single', 'w6-reservation-single', 'Workshop-OpenHands; one repair owner'),
    ('w6-reservation-team', 'w6-reservation-team', 'Workshop-OpenHands; independent adversary'),
]
PROMPT_INDEX = 'https://rajshah4.github.io/learn-openhands-harness/workshops/odsc-2026/prompts'
EXERCISE_PAGES = dict(zip(('w1', 'w2', 'w3', 'w4', 'w5', 'w6'), (
    '00-working-harness', '01-add-harness-capability', '02-place-context',
    '03-model-routing', '04-let-it-run', '05-multi-agent')))


def exercise_url(case):
    return PROMPT_INDEX.rsplit('/', 1)[0] + '/exercises/' + EXERCISE_PAGES[case.split('-')[0]]

def files(folder):
    return {str(p.relative_to(folder)): p for p in folder.rglob('*')
            if p.is_file() and not any(x in IGNORED for x in p.relative_to(folder).parts)
            and p.suffix != '.pyc'}

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prompt(case):
    _, name, guidance = CASES[case]
    text = (ROOT / 'prompts' / f'{name}.txt').read_text()
    text = text.replace('{python}', shlex.quote(sys.executable))
    if guidance:
        notes = (ROOT / 'guidance' / f'{guidance}.md').read_text().replace('python3 -m pytest', shlex.quote(sys.executable) + ' -m pytest')
        if notes.strip():
            text = 'Supplied project notes (verify against newer accepted records):\n\n' + notes + '\n\nTask:\n' + text
    if case in ('w5-goal', 'w5-goal-capped'):
        text = '/goal --max 2 ' + text
    return text

def prepare(case, workspace):
    if workspace.exists():
        raise ValueError('Workspace already exists. Choose a new path; preparation never overwrites work.')
    if workspace == ROOT or ROOT in workspace.parents:
        raise ValueError('Choose a workspace outside the lab package.')
    checkout = ROOT.parents[2]
    if checkout in workspace.parents:
        print('Tip: use a workspace outside the course checkout, such as ../odsc-runs/my-run.', file=sys.stderr)
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


def prepare_all(parent):
    checkout = ROOT.parents[2]
    if parent == checkout or checkout in parent.parents:
        raise ValueError('Choose a workspace parent outside the course checkout, such as ../odsc-runs.')
    # Validate the inputs before creating the session. Preparation never resets old work.
    for case, _, _ in WORKSPACES:
        if case in classroom.CASES:
            classroom.prompt(case)
            fixture = classroom.CASES[case]['starter']
            if not (classroom.DATA / 'starters' / fixture).is_dir():
                raise ValueError('Missing classroom starter: ' + fixture)
        else:
            prompt(case)
            fixture = CASES[case][0]
            if fixture and not (ROOT / 'starters' / fixture).is_dir():
                raise ValueError('Missing starter: ' + fixture)
    session = parent / ('session-' + time.strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6])
    session.mkdir(parents=True, exist_ok=False)
    prompts = session / 'prompts'
    prompts.mkdir()
    records = []
    lines = ['WORKSHOP WORKSPACES', '', 'Exercise prompts: ' + PROMPT_INDEX,
             'Python interpreter for web prompts: ' + shlex.quote(sys.executable), '',
             'Open one exercise folder in Canvas, not this session folder.',
             'Start a new conversation for each run. Keep prompts and this index outside the agent workspace.',
             'Each retry of prepare-all creates a new session and leaves previous runs alone.', '']
    for case, name, profile in WORKSPACES:
        workspace = session / name
        classroom_case = case in classroom.CASES
        with contextlib.redirect_stdout(io.StringIO()):
            (classroom.prepare if classroom_case else prepare)(case, workspace)
        prompt_file = prompts / (name + '.txt')
        prompt_file.write_text((classroom.prompt if classroom_case else prompt)(case) + '\n')
        record = {'case': case, 'workspace': str(workspace), 'profile_or_configuration': profile,
                  'exercise_page': exercise_url(case), 'prompt_file': str(prompt_file)}
        records.append(record)
        lines.extend([name, '  Canvas workspace: ' + str(workspace), '  Profile/configuration: ' + profile,
                      '  Get the prompt: ' + exercise_url(case),
                      '  Optional local prompt copy: ' + str(prompt_file)])
        if case != 'w2':
            command = shlex.join([sys.executable, str(ROOT / ('classroom.py' if classroom_case else 'lab.py')), 'check', case,
                                  '--workspace', str(workspace)])
            record['check_command'] = command
            lines.append('  After the run, check: ' + command)
            if case == 'w5-goal-capped':
                lines.append('  Expected: unchanged files and a failed dot check; inspect Canvas for continuation and the two-audit cap.')
        lines.append('')
    (session / 'workspaces.json').write_text(json.dumps(records, indent=2) + '\n')
    index = session / 'WORKSPACES.txt'
    index.write_text('\n'.join(lines))
    print(f'Prepared {len(records)} fresh workspaces for all six exercises. No agents were run.')
    print(f'Session: {session}\nWorkspace, profile, prompt and check instructions: {index}')
    print('\nStart Exercise 1 with:')
    for record in records[:3]:
        print(f"  {record['profile_or_configuration']}: {record['workspace']}")
    print('\nIn Canvas, open the Workshop-OpenHands folder above and start a new conversation.')
    print('Open Exercise 1 for its prompt: ' + exercise_url('w1'))
    print('All exercise prompts: ' + PROMPT_INDEX)
    print('Replace the web prompt\'s interpreter placeholder with: ' + shlex.quote(sys.executable))
    return session

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
    return sorted(changed), sorted(forbidden)

def check(case, workspace, strict_scope=False):
    if not workspace.is_dir(): raise ValueError('Workspace does not exist.')
    if CASES[case][0] is None:
        raise ValueError('Exercise 2 requires the human evidence rubric, not a code checker.')
    changed, unexpected = scope(case, workspace)
    if strict_scope and unexpected:
        raise AssertionError('Unexpected file edits: ' + ', '.join(unexpected))
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
                        assert result.items == items[(page - 1)*size:page*size], f'Pagination omitted or changed items on page {page}, per_page={size}, input={items!r}.'
                        seen.extend(result.items)
                    assert seen == items and items == before, 'Pagination lost, duplicated, or mutated input items.'
            for page, size in [(0,1),(1,0)]:
                try: p.paginate([1],page,size)
                except ValueError: pass
                else: raise AssertionError('Invalid bounds accepted.')
            if fixture == 'rename':
                names = {n.id for n in ast.walk(ast.parse((workspace/'toyapp/pagination.py').read_text())) if isinstance(n,ast.Name)}
                assert 'source_items' in names and 'raw_items' not in names, 'Rename is not complete: use source_items and remove raw_items.'
        elif fixture == 'async':
            import asyncio
            a = importlib.import_module('toyapp.async_jobs')
            for attempt in range(20):
                actual = a.run_batch_sync(50)
                assert actual == 50, f'Counter lost updates: expected 50, got {actual}, attempt {attempt + 1}.'
            a.WORK_DELAY_SECONDS = 0.02
            original_sleep = a.asyncio.sleep
            probe = {'delayed_calls': 0, 'active': 0, 'max_active': 0}
            async def observed_sleep(delay, *args, **kwargs):
                if delay > 0:
                    probe['delayed_calls'] += 1
                    probe['active'] += 1
                    probe['max_active'] = max(probe['max_active'], probe['active'])
                    try:
                        return await original_sleep(delay, *args, **kwargs)
                    finally:
                        probe['active'] -= 1
                return await original_sleep(delay, *args, **kwargs)
            a.asyncio.sleep = observed_sleep
            try:
                start = time.monotonic()
                actual = asyncio.run(a.run_batch(30))
                elapsed = time.monotonic() - start
            finally:
                a.asyncio.sleep = original_sleep
            assert actual == 30, f'Counter expected 30, got {actual}.'
            assert probe['delayed_calls'] >= 30, 'The simulated work delay was removed. Keep the work and repair the shared update.'
            assert probe['max_active'] > 1, 'The simulated jobs ran one at a time. Keep the work concurrent.'
            assert 0.02 <= elapsed < 0.30, f'Work delay or concurrency needs inspection ({elapsed:.3f}s). Retry on an idle host if it was overloaded.'
        elif fixture == 'goals':
            s = importlib.import_module('slugify').slugify
            for given, wanted in [('api.v1 endpoint','api.v1-endpoint'),('Hello World!','hello-world'),
                                  ('Café déjà vu!','cafe-deja-vu'),('Straße der Erinnerung','strasse-der-erinnerung'),
                                  ('Special @#$% Characters!','special-characters'),('', ''),(None,'')]:
                assert s(given) == wanted, f'{given!r}: wanted {wanted!r}, got {s(given)!r}'
        elif fixture == 'security':
            report = (workspace/'SECURITY_REVIEW.md').read_text().lower()
            groups = {
                'debug-header bypass': r'x-debug-user',
                'Bearer parsing': r'\bbearer\b',
                'hardcoded tokens': r'hard[ -]?coded|embedded.*token',
                'health prefix': r'\bhealth\b|/health',
                'proposed fix': r'\b(?:fix(?:es)?|remediation|recommend(?:ation|ations|ed)?|mitigat(?:e|ion))\b',
            }
            missing = [k for k, pattern in groups.items() if not re.search(pattern, report)]
            print('Optional topic coverage: ' + (', '.join(missing) + ' not mentioned.' if missing else 'all example topics mentioned.'))
            print('Read the explanation and proposed fix against source. Topic coverage is not a security verdict.')
            print('A dict membership test does not establish a timing attack. Discuss timing-safe comparison only where the proposed design needs it.')
    print(json.dumps({'case':case,'passed':None if fixture == 'security' else True,'changed_files':changed,'scope_notes':unexpected},indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['list','prepare','prepare-all','prompt','check'])
    parser.add_argument('case',choices=list(CASES),nargs='?')
    parser.add_argument('--workspace',type=Path)
    parser.add_argument('--strict-scope',action='store_true',help='Optionally reject edits outside the supplied fixture scope.')
    args=parser.parse_args()
    try:
        if args.action=='list': print('\n'.join(CASES));return 0
        if args.action=='prepare-all':
            prepare_all((args.workspace or ROOT.parents[3] / 'odsc-runs').expanduser().resolve())
            return 0
        if not args.case: parser.error('case is required')
        if args.action=='prompt': print(prompt(args.case));return 0
        if not args.workspace: parser.error('--workspace is required')
        workspace=args.workspace.expanduser().resolve()
        if args.action=='prepare': prepare(args.case,workspace)
        else: check(args.case,workspace,args.strict_scope)
        return 0
    except Exception as exc:
        print(json.dumps({'passed':False,'detail':f"{type(exc).__name__}: {exc or 'Inspect the implementation and test output.'}"},indent=2),file=sys.stderr)
        return 1

if __name__=='__main__': sys.exit(main())
