"""Pack-size parsing, unit-price normalisation, fuzzy matching and ranking."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher

# Base units: grams for mass, millilitres for volume, count for items.
_UNIT_FACTORS = {
    "kg": ("g", 1000.0),
    "g": ("g", 1.0),
    "l": ("ml", 1000.0),
    "litre": ("ml", 1000.0),
    "liter": ("ml", 1000.0),
    "ml": ("ml", 1.0),
    "cl": ("ml", 10.0),
}

_SIZE_RE = re.compile(
    r"(?:(\d+)\s*x\s*)?(\d+(?:\.\d+)?)\s*(kg|g|ml|cl|litre|liter|l)\b",
    re.IGNORECASE,
)


@dataclass
class Product:
    store: str
    name: str
    price: float
    url: str = ""
    brand: str = ""
    own_brand: bool = False
    unit_price: float | None = field(default=None, init=False)
    unit_label: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.unit_price, self.unit_label = unit_price(self.name, self.price)


def parse_size(text: str) -> tuple[float, str] | None:
    """Return (quantity, base_unit) for a size such as '2L' or '6 x 250ml'.

    base_unit is 'g' or 'ml'. Returns None if no size is found.
    """
    match = _SIZE_RE.search(text)
    if not match:
        return None
    count = int(match.group(1)) if match.group(1) else 1
    amount = float(match.group(2))
    base, factor = _UNIT_FACTORS[match.group(3).lower()]
    return count * amount * factor, base


def unit_price(name: str, price: float) -> tuple[float | None, str]:
    """Price per kg (for mass) or per litre (for volume), or None if unknown."""
    parsed = parse_size(name)
    if parsed is None or parsed[0] <= 0:
        return None, ""
    quantity, base = parsed
    if base == "g":
        return price / (quantity / 1000.0), "per kg"
    return price / (quantity / 1000.0), "per litre"


def similarity(a: str, b: str) -> float:
    """Rough name similarity in [0, 1], ignoring case and size tokens."""
    def clean(s: str) -> str:
        s = _SIZE_RE.sub(" ", s.lower())
        return re.sub(r"[^a-z0-9 ]+", " ", s).split()

    tokens_a, tokens_b = clean(a), clean(b)
    if not tokens_a or not tokens_b:
        return 0.0
    set_a, set_b = set(tokens_a), set(tokens_b)
    jaccard = len(set_a & set_b) / len(set_a | set_b)
    seq = SequenceMatcher(None, " ".join(tokens_a), " ".join(tokens_b)).ratio()
    return 0.6 * jaccard + 0.4 * seq


def search(query: str, products: list[Product], min_score: float = 0.35) -> dict:
    """Return the cheapest-first matches for a query, plus cheaper alternatives.

    'matches' are the products whose names are similar enough to the query,
    sorted by unit price (falling back to shelf price when no size is known).
    'alternatives' are own-brand items among the matches that are cheaper than
    the cheapest exact-looking match.
    """
    scored = [(similarity(query, p.name), p) for p in products]
    matches = [p for score, p in scored if score >= min_score]

    def sort_key(p: Product) -> tuple[float, float]:
        primary = p.unit_price if p.unit_price is not None else float("inf")
        return (primary, p.price)

    matches.sort(key=sort_key)
    alternatives: list[Product] = []
    if matches:
        baseline = matches[0].price
        alternatives = [p for p in matches[1:] if p.own_brand and p.price < baseline]

    return {
        "query": query,
        "matches": [_as_dict(p) for p in matches],
        "alternatives": [_as_dict(p) for p in alternatives],
    }


def _as_dict(p: Product) -> dict:
    return {
        "store": p.store,
        "name": p.name,
        "price": round(p.price, 2),
        "unit_price": round(p.unit_price, 2) if p.unit_price is not None else None,
        "unit_label": p.unit_label,
        "url": p.url,
        "own_brand": p.own_brand,
    }
