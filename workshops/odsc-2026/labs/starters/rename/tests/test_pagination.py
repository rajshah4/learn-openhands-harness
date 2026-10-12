from toyapp.pagination import paginate


def test_first_page_includes_full_page() -> None:
    page = paginate(["a", "b", "c", "d"], page=1, per_page=2)
    assert page.items == ["a", "b"]


def test_second_page_includes_full_page() -> None:
    page = paginate(["a", "b", "c", "d"], page=2, per_page=2)
    assert page.items == ["c", "d"]


def test_last_page_can_be_partial() -> None:
    page = paginate(["a", "b", "c", "d", "e"], page=3, per_page=2)
    assert page.items == ["e"]
