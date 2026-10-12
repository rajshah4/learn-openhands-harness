from toyapp.catalog import browse


def test_direct_catalog_page():
    assert browse(["a", "b", "c"], page=2, per_page=2).items == ["c"]
