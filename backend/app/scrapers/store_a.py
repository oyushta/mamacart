"""Stub scraper for one store. Replace the body with real fetching and parsing."""

from __future__ import annotations

from ..matching import Product
from .base import Scraper


class StoreA(Scraper):
    store_name = "Store A"

    def search(self, query: str) -> list[Product]:
        # TODO: request the store's search page or API for `query`,
        # parse name, price, URL and own-brand flag, and return Product objects.
        # Example shape:
        # return [Product(store=self.store_name, name="Semi-skimmed milk 2L",
        #                 price=1.45, url="https://...", own_brand=True)]
        return []
