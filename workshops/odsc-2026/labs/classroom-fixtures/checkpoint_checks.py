"""Independent acceptance checker; stored outside all agent workspaces."""
import importlib.util,json,sys,tempfile,subprocess,os
from pathlib import Path

def check(workspace):
    workspace=Path(workspace)
    spec=importlib.util.spec_from_file_location('candidate_report',workspace/'report.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    rows=[]
    cases=[('mixed','id,amount,status\na,0.10,posted\nb,0.20,posted\na,0.10,posted\nc,10.00,pending\nd,-0.05,posted\n',{'total':'0.25','rows':3},{'included_ids':['a','b','d'],'excluded_pending_ids':['c'],'duplicate_ids':['a'],'total':'0.25'}),
    ('empty','id,amount,status\n',{'total':'0.00','rows':0},{'included_ids':[],'excluded_pending_ids':[],'duplicate_ids':[],'total':'0.00'}),
    ('pending-duplicate','id,amount,status\nz,100.00,pending\nz,100.00,pending\nx,12.34,posted\ny,-2.34,posted\n',{'total':'10.00','rows':2},{'included_ids':['x','y'],'excluded_pending_ids':['z'],'duplicate_ids':['z'],'total':'10.00'})]
    with tempfile.TemporaryDirectory(prefix='w5-independent-') as td:
        for name,csv,report,recon in cases:
            folder=Path(td)/name;folder.mkdir();src=folder/'input.csv';src.write_text(csv)
            error=None
            try:mod.build(src,folder/'report.json')
            except Exception as exc:error=repr(exc)
            for filename,expected in [('report.json',report),('reconciliation.json',recon)]:
                try:observed=json.loads((folder/filename).read_text())
                except Exception as exc:observed={'error':type(exc).__name__}
                rows.append({'case':name,'artifact':filename,'expected':expected,'observed':observed,'pass':error is None and observed==expected,'build_error':error})
        folder=Path(td)/'cli';folder.mkdir();(folder/'transactions.csv').write_text(cases[0][1])
        p=subprocess.run([sys.executable,str(workspace/'report.py')],cwd=folder,capture_output=True,text=True,timeout=20,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        for filename,expected in [('report.json',cases[0][2]),('reconciliation.json',cases[0][3])]:
            try:observed=json.loads((folder/filename).read_text())
            except Exception as exc:observed={'error':type(exc).__name__}
            rows.append({'case':'cli','artifact':filename,'expected':expected,'observed':observed,'pass':p.returncode==0 and observed==expected})
    return {'pass':all(x['pass'] for x in rows),'checks':rows}

if __name__=='__main__':
    result=check(sys.argv[1]);print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 1)
