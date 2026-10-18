import copy
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from setup_examples import ROOT, TOKEN, digest, install, read, rebase, safe_destination, verify


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_manifest(self):
        manifest = verify(ROOT / 'package')
        self.assertEqual(len(manifest['examples']), 19)
        self.assertEqual(sum(e['events'] for e in manifest['examples']), 726)

    def test_dry_run_has_no_effect(self):
        install(ROOT / 'package', self.root / 'fresh')
        self.assertFalse((self.root / 'fresh').exists())

    def test_install_rebases_only_state(self):
        dest = self.root / 'fresh'
        install(ROOT / 'package', dest, False)
        first = next((dest / 'conversations').iterdir())
        state = read(first / 'base_state.json')
        self.assertTrue(state['workspace']['working_dir'].startswith(str(dest)))
        original = ROOT / 'package/conversations' / first.name / 'events'
        for event in original.glob('*.json'):
            self.assertEqual(digest(event), digest(first / 'events' / event.name))

    def test_existing_directory_refused(self):
        with self.assertRaisesRegex(ValueError, 'already exists'):
            install(ROOT / 'package', self.root, False)

    def test_tamper_refused_before_write(self):
        package = self.root / 'package'
        shutil.copytree(ROOT / 'package', package)
        (package / 'index.html').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            install(package, self.root / 'dest', False)
        self.assertFalse((self.root / 'dest').exists())

    def test_unlisted_file_refused(self):
        package = self.root / 'package'
        shutil.copytree(ROOT / 'package', package)
        (package / 'extra').touch()
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            verify(package)

    def test_package_symlink_refused(self):
        package = self.root / 'package'
        shutil.copytree(ROOT / 'package', package)
        (package / 'link').symlink_to('/etc/passwd')
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            verify(package)

    def test_destination_symlink_refused(self):
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            safe_destination(str(self.root / 'link/fresh'))

    def test_live_store_refused(self):
        with self.assertRaisesRegex(ValueError, 'live store'):
            safe_destination(str(self.root / '.openhands/fresh'))

    def test_traversal_rebase_refused(self):
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            rebase({'working_dir': TOKEN + '/../escape'}, self.root)

    def test_historical_text_never_rebased(self):
        obj = {'command': TOKEN + '/anything', 'working_dir': TOKEN + '/workspaces/example'}
        new = rebase(obj, self.root)
        self.assertEqual(new['command'], obj['command'])
        self.assertEqual(new['working_dir'], str(self.root / 'workspaces/example'))

    def test_no_credentials_or_execution_wiring(self):
        for path in (ROOT / 'package/conversations').rglob('base_state.json'):
            state = read(path)
            self.assertEqual(state['agent']['tools'], [])
            self.assertEqual(state['agent']['mcp_config'], {})
            self.assertEqual(state['agent_state'], {})
            self.assertIsNone(state['agent']['llm']['api_key'])
            self.assertEqual(state['secret_registry'], {'secret_sources': {}})
            self.assertEqual(state['execution_status'], 'finished')


class SDKAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from view_canvas import create_archive_app
        from fastapi.testclient import TestClient
        cls.temp = tempfile.TemporaryDirectory()
        cls.store = Path(cls.temp.name).resolve() / 'archive'
        install(ROOT / 'package', cls.store, False)
        cls.app = create_archive_app(cls.store, Path(os.environ.get('CANVAS_PACKAGE', '/opt/homebrew/lib/node_modules/@openhands/agent-canvas')))
        cls.client_context = TestClient(cls.app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client_context.__exit__(None, None, None)
        cls.temp.cleanup()

    def test_all_details_and_events(self):
        listing = self.client.get('/api/conversations/search?limit=100').json()
        self.assertEqual(len(listing['items']), 19)
        for row in verify(ROOT / 'package')['examples']:
            import uuid
            cid = str(uuid.UUID(row['id']))
            detail = self.client.get('/api/conversations/' + cid)
            self.assertEqual(detail.status_code, 200, cid)
            self.assertEqual(detail.json()['runtime_info']['can_resume'], False)
            self.assertEqual(detail.json()['runtime_info']['runtime_status'], 'missing')
            events = self.client.get('/api/conversations/' + cid + '/events/search?limit=100')
            self.assertEqual(events.status_code, 200)
            self.assertEqual(len(events.json()['items']), row['events'], cid)
        health = self.client.get('/archive-health').json()
        self.assertEqual(health['runtime_services'], 0)
        self.assertEqual(health['containers'], 0)
        self.assertFalse((self.store / 'workspaces').exists())

    def test_all_mutations_refused(self):
        cid = '7565473d-df03-46ad-b9d6-ba32a5cee17c'
        paths = ['/api/conversations', '/api/settings', '/api/conversations/' + cid + '/run',
                 '/api/conversations/' + cid + '/events', '/api/conversations/' + cid + '/fork',
                 '/api/conversations/' + cid + '/goal', '/api/conversations/' + cid + '/runtime/reprovision',
                 '/api/conversations/' + cid + '/bash/execute_bash_command']
        before = {p: digest(p) for p in (self.store / 'conversations').rglob('*.json')}
        for method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            for path in paths:
                self.assertEqual(self.client.request(method, path, json={}).status_code, 403)
        self.assertEqual(before, {p: digest(p) for p in (self.store / 'conversations').rglob('*.json')})

    def test_reads_never_initialize_agent_or_model(self):
        from openhands.sdk import LLM
        from openhands.sdk.conversation.impl.local_conversation import LocalConversation
        cid = '7565473d-df03-46ad-b9d6-ba32a5cee17c'
        with patch.object(LocalConversation, '_ensure_agent_ready', side_effect=AssertionError('agent init')):
            with patch.object(LLM, 'completion', side_effect=AssertionError('model call')):
                self.assertEqual(self.client.get('/api/conversations/' + cid).status_code, 200)
                self.assertEqual(self.client.get('/api/conversations/' + cid + '/events/search').status_code, 200)
                self.assertEqual(self.client.get('/api/conversations/' + cid + '/runtime').status_code, 200)
                self.assertEqual(self.client.get('/api/conversations/' + cid + '/agent_final_response').status_code, 404)

    def test_websockets_refused(self):
        from starlette.websockets import WebSocketDisconnect
        with self.assertRaises(WebSocketDisconnect):
            with self.client.websocket_connect('/sockets/conversations/7565473d-df03-46ad-b9d6-ba32a5cee17c'):
                self.fail('WebSocket unexpectedly accepted')

    def test_actual_event_schemas(self):
        from jsonschema import Draft202012Validator
        spec = read(ROOT / 'tests/event-schemas.json')
        count = 0
        for path in (ROOT / 'package/conversations').rglob('event-*.json'):
            event = read(path)
            schema = {'$ref': '#/components/schemas/' + event['kind'], 'components': spec['components']}
            errors = list(Draft202012Validator(schema).iter_errors(event))
            self.assertEqual(errors, [], str(path))
            count += 1
        self.assertEqual(count, 745)


if __name__ == '__main__':
    unittest.main(verbosity=2)
