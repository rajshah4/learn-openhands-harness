import pytest
from toyapp.exporter import export_all
from toyapp.pagination import ExportWindow, export_window
from toyapp.tokens import decode_offset, encode_offset


def test_export_resumes_and_preserves_order():
    assert export_all(list(range(7)), 2) == list(range(7))
    first = export_window(["a", "b", "c"], limit=2)
    assert isinstance(first, ExportWindow)
    assert first.resume_token == encode_offset(2)
    assert export_window(["a", "b", "c"], first.resume_token, 2).records == ["c"]


def test_empty_export_and_bounds():
    assert export_all([], 2) == []
    assert export_window([1], encode_offset(100), 2) == ExportWindow([], None)
    with pytest.raises(ValueError):
        export_all([1], 0)


@pytest.mark.parametrize("cursor", ["2", "%%%", "djE6MA", "djI6LTE", "djI6Mg==", "djI6MDA"])
def test_shared_token_validation(cursor):
    with pytest.raises(ValueError):
        decode_offset(cursor)
