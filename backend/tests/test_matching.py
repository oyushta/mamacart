from app.matching import Product, parse_size, search, unit_price


def test_parse_size_litres_and_grams():
    assert parse_size("Semi-skimmed milk 2L") == (2000.0, "ml")
    assert parse_size("Butter 500g") == (500.0, "g")


def test_parse_size_multipack():
    assert parse_size("Cola 6 x 250ml") == (1500.0, "ml")


def test_parse_size_missing():
    assert parse_size("Bread") is None


def test_unit_price_per_litre():
    price, label = unit_price("Milk 2L", 2.00)
    assert round(price, 2) == 1.00
    assert label == "per litre"


def test_unit_price_per_kg():
    price, label = unit_price("Butter 500g", 3.00)
    assert round(price, 2) == 6.00
    assert label == "per kg"


def test_search_sorts_by_unit_price_and_flags_alternatives():
    products = [
        Product("A", "Semi-skimmed milk 2L", 2.40),
        Product("B", "Own brand semi-skimmed milk 2L", 1.60, own_brand=True),
        Product("C", "Semi-skimmed milk 4L", 3.00),
        Product("D", "Dish soap 500ml", 1.00),
    ]
    result = search("semi-skimmed milk", products)
    names = [m["name"] for m in result["matches"]]
    assert "Dish soap 500ml" not in names
    assert result["matches"][0]["store"] == "C"  # 0.75/L beats 0.80/L and 1.20/L
    assert [a["store"] for a in result["alternatives"]] == ["B"]
