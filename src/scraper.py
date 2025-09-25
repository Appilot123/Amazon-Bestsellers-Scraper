from __future__ import annotations
from storage import write_rows


BANNER = """
Amazon Bestsellers Scraper — research/analytics tool
Respect Amazon ToS and local laws. Use low concurrency and delays.
"""


async def fetch_category(url: str) -> List[Dict]:
async with async_playwright() as pw:
launch_args = {"headless": SETTINGS.headless}
if SETTINGS.proxy:
launch_args["proxy"] = {"server": SETTINGS.proxy}
browser = await pw.chromium.launch(**launch_args)
context = await browser.new_context(
user_agent=SETTINGS.user_agent,
viewport={"width": 1366, "height": 900},
)
page = await context.new_page()
await page.goto(url, wait_until="domcontentloaded")
await page.wait_for_timeout(1000)
items = await parse_list_items(page)
# annotate
for r in items:
r["category"] = url
r["timestamp"] = datetime.utcnow().isoformat()
await browser.close()
return items


async def run(urls: List[str], out: str, limit: int | None) -> None:
all_rows: List[Dict] = []
for i, url in enumerate(urls):
print(f"[ {i+1}/{len(urls)} ] {url}")
rows = await fetch_category(url)
if limit: rows = rows[:limit]
print(f" → {len(rows)} rows")
all_rows.extend(rows)
# polite delay
await asyncio.sleep(max(0.2, SETTINGS.rate_delay_ms / 1000))
write_rows(all_rows, out)
print(f"Saved {len(all_rows)} rows → {out}")


def load_urls(args) -> List[str]:
urls: List[str] = []
if args.category_url:
urls.append(args.category_url)
if args.input_file:
with open(args.input_file, "r", encoding="utf-8") as f:
for line in f:
line = line.strip()
if line and not line.startswith('#'):
urls.append(line)
return urls


if __name__ == "__main__":
p = argparse.ArgumentParser(description=BANNER)
p.add_argument("--category-url", help="Single Best Sellers category URL")
p.add_argument("--input-file", help="File with category URLs (one per line)")
p.add_argument("--limit", type=int, default=None, help="Max items per category")
p.add_argument("--out", required=True, help="Output path: .csv | .json | .sqlite")
args = p.parse_args()


urls = load_urls(args)
if not urls:
print("Provide --category-url or --input-file", file=sys.stderr)
sys.exit(1)


asyncio.run(run(urls, args.out, args.limit))
