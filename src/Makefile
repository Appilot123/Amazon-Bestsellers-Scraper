.PHONY: setup crawl demo fmt


setup:
python -m pip install -r requirements.txt
python -m playwright install chromium


crawl:
python src/scraper.py --category-url "https://www.amazon.com/Best-Sellers/zgbs/electronics" --limit 100 --out data/out/electronics.csv


demo:
python src/scraper.py --input-file examples/categories.txt --limit 50 --out data/out/bestsellers.json


fmt:
python -m pip install pyflakes >/dev/null 2>&1 || true
pyflakes src || true
