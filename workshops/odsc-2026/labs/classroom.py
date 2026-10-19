#!/usr/bin/env python3
"""Prepare selected classroom fixtures and check them without model calls."""
import argparse,json,os,shutil,subprocess,sys,tempfile,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'classroom-fixtures'
CASES=json.loads((DATA/'cases.json').read_text())
def prompt(case):return CASES[case]['prompt']
def prepare(case,workspace):
 workspace=workspace.resolve()
 if workspace.exists():raise ValueError('Workspace already exists; choose a new path.')
 if ROOT in workspace.parents or workspace==ROOT:raise ValueError('Choose a workspace outside the lab package.')
 shutil.copytree(DATA/'starters'/CASES[case]['starter'],workspace)
 (workspace/'.gitignore').write_text('__pycache__/\n*.pyc\n')
 for cmd in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Workshop baseline','-c','user.email=workshop@example.invalid','-c','commit.gpgsign=false','commit','-qm','Prepared classroom baseline']]:subprocess.run(cmd,cwd=workspace,check=True)
 print('Prepared '+str(workspace)+'\n\n'+prompt(case))
def check(case,workspace):
 workspace=workspace.resolve();kind=CASES[case]['checker']
 if kind=='checkpoint':
  spec=importlib.util.spec_from_file_location('checkpoint_checks',DATA/'checkpoint_checks.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.check(workspace)
 if kind=='security':
  spec=importlib.util.spec_from_file_location('security_checks',DATA/'security_checks.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);r=m.security(m.load(workspace/'service.py'));return dict(r,**{'pass':r['passed']==r['total']})
 if kind=='agreement':
  code="import csv,io;from exporter import export_rows;x=[{'customer_id':'0012','region':None},{'customer_id':'0070'},{'customer_id':'0003','region':''},{'customer_id':'0004','region':'EU'}];assert list(csv.reader(io.StringIO(export_rows(x))))==[['customer_id','region'],['0012','NA'],['0070','NA'],['0003',''],['0004','EU']]"
  checks={'accepted_agreement':code};imports=''
 else:
  data=json.loads((DATA/'w6_checks.json').read_text())[kind];checks=data['checks'];imports=data['imports']
 results={}
 for name,code in checks.items():
  p=subprocess.run([sys.executable,'-c',imports+'\n'+code],cwd=workspace,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=20)
  results[name]={'pass':p.returncode==0,'stdout':p.stdout,'stderr':p.stderr}
 return {'pass':all(x['pass'] for x in results.values()),'checks':results}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','prompt','check']);p.add_argument('case',choices=CASES);p.add_argument('--workspace',type=Path);args=p.parse_args()
 if args.action=='prompt':print(prompt(args.case));return
 if args.workspace is None:p.error('--workspace is required')
 if args.action=='prepare':prepare(args.case,args.workspace)
 else:
  result=check(args.case,args.workspace);print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 1)
if __name__=='__main__':main()
