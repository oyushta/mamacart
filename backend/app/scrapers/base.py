"""Interface every store scraper implements."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..matching import Product


class Scraper(ABC):
    #: Human-readable store name shown in results.
    store_name: str = "unknown"

    @abstractmethod
    def search(self, query: str) -> list[Product]:
        """Return current products for a free-text query.

        Implementations should respect the store's terms and robots rules,
        rate-limit requests, and raise on hard failures rather than returning
        partial data silently.
        """
