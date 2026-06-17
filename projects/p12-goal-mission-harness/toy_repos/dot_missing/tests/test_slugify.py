from slugify import slugify


def test_basic_slugify():
    assert slugify("Hello World!") == "hello-world"


def test_special_characters():
    assert slugify("Special @#$% Characters!") == "special-characters"


def test_unicode_handling():
    assert slugify("Café déjà vu!") == "cafe-deja-vu"


def test_german_characters():
    assert slugify("Straße der Erinnerung") == "strasse-der-erinnerung"


def test_empty_and_edge_cases():
    assert slugify("") == ""
    assert slugify(None) == ""
