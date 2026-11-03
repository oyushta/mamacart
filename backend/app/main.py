"""FastAPI app: search endpoint and basic search page."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from .matching import search
from .scrapers.store_a import StoreA

app = FastAPI(title="MamaCart")
SCRAPERS = [StoreA()]
STATIC_DIR = Path(__file__).parent / "static"


def collect_products(query: str):
    products = []
    for scraper in SCRAPERS:
        try:
            products.extend(scraper.search(query))
        except Exception:  # one failing store should not break the whole search
            continue
    return products


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/search")
def search_products(q: str = Query(..., min_length=2, max_length=100)):
    return search(q, collect_products(q))
