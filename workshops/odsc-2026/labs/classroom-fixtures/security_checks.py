import importlib.util
import json
from pathlib import Path
import tempfile
import copy
import sys
import hmac
import hashlib

def load(path):
    spec=importlib.util.spec_from_file_location('subject',path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def same(a,b):
    assert a==b, f'{a!r} != {b!r}'
def raises(fn, typ=ValueError):
    try: fn()
    except typ: return
    raise AssertionError('expected '+typ.__name__)
def security(m):
    db=m.database()
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)/'exports'; root.mkdir()
        other=Path(d)/'exports-old'; other.mkdir()
        (root/'ok').write_text('OK'); (other/'private').write_text('PRIVATE')
        (root/'escape').symlink_to(other/'private')
        (root/'internal').symlink_to(root/'ok')
        (root/'nested').mkdir(); (root/'nested'/'ok').write_text('NESTED')
        cases={
          'sql_title':lambda:same(m.search(db,'alice',"x' OR 1=1 --"),[]),
          'sql_owner':lambda:same(m.search(db,"x' OR 1=1 --",'private'),[]),
          'sql_valid':lambda:same(m.search(db,'alice','public'),[(1,'public')]),
          'idor_other':lambda:same(m.read_doc(db,'alice',2),None),
          'idor_own':lambda:same(m.read_doc(db,'bob',2),('private',)),
          'idor_missing':lambda:same(m.read_doc(db,'alice',999),None),
          'path_sibling':lambda:raises(lambda:m.read_export(root,'../exports-old/private'),PermissionError),
          'path_symlink':lambda:raises(lambda:m.read_export(root,'escape'),PermissionError),
          'path_contract':lambda:(raises(lambda:m.read_export(root,str(root/'ok')),PermissionError),same(m.read_export(root,'internal'),'OK'),same(m.read_export(root,'ok'),'OK'),same(m.read_export(root,'nested/ok'),'NESTED')),
          'safe_regression':lambda:(same(m.safe_lookup(db,'alice',"x' OR 1=1 --"),[]),same(m.verify_signature(b'key',b'data','bad'),False),same(m.verify_signature(b'key',b'data',hmac.new(b'key',b'data',hashlib.sha256).hexdigest()),True))}
        return run_cases(cases)
def event(i,seq,kind='credit',account='a',**kw):
    return dict(id=i,seq=seq,kind=kind,account=account) | ({'cents':10} if kind!='reverse' else {}) | kw
def ledger(m):
    c=event('c',1); d=event('d',2,'debit',cents=3); r=event('r',3,'reverse',target='d')
    def valid(es,total):
        before=copy.deepcopy(es);same(m.balance(es,'a'),total);same(es,before)
    def invalid(es): raises(lambda:m.balance(es,'a'))
    return run_cases({
      'ordinary':lambda:(valid([],0),valid([c,d],7),valid([event('b',4,account='b')],0)),
      'order_reverse':lambda:(valid([r,d,c],10),valid([event('r',2,'reverse',target='c'),c],0)),
      'retry':lambda:valid([c,dict(c),d],7),
      'conflict':lambda:invalid([c,event('c',2,cents=9)]),
      'other_account_conflict':lambda:invalid([c,event('c',2,account='b')]),
      'cents_validation':lambda:[invalid([event('bad',1,cents=v)]) for v in (-1,True,1.5,'10')],
      'duplicate_seq':lambda:invalid([c,event('d',1)]),
      'unknown_kind_other_account':lambda:invalid([event('b',1,'other',account='b')]),
      'missing_or_later_target':lambda:(invalid([event('r',1,'reverse',target='x')]),invalid([event('r',1,'reverse',target='c'),event('c',2)])),
      'cross_account_target':lambda:invalid([c,event('r',2,'reverse',account='b',target='c')]),
      'double_reverse':lambda:invalid([c,event('r',2,'reverse',target='c'),event('r2',3,'reverse',target='c')]),
      'reverse_reverse':lambda:invalid([c,event('r',2,'reverse',target='c'),event('r2',3,'reverse',target='r')])})
def run_cases(cases):
    rows=[]
    for name,fn in cases.items():
        try: fn();rows.append({'name':name,'pass':True})
        except Exception as ex: rows.append({'name':name,'pass':False,'error':type(ex).__name__+': '+str(ex)})
    return {'passed':sum(r['pass'] for r in rows),'total':len(rows),'checks':rows}
if __name__=='__main__':
    kind,workspace=sys.argv[1:3]
    try: result=globals()[kind](load(Path(workspace)/('service.py' if kind=='security' else 'ledger.py')))
    except Exception as ex: result={'passed':0,'total':10 if kind=='security' else 12,'error':repr(ex)}
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['passed']==result['total'] else 1)
