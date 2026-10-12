#!/usr/bin/env python3
"""Independent checks, outside agent workspaces; failures are reported by dimension."""
import argparse
import base64
import dataclasses
import importlib
import inspect
import json
import sys
from pathlib import Path


def token(offset):
    return base64.urlsafe_b64encode(f'v2:{offset}'.encode()).decode().rstrip('=')


def raises_value_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('expected ValueError')


def verify(repo):
    sys.path.insert(0, str(repo))
    p = importlib.import_module('toyapp.pagination')
    c = importlib.import_module('toyapp.catalog')
    e = importlib.import_module('toyapp.exporter')
    results = {}
    def check(name, fn):
        try:
            fn()
            results[name] = {'passed': True}
        except Exception as exc:
            results[name] = {'passed': False, 'detail': f'{type(exc).__name__}: {exc}'}
    def compatibility():
        assert c.browse([1,2,3], 2, 2).items == [3]
        assert p.paginate([1,2,3], 1, 2) == p.Page(1,2,3,2,[1,2])
        assert p.page_numbers(5,2) == [1,2,3]
        raises_value_error(lambda: p.paginate([1],0,1))
        raises_value_error(lambda: p.paginate([1],1,0))
        for n in range(10):
            assert e.export_all(list(range(n)), 3) == list(range(n))
        assert p.export_window([1],token(20),2).records == []
        raises_value_error(lambda: e.export_all([1],0))
    def architecture():
        assert dataclasses.is_dataclass(p.CursorPage)
        assert p.CursorPage.__dataclass_params__.frozen
        assert list(inspect.signature(p.paginate_cursor).parameters) == ['items','cursor','per_page']
        assert inspect.signature(p.paginate_cursor).parameters['per_page'].default == 20
        assert list(inspect.signature(c.browse_next).parameters) == ['items','cursor','per_page']
        assert c.browse_next([1,2,3],None,2) == p.paginate_cursor([1,2,3],None,2)
    def traversal():
        for n in range(11):
            for size in range(1,5):
                source = list(range(n)); before = source[:]; cursor = None; seen = []
                for _ in range(n+2):
                    page=p.paginate_cursor(source,cursor,size)
                    assert isinstance(page,p.CursorPage)
                    assert page.has_more is (page.next_cursor is not None)
                    seen.extend(page.items)
                    assert source == before
                    if page.next_cursor is None: break
                    assert page.next_cursor == token(len(seen))
                    cursor=page.next_cursor
                else: raise AssertionError('traversal did not terminate')
                assert seen == source
        assert p.paginate_cursor((3,1,2),None,2).items == [3,1]
        assert p.paginate_cursor([1],token(30),2).items == []
        assert p.paginate_cursor([1],token(30),2).next_cursor is None
    def validation():
        for bad in ['2','%%%','djE6MA','djI6LTE','djI6Mg==','djI6MDA','djI6Mg!','',token(2)+'=']:
            raises_value_error(lambda: p.paginate_cursor([1,2,3],bad,1))
        for size in [0,-1]:
            raises_value_error(lambda: p.paginate_cursor([1],None,size))
        result=p.paginate_cursor([1])
        try: result.has_more=True
        except dataclasses.FrozenInstanceError: pass
        else: raise AssertionError('mutable result')
    check('backwards_compatibility',compatibility)
    check('public_api_alignment',architecture)
    check('cursor_correctness',traversal)
    check('validation_and_frozen_result',validation)
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    try: result=verify(args.repo.resolve())
    except Exception as exc: result={'import':{'passed':False,'detail':f'{type(exc).__name__}: {exc}'}}
    print(json.dumps(result,indent=2))
    sys.exit(0 if all(x['passed'] for x in result.values()) else 1)
