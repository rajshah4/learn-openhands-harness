"""Offline calibration of defects, valid repairs, scope, and MCP surfaces."""
from pathlib import Path
import asyncio
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent

def command(*args,expected=0):
    result=subprocess.run([sys.executable,str(ROOT/'lab.py'),*args],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    assert result.returncode==expected,result.stdout+result.stderr

def patch(path,old,new):
    text=path.read_text();assert old in text;path.write_text(text.replace(old,new))

def main():
    counts=0
    with tempfile.TemporaryDirectory(prefix='workshop-calibration-') as tmp:
        for case in ['w1','w3-none','w3-older','w3-current','w4-rename','w4-pagination','w4-async','w4-security','w5','w6-single','w6-validator']:
            workspace=Path(tmp)/case
            command('prepare',case,'--workspace',str(workspace));counts+=1
            command('prepare',case,'--workspace',str(workspace),expected=1);counts+=1
            command('check',case,'--workspace',str(workspace),expected=1);counts+=1
            if case.startswith('w3'):
                p=workspace/'toyapp/pagination.py'
                p.write_text(p.read_text()+'''

@dataclass(frozen=True)
class CursorPage:
    items: list[object]
    next_cursor: str | None
    has_more: bool


def paginate_cursor(items, cursor=None, per_page=20):
    window = export_window(items, cursor, per_page)
    return CursorPage(window.records, window.resume_token, window.resume_token is not None)
''')
                p=workspace/'toyapp/catalog.py'
                p.write_text(p.read_text()+'''

from toyapp.pagination import paginate_cursor

def browse_next(items, cursor=None, per_page=20):
    return paginate_cursor(items, cursor, per_page)
''')
            elif case in ['w1','w4-pagination']:
                patch(workspace/'toyapp/pagination.py','end = start + per_page - 1','end = start + per_page')
            elif case=='w4-rename':patch(workspace/'toyapp/pagination.py','raw_items','source_items')
            elif case in ['w4-async','w6-single','w6-validator']:
                patch(workspace/'toyapp/async_jobs.py','''        current = self.value
        await asyncio.sleep(0)
        self.value = current + 1''','''        self.value += 1''')
            elif case=='w5':patch(workspace/'src/slugify.py',r'[^\w\s-]',r'[^\w\s.-]')
            elif case=='w4-security':
                # Demonstrates why coverage requires a separate human semantic review.
                (workspace/'SECURITY_REVIEW.md').write_text('x-debug-user bypass bearer replace timing compare_digest hardcoded token health prefix fix')
            command('check',case,'--workspace',str(workspace));counts+=1
            if case!='w4-security':
                env=dict(os.environ,PYTHONPATH=str(workspace/'src' if case=='w5' else workspace),PYTHONDONTWRITEBYTECODE='1')
                tests=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider'],cwd=workspace,env=env,capture_output=True,text=True)
                assert tests.returncode==0,tests.stdout+tests.stderr;counts+=1
            if case!='w5':
                (workspace/'toyapp/__init__.py').unlink()
                command('check',case,'--workspace',str(workspace),expected=1);counts+=1
        workspace=Path(tmp)/'serialized'
        command('prepare','w6-single','--workspace',str(workspace))
        p=workspace/'toyapp/async_jobs.py'
        patch(p,'self.value = 0','self.value = 0\n        self.lock = asyncio.Lock()')
        patch(p,'''        await asyncio.sleep(WORK_DELAY_SECONDS)
        current = self.value
        await asyncio.sleep(0)
        self.value = current + 1''','''        async with self.lock:
            await asyncio.sleep(WORK_DELAY_SECONDS)
            self.value += 1''')
        command('check','w6-single','--workspace',str(workspace),expected=1);counts+=1
        for p in (ROOT/'prompts').glob('*.txt'):
            assert '/Users/' not in p.read_text() and '/home/ubuntu/' not in p.read_text()
        counts+=1
    async def mcp_check():
        from fastmcp import Client
        for mode,expected in [('primitive',4),('broad',12),('task-shaped',1)]:
            os.environ['WORKSHOP_MCP_MODE']=mode
            spec=importlib.util.spec_from_file_location('workshop_mcp_'+mode,ROOT/'tools/github_mcp_server.py')
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            async with Client(module.mcp) as client:
                tools=await client.list_tools();assert len(tools)==expected,(mode,len(tools))
            def github_get(path):
                if '/files?' in path:return [{'filename':'src/a.py','changes':20,'patch':'code','blob_url':'https://example.invalid/a'},{'filename':'tests/test_a.py','changes':10,'patch':'test','blob_url':'https://example.invalid/test'}]
                if '/commits?' in path:return []
                return {'number':16860,'title':'Example','body':'Automated: tests passed','html_url':'https://example.invalid/pr'}
            module.github_get=github_get
            result=module.get_pull_request_evidence_bundle('OpenHands','OpenHands',16860)
            assert result and 'https://example.invalid' in json.dumps(result)
    asyncio.run(mcp_check());counts+=6
    print(json.dumps({'passed':True,'calibration_checks':counts,'live_model_calls':0}))

if __name__=='__main__':main()
