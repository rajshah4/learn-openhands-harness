import csv,json
from decimal import Decimal
from pathlib import Path

def build(source,destination):
    posted={}
    with Path(source).open(newline='') as stream:
        for row in csv.DictReader(stream):
            if row['status']=='posted':
                posted.setdefault(row['id'],Decimal(row['amount']))
    total=sum(posted.values(),Decimal('0'))
    Path(destination).write_text(json.dumps({'total':f'{total:.2f}','rows':len(posted)}))
    # Checkpoint: reconciliation sidecar has not been implemented yet.

if __name__=='__main__':
    build('transactions.csv','report.json')
