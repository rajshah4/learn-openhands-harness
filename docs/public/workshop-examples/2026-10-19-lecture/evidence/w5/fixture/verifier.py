"""Small controller-owned data check; no LLM and no candidate code execution."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def verify(workspace):
    workspace=Path(workspace)
    try:
        frozen=json.loads((ROOT/'source-hashes.json').read_text())
        unchanged=all(not (workspace/n).is_symlink() and hashlib.sha256((workspace/n).read_bytes()).hexdigest()==h for n,h in frozen.items())
        if not unchanged:raise ValueError('Source or handoff changed')
        with (workspace/'transactions.csv').open(newline='') as f:source=list(csv.DictReader(f))
        report=json.loads((workspace/'report.json').read_text())
        ids=report.get('record_ids');assert type(ids)==list and all(type(x)==str for x in ids),'record_ids must be a list of strings'
        expected_ids=[x['id'] for x in source];expected_total=sum(int(x['amount_cents']) for x in source)
        missing=sorted(set(expected_ids)-set(ids));extra=sorted(set(ids)-set(expected_ids));duplicates=sorted(x for x,count in Counter(ids).items() if count>1)
        total=report.get('total_cents')
        passed=not (missing or extra or duplicates) and type(total)==int and total==expected_total and report.get('status')=='complete'
        return {'pass':passed,'missing_record_ids':missing,'extra_record_ids':extra,'duplicate_record_ids':duplicates,'expected_total_cents':expected_total,'actual_total_cents':total,'source_records':len(source),'report_records':len(ids),'source_unchanged':unchanged,'report_status':report.get('status')}
    except Exception as e:return {'pass':False,'error':type(e).__name__+': '+str(e)}

if __name__=='__main__':
    import sys
    result=verify(sys.argv[1]);print(json.dumps(result,indent=2));sys.exit(0 if result['pass'] else 1)
