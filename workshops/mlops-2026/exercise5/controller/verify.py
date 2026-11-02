"""External HTTP replay. Freeze once; never learn expectations from candidate."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent

def cases():
    base = {'customerId':' acme ', 'reference':'007', 'units':2, 'unitPrice':'12.50'}
    rows=[]
    def add(name, **changes): rows.append({'name':name,'request':dict(base, **changes)})
    add('omitted-memo')
    add('explicit-null', memo=None)
    add('numeric-customer', customerId=412, memo='renewal')
    add('text-reference', reference='PO-7', memo='rush')
    add('integer-reference', reference=7)
    add('numeric-string-units', units='3', unitPrice='0.10')
    add('zero-units', units=0)
    add('too-many-units', units=1001)
    add('negative-price', unitPrice='-1')
    add('unknown-field', coupon='FREE')
    add('blank-customer', customerId='  ')
    add('container-reference', reference={'id':7})
    add('bad-units', units='many')
    rows.append({'name':'field-name-alias','request':{'customer_id':' c2 ','reference':'19','units':1,'unit_price':'4.25'}})
    rows.append({'name':'missing-reference','request':{'customerId':'acme','units':1,'unitPrice':'1'}})
    return rows

def replay(workspace, python, rows):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
    with tempfile.TemporaryFile() as log:
        proc = subprocess.Popen([python,'-m','uvicorn','app:app','--host','127.0.0.1','--port',str(port)],cwd=workspace,stdout=log,stderr=log,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        try:
            url=f'http://127.0.0.1:{port}'
            for _ in range(100):
                if proc.poll() is not None:
                    log.seek(0); raise RuntimeError('service startup failed: '+log.read().decode()[-4000:])
                try:
                    with urllib.request.urlopen(url+'/openapi.json',timeout=1) as res: schema=json.load(res)
                    break
                except (OSError,ValueError): time.sleep(.1)
            else: raise RuntimeError('service startup timed out')
            output=[]
            for row in rows:
                req=urllib.request.Request(url+'/quotes',data=json.dumps(row['request']).encode(),headers={'Content-Type':'application/json'})
                try: res=urllib.request.urlopen(req,timeout=3)
                except urllib.error.HTTPError as e: res=e
                with res:
                    body=json.load(res)
                    # Error wording differs by framework; the accepted status is frozen.
                    output.append(dict(row,status=res.status,body=body if res.status==200 else None))
            return output,schema
        finally:
            proc.terminate()
            try: proc.wait(timeout=3)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait()

def main():
    p=argparse.ArgumentParser(); p.add_argument('workspace');p.add_argument('python');p.add_argument('--freeze',action='store_true');p.add_argument('--hook',action='store_true');args=p.parse_args()
    args.workspace=str(Path(args.workspace).resolve())
    args.python=str(Path(args.python).absolute())
    frozen=HERE/'contract.json'
    rows=cases() if args.freeze else json.loads(frozen.read_text())
    try:
        actual,schema=replay(args.workspace,args.python,rows)
        if args.freeze:
            assert not frozen.exists(), 'contract already frozen'
            frozen.write_text(json.dumps(actual,indent=2)+'\n');(HERE/'old-openapi.json').write_text(json.dumps(schema,indent=2)+'\n')
            print('FROZEN',len(actual),'HTTP cases');return
        failures=[]
        for expected,got in zip(rows,actual):
            # JSON encoding keeps number vs string distinction; int/float numeric equivalence is accepted.
            if expected['status']!=got['status'] or expected['body']!=got['body']:
                failures.append(f"{expected['name']}: expected HTTP {expected['status']} {json.dumps(expected['body'],sort_keys=True)}; got HTTP {got['status']} {json.dumps(got['body'],sort_keys=True)}")
        source=(Path(args.workspace)/'app.py').read_text()
        if 'pydantic.v1' in source: failures.append('native-v2 requirement violated: pydantic.v1 import')
        # Version and deprecated API checks are required only for candidate verification.
        if os.environ.get('REQUIRE_V2')=='1':
            version=subprocess.check_output([args.python,'-c','import pydantic; print(pydantic.__version__)'],text=True).strip()
            if version!='2.11.7': failures.append('expected pydantic 2.11.7; got '+version)
            if '@validator(' in source or 'class Config:' in source: failures.append('deprecated v1 validator/config API remains')
        if failures:
            message=f"API compatibility FAIL: {len(failures)} mismatch(es) across {len(rows)} frozen requests.\n"+'\n'.join(failures)
            if args.hook:
                print(json.dumps({'decision':'deny','reason':'Frozen API compatibility checks failed','additionalContext':message}))
            else: print(message)
            sys.exit(0 if args.hook else 1)
        print(json.dumps({'decision':'allow','reason':f'API compatibility PASS: {len(rows)} frozen requests'}) if args.hook else f'API compatibility PASS: {len(rows)} frozen requests')
    except Exception as exc:
        # Hook infrastructure failure must block, not silently fall open.
        print('Verifier execution error: '+str(exc),file=sys.stderr);sys.exit(2 if args.hook else 1)

if __name__=='__main__': main()
