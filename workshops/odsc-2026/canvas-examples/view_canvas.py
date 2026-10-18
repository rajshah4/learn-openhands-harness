#!/usr/bin/env python3
"""Workshop-only read host for the pinned Canvas UI and SDK persisted-history API."""
import argparse
from contextlib import asynccontextmanager
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

from setup_examples import VERSIONS, read


def create_archive_app(store, canvas):
    # Isolate all incidental SDK stores before importing SDK modules.
    process_env = {k: v for k, v in os.environ.items() if k in ('PATH', 'LANG', 'LC_ALL', 'TMPDIR', 'SYSTEMROOT', 'WINDIR')}
    process_env.update(HOME=str(store / 'host-home'), PYTHON_DOTENV_DISABLED='1',
                       LITELLM_LOCAL_MODEL_COST_MAP='True', OPENHANDS_SUPPRESS_BANNER='1',
                       OH_PERSISTENCE_DIR=str(store / 'host-state'), OTEL_SDK_DISABLED='true', DO_NOT_TRACK='1')
    os.environ.clear()
    os.environ.update(process_env)
    for name, version in [('openhands-sdk', VERSIONS['sdk']), ('openhands-agent-server', VERSIONS['server']), ('openhands-tools', VERSIONS['sdk']), ('openhands-workspace', VERSIONS['sdk'])]:
        if importlib.metadata.version(name) != version:
            raise ValueError('Unsupported dependency version: ' + name)
    if read(canvas / 'package.json')['version'] != VERSIONS['canvas']:
        raise ValueError('Canvas must be version ' + VERSIONS['canvas'])
    if not (store / '.workshop-install.json').is_file():
        raise ValueError('Use setup_examples.py with a new dedicated store first')
    from cryptography.fernet import Fernet
    from fastapi import FastAPI, Request
    from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, RedirectResponse
    from fastapi.staticfiles import StaticFiles
    from openhands.agent_server.config import Config
    from openhands.agent_server.conversation_service import ConversationService
    from openhands.agent_server.conversation_router import conversation_router
    from openhands.agent_server.event_router import event_read_router
    from openhands.agent_server.docker_runtime.registry import DockerConversationRegistry
    from openhands.agent_server.server_details_router import server_details_router

    config = Config(conversations_path=store / 'conversations', workspace_path=store / 'workspaces',
                    secret_key=Fernet.generate_key().decode(), session_api_keys=[], conversation_runtime='docker')
    registry = DockerConversationRegistry(config)
    service = ConversationService(conversations_dir=store / 'conversations')
    registry.configure_service(service)
    # Prevent every hydration route, including future accidental GET integrations.
    service.get_event_service = service.get_persisted_event_service

    @asynccontextmanager
    async def lifespan(app):
        # Deliberately do not call registry.start(), api_lifespan(), Docker, tmux,
        # profile loading, automation, extension startup, or credential setup.
        async with service:
            yield

    app = FastAPI(lifespan=lifespan)
    app.state.config = config
    app.state.conversation_registry = registry
    app.state.conversation_service = service
    app.state.archive_service = service
    app.state.archive_registry = registry

    @app.middleware('http')
    async def readonly(request: Request, call_next):
        if request.method not in ('GET', 'HEAD'):
            return JSONResponse({'detail': 'Workshop archive is read-only'}, status_code=403)
        return await call_next(request)

    # Register only actual SDK read handlers. No execution proxy or workspace route.
    from fastapi import APIRouter
    reads = APIRouter()
    for route in conversation_router.routes:
        if getattr(route, 'methods', set()) == {'GET'} and route.name in {
                'search_conversations', 'count_conversations', 'get_conversation',
                'get_local_conversation_runtime', 'batch_get_conversations'}:
            reads.routes.append(route)
    app.include_router(reads, prefix='/api')
    app.include_router(event_read_router, prefix='/api')
    app.include_router(server_details_router)

    @app.get('/api/settings')
    async def settings():
        return {'agent_settings': {}, 'llm_settings': {}, 'confirmation_mode': True, 'user_consents_to_analytics': False, 'misc_settings': {'app_preferences': {'user_consents_to_analytics': False}, 'telemetry': {'consent': False}}}

    @app.get('/api/agent-profiles')
    @app.get('/api/llm-profiles')
    @app.get('/api/profiles')
    async def empty_profiles():
        return {'profiles': [], 'active_profile': None, 'active_agent_profile_id': None}

    @app.get('/api/meta-profiles')
    async def meta_profiles():
        return {'meta_profiles': [], 'active_meta_profile': None}

    @app.get('/archive-health')
    async def health():
        return {'mode': 'workshop-read-only', 'runtime_services': len(service._event_services),
                'containers': len(registry._containers), 'versions': VERSIONS}

    app.mount('/assets', StaticFiles(directory=canvas / 'build/assets'))
    app.mount('/locales', StaticFiles(directory=canvas / 'build/locales'))
    app.mount('/evidence', StaticFiles(directory=store / 'archive/evidence'))
    app.mount('/packet', StaticFiles(directory=store / 'archive', html=True))

    @app.get('/{path:path}')
    async def frontend(path: str):
        if path in ('', 'conversations'):
            return RedirectResponse('/conversations/49ef3890-c667-453f-ba62-c93074ca693b?backend=workshop')
        if path.startswith(('api/', 'sockets/', 'ws', 'server_info/')):
            return JSONResponse({'detail': 'Unavailable in workshop archive'}, status_code=404)
        candidate = (canvas / 'build' / path).resolve()
        if candidate.is_relative_to((canvas / 'build').resolve()) and candidate.is_file():
            return FileResponse(candidate)
        bootstrap = """<script>
+window.__AGENT_CANVAS_DO_NOT_TRACK__=true;
+localStorage.setItem('openhands-onboarded','1');
+localStorage.setItem('openhands-telemetry-consent','denied');
+localStorage.setItem('openhands-backends',JSON.stringify([{id:'workshop',name:'Workshop archive',kind:'local',host:location.origin,apiKey:''}]));
+localStorage.setItem('openhands-active-backend',JSON.stringify({backendId:'workshop'}));
+</script>""".replace('\n+', '\n')
        content = (canvas / 'build/index.html').read_text().replace('<head>', '<head>' + bootstrap)
        return HTMLResponse(content, headers={'Content-Security-Policy': "connect-src 'self'"})

    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--canvas', type=Path, required=True, help='Installed @openhands/agent-canvas directory')
    parser.add_argument('--port', type=int, default=28080)
    args = parser.parse_args()
    import uvicorn
    app = create_archive_app(args.store.resolve(), args.canvas.resolve())
    uvicorn.run(app, host='127.0.0.1', port=args.port)


if __name__ == '__main__':
    main()
