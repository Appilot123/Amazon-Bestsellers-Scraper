# Usage Examples


## Setup
```bash
python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```


## Single Category → CSV
```bash
python src/scraper.py \
--category-url "https://www.amazon.com/Best-Sellers/zgbs/electronics" \
--limit 100 \
--out data/out/electronics.csv
```


## Multiple Categories (file) → JSON
```bash
python src/scraper.py \
--input-file examples/categories.txt \
--limit 50 \
--out data/out/bestsellers.json
```


## SQLite Output
```bash
python src/scraper.py \
--category-url "https://www.amazon.com/Best-Sellers/zgbs/books" \
--limit 100 \
--out data/out/books.sqlite
```


## Notes
- Keep **A_MAX_CONCURRENCY=1** and generous delays to be respectful.
- Target only the **Best Sellers** category pages; do not fetch user data.
- Policies can change — review Amazon's ToS regularly.
