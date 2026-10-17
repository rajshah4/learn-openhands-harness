#!/usr/bin/env python3
"""Configure and verify the same OpenHands-hosted model in three harnesses."""
from __future__ import annotations

import argparse
import getpass
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

MODEL = 'deepseek-v4-flash'
GATEWAY = 'https://llm-proxy.app.all-hands.dev/v1'
SECRET = 'ODSC_LLM_API_KEY'
NAMES = {'openhands': 'Workshop-OpenHands', 'pi': 'Workshop-Pi', 'opencode': 'Workshop-OpenCode'}
ROOT = Path(__file__).resolve().parent


class Canvas:
    def __init__(self, url, key_file):
        self.url = url.rstrip('/')
        if urllib.parse.urlparse(self.url).hostname not in ('localhost', '127.0.0.1', '::1'):
            raise ValueError('Use a local Canvas backend on localhost or 127.0.0.1.')
        self.key = key_file.expanduser().read_text().strip()

    def request(self, method, path, payload=None, raw=False):
        req = urllib.request.Request(self.url + path, method=method,
            headers={'X-Session-API-Key': self.key, 'Content-Type': 'application/json'},
            data=None if payload is None else json.dumps(payload).encode())
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                data = response.read().decode()
            return data.strip() if raw else json.loads(data)
        except urllib.error.HTTPError as exc:
            # Responses can contain submitted configuration, so never echo the body.
            raise RuntimeError(f'Canvas {method} {path}: HTTP {exc.code}') from None


def private_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(json.dumps(data, indent=2) + '\n')
    path.chmod(0o600)


def model_access(base_url, key, model):
    req = urllib.request.Request(base_url.rstrip('/') + '/models',
        headers={'Authorization': 'Bearer ' + key})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            models = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'OpenHands model access failed: HTTP {exc.code}. Use the LLM API Key, not a Cloud API Key.') from None
    if model not in {item['id'] for item in models.get('data', [])}:
        raise ValueError(f'{model} is not available to this key. Do not substitute another model silently.')


def prepare_files(args):
    tools = {}
    for binary in ('pi', 'pi-acp', 'opencode'):
        found = shutil.which(binary, path=str(args.bin_dir) + os.pathsep + os.environ.get('PATH', '') if args.bin_dir else None)
        if not found:
            raise ValueError(f'Missing {binary}. Install the packages listed on the setup page first.')
        tools[binary] = str(Path(found).absolute())
    config = args.config_dir.expanduser().resolve()
    # Dedicated files avoid changing the student's existing Pi/OpenCode defaults.
    private_json(config / 'pi/models.json', {'providers': {'openhands': {
        'baseUrl': args.base_url, 'api': 'openai-completions',
        'apiKey': '$' + SECRET, 'authHeader': True,
        'compat': {'supportsDeveloperRole': False, 'supportsReasoningEffort': False},
        'models': [{'id': args.model, 'name': 'DeepSeek Flash (OpenHands)',
                    'reasoning': False, 'input': ['text'], 'contextWindow': 128000, 'maxTokens': 16384}]
    }}})
    private_json(config / 'pi/settings.json', {'defaultProvider': 'openhands', 'defaultModel': args.model})
    private_json(config / 'opencode.json', {
        '$schema': 'https://opencode.ai/config.json', 'model': 'openhands/' + args.model,
        'small_model': 'openhands/' + args.model, 'enabled_providers': ['openhands'],
        'provider': {'openhands': {'npm': '@ai-sdk/openai-compatible', 'name': 'OpenHands',
            'options': {'baseURL': args.base_url, 'apiKey': '{env:' + SECRET + '}'},
            'models': {args.model: {'name': 'DeepSeek Flash (OpenHands)',
                'limit': {'context': 128000, 'output': 16384}}}}}})
    commands = {
        'pi': shlex.join(['env', 'PI_CODING_AGENT_DIR=' + str(config / 'pi'),
                         'PI_ACP_PI_COMMAND=' + tools['pi'], tools['pi-acp']]),
        'opencode': shlex.join(['env', 'OPENCODE_CONFIG=' + str(config / 'opencode.json'),
                               tools['opencode'], 'acp']),
    }
    private_json(config / 'setup.json', {'model': args.model, 'base_url': args.base_url,
                                         'profiles': NAMES, 'canvas_url': args.canvas_url})
    return commands


