# MamaCart

A grocery price-comparison tool for home delivery. Search for a product and see matching items across supermarkets, ranked from cheapest to most expensive per unit, with cheaper alternatives listed alongside.

## Status

Starter project. The matching logic and search API work; the store scrapers are stubs to be filled in.

## Layout

```
backend/
  app/
    main.py            FastAPI app and /search endpoint
    matching.py        Pack-size parsing, unit-price normalisation, fuzzy matching, ranking
    scrapers/
      base.py          Scraper interface
      store_a.py       Example stub for one store
    static/
      index.html       Basic search page
  tests/
    test_matching.py
```

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the search page, or call `GET /search?q=milk` directly.

## Tests

```bash
cd backend
pytest
```

## Next steps

1. Pick 2–3 stores that deliver to your address and check their terms before scraping.
2. Implement each scraper in `app/scrapers/` against the `Scraper` interface.
3. Store prices with timestamps so you can track changes over time.
4. Add basket optimisation: cheapest single store and cheapest split, including delivery fees.
