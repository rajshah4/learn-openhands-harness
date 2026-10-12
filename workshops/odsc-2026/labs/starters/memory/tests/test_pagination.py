import pytest

from toyapp.pagination import page_numbers, paginate


def test_page_number_api_remains_one_based() -> None:
    assert paginate(["a", "b", "c"], page=1, per_page=2).items == ["a", "b"]
    assert paginate(["a", "b", "c"], page=2, per_page=2).items == ["c"]


def test_page_number_validation_is_preserved() -> None:
    with pytest.raises(ValueError):
        paginate(["a"], page=0, per_page=1)
    assert page_numbers(5, 2) == [1, 2, 3]