def show_files(args):
    commands = prepare_files(args)
    print('Provider files prepared. No credentials requested; no Canvas settings changed.')
    print('In Canvas, add secret ' + SECRET + ', then create the profiles on the setup page.')
    for harness, command in commands.items():
        print('\n' + NAMES[harness] + ' Command (copy this entire line):\n' + command)
    print('\nModel for both ACP profiles: openhands/' + args.model)


def configure(args, canvas):
    key = (canvas.request('GET', '/api/settings/secrets/LLM_API_KEY', raw=True)
           if args.use_canvas_key else getpass.getpass('Paste your OpenHands LLM API Key (hidden): ').strip())
    if not key:
        raise ValueError('No key supplied.')
    model_access(args.base_url, key, args.model)
    commands = prepare_files(args)
    config = args.config_dir.expanduser().resolve()
    canvas.request('PUT', '/api/settings/secrets', {'name': SECRET, 'value': key,
        'description': 'OpenHands LLM key for the three workshop harnesses'})
    canvas.request('POST', '/api/profiles/Workshop-DeepSeek', {'llm': {
        'model': 'openhands/' + args.model, 'base_url': args.base_url, 'api_key': key,
        'reasoning_effort': 'none', 'num_retries': 2, 'timeout': 120,
        'max_output_tokens': 16384, 'drop_params': True}, 'include_secrets': True})
    existing = {p['name']: p for p in canvas.request('GET', '/api/agent-profiles')['profiles']}
    for harness, name in NAMES.items():
        body = {'schema_version': 3, 'name': name,
            'id': existing.get(name, {}).get('id', str(uuid.uuid4())),
            'mcp_server_refs': [], 'secret_refs': [SECRET], 'agent_kind': 'openhands' if harness == 'openhands' else 'acp'}
        if harness == 'openhands':
            body.update(llm_profile_ref='Workshop-DeepSeek',
                        tools=[{'name': 'terminal'}, {'name': 'file_editor'}])
        else:
            body.update(acp_server='custom', acp_command=commands[harness],
                        acp_model='openhands/' + args.model, acp_startup_timeout=120, acp_prompt_timeout=300)
        canvas.request('POST', '/api/agent-profiles/' + name, body)
        diagnostics = canvas.request('POST', '/api/agent-profiles/' + name + '/materialize', {})
        if not diagnostics.get('valid'):
            raise RuntimeError(f'{name} failed Canvas profile validation.')
        print(f'Configured {name}: openhands/{args.model}', flush=True)
    private_json(config / 'setup.json', {'model': args.model, 'base_url': args.base_url,
                                         'profiles': NAMES, 'canvas_url': canvas.url})
    print('Open a prepared exercise workspace, select a Workshop profile, and start a new conversation.')
    print('Run this script with verify to test all three profiles before class.')


