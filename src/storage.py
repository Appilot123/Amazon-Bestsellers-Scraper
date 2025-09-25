from __future__ import annotations
import os, csv, json, sqlite3
from typing import List, Dict


def write_rows(rows: List[Dict], out: str) -> None:
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
if out.endswith(".csv"):
_to_csv(rows, out)
elif out.endswith(".json"):
with open(out, "w", encoding="utf-8") as f:
json.dump(rows, f, ensure_ascii=False, indent=2)
elif out.endswith(".sqlite"):
_to_sqlite(rows, out)
else:
raise ValueError("Output must be .csv | .json | .sqlite")


def _to_csv(rows: List[Dict], path: str) -> None:
if not rows:
open(path, "w").close(); return
keys = sorted({k for r in rows for k in r.keys()})
with open(path, "w", newline="", encoding="utf-8") as f:
w = csv.DictWriter(f, fieldnames=keys)
w.writeheader(); w.writerows(rows)


def _to_sqlite(rows: List[Dict], path: str) -> None:
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute(
"""
CREATE TABLE IF NOT EXISTS bestsellers (
rank INTEGER, title TEXT, asin TEXT, url TEXT,
price REAL, rating REAL, reviews_count INTEGER,
badge TEXT, category TEXT, timestamp TEXT
)
"""
)
cur.executemany(
"""
INSERT INTO bestsellers
(rank, title, asin, url, price, rating, reviews_count, badge, category, timestamp)
VALUES (:rank,:title,:asin,:url,:price,:rating,:reviews_count,:badge,:category,:timestamp)
""",
rows,
)
conn.commit(); conn.close()