def verify(args, canvas):
    import lab
    config = json.loads((args.config_dir.expanduser() / 'setup.json').read_text())
    # Pass only the model credential, never the Canvas administrative key, to agents.
    llm_key = canvas.request('GET', '/api/settings/secrets/' + SECRET, raw=True)
    profiles = {p['name']: p for p in canvas.request('GET', '/api/agent-profiles')['profiles']}
    run_root = args.runs_dir.expanduser().resolve() / time.strftime('setup-check-%Y%m%d-%H%M%S')
    run_root.mkdir(parents=True, exist_ok=False)
    results = []
    for harness, name in NAMES.items():
        workspace = run_root / harness
        lab.prepare('w1', workspace)
        # Prepare emits the full prompt; no credential is ever in it.
        prompt = lab.prompt('w1')
        result = {'harness': harness, 'profile': name, 'workspace': str(workspace)}
        try:
            baseline = subprocess.run([sys.executable, str(ROOT / 'lab.py'), 'check', 'w1',
                '--workspace', str(workspace)], text=True, capture_output=True)
            if baseline.returncode == 0:
                raise RuntimeError('Starter already passes. Restore the original course starter before comparing harnesses.')
            start = canvas.request('POST', '/api/conversations', {
                'agent_profile_id': profiles[name]['id'],
                'workspace': {'working_dir': str(workspace), 'kind': 'LocalWorkspace'},
                'autotitle': False, 'max_iterations': 30, 'worktree': False,
                'secrets': {SECRET: {'kind': 'StaticSecret', 'value': llm_key}},
                'initial_message': {'role': 'user', 'content': [{'type': 'text', 'text': prompt}], 'run': True}})
            cid = start['id']
            result['conversation_id'] = cid
            print(f'{name}: {canvas.url}/conversations/{cid}', flush=True)
            deadline = time.monotonic() + args.timeout
            while True:
                state = canvas.request('GET', '/api/conversations/' + cid)
                status = state.get('execution_status')
                if status in ('finished', 'error', 'paused', 'stuck'):
                    break
                if time.monotonic() >= deadline:
                    canvas.request('POST', '/api/conversations/' + cid + '/pause')
                    raise RuntimeError('Timed out; the test conversation was paused.')
                time.sleep(2)
            resolved = state.get('current_model_id') or state.get('agent', {}).get('llm', {}).get('model')
            result.update(status=status, resolved_model=resolved)
            if status != 'finished':
                raise RuntimeError('Conversation ended with status ' + str(status))
            if resolved not in (config['model'], 'openhands/' + config['model']):
                raise RuntimeError('Unexpected resolved model: ' + str(resolved))
            check = subprocess.run([sys.executable, str(ROOT / 'lab.py'), 'check', 'w1',
                '--workspace', str(workspace), '--strict-scope'], text=True, capture_output=True)
            (run_root / (harness + '-check.txt')).write_text(check.stdout + check.stderr)
            if check.returncode:
                raise RuntimeError('Independent checker failed. See ' + str(run_root / (harness + '-check.txt')))
            tests = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=workspace,
                text=True, capture_output=True)
            (run_root / (harness + '-pytest.txt')).write_text(tests.stdout + tests.stderr)
            if tests.returncode:
                raise RuntimeError('Independent pytest run failed. See ' + str(run_root / (harness + '-pytest.txt')))
            events = []
            page = ''
            while True:
                suffix = '?' + urllib.parse.urlencode({'page_id': page}) if page else ''
                data = canvas.request('GET', '/api/conversations/' + cid + '/events/search' + suffix)
                events.extend(data.get('items', []))
                page = data.get('next_page_id')
                if not page:
                    break
            # Save only tool actions/results. Configuration and model reasoning are excluded.
            actions = []
            for event in events:
                if event.get('kind') in ('ActionEvent', 'ObservationEvent') and event.get('tool_name') != 'finish':
                    actions.append({k: event[k] for k in ('kind', 'tool_name', 'action', 'observation') if k in event})
                elif event.get('kind') == 'ACPToolCallEvent' and event.get('status') == 'completed':
                    actions.append({k: event[k] for k in ('kind', 'title', 'raw_input', 'raw_output', 'content', 'is_error') if k in event})
            private_json(run_root / (harness + '-actions.json'), actions)
            diff = subprocess.run(['git', 'diff'], cwd=workspace, text=True, capture_output=True, check=True)
            (run_root / (harness + '-diff.txt')).write_text(diff.stdout)
            result['passed'] = True
            print(f'PASS {name}: {resolved}; independent behavior and scope checks passed.', flush=True)
        except (RuntimeError, ValueError, OSError) as exc:
            result.update(passed=False, error=str(exc))
            print(f'FAIL {name}: {exc}', flush=True)
        results.append(result)
        private_json(run_root / 'results.json', results)
    print('Results: ' + str(run_root / 'results.json'))
    return 0 if all(r['passed'] for r in results) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['files', 'configure', 'verify'])
    parser.add_argument('--canvas-url', default='http://localhost:8000')
    parser.add_argument('--key-file', type=Path, default=Path.home() / '.openhands/agent-canvas/api-key.txt')
    parser.add_argument('--config-dir', type=Path, default=Path.home() / '.openhands/odsc-2026')
    parser.add_argument('--base-url', default=GATEWAY)
    parser.add_argument('--model', default=MODEL)
    parser.add_argument('--bin-dir', type=Path, help='Optional directory containing installed harness executables')
    parser.add_argument('--use-canvas-key', action='store_true', help='Reuse LLM_API_KEY already saved in local Canvas instead of prompting')
    parser.add_argument('--runs-dir', type=Path, default=ROOT.parents[3] / 'odsc-runs')
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    try:
        if args.command == 'files':
            show_files(args)
            return 0
        canvas = Canvas(args.canvas_url, args.key_file)
        if args.command == 'configure':
            configure(args, canvas)
            return 0
        return verify(args, canvas)
    except (OSError, ValueError, RuntimeError) as exc:
        print('Setup stopped: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
