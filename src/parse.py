from __future__ import annotations
rows: List[Dict] = []
for i in range(count):
el = cards.nth(i)
asin = await el.get_attribute('data-asin') or ''
# title nodes are inconsistent; try several
title = await _first_text(el, [
'h2 a span', 'h2', 'h3 a span', 'h3', '[data-csa-c-type="title"]', 'span.a-size-medium']
) or ''
url = await _first_attr(el, ['h2 a', 'h3 a', 'a.a-link-normal', 'a'], 'href') or ''
price_text = await _first_text(el, ['span.a-price > span.a-offscreen', '[class*="price"]', '.p13n-sc-price'])
rating_aria = await _first_attr(el, ['i.a-icon-star-small','i.a-icon-star','span.a-icon-alt'], 'aria-label')
reviews_aria = await _first_attr(el, ['[aria-label$="ratings"]','[aria-label$="rating"]','.a-size-small .a-link-normal'], 'aria-label')


rows.append({
'rank': i+1,
'asin': asin.strip(),
'title': title.strip(),
'url': await _normalize_url(page, url),
'price': _to_price(price_text),
'rating': _to_float(rating_aria),
'reviews_count': _to_int(reviews_aria),
'badge': await _first_text(el, ['span.p13n-best-seller-badge','span[title*="Best Seller"]']) or None,
})
return rows


async def _first_text(scope, selectors: List[str]) -> Optional[str]:
for s in selectors:
loc = scope.locator(s)
if await loc.count():
t = await loc.first.text_content()
if t: return t
return None


async def _first_attr(scope, selectors: List[str], name: str) -> Optional[str]:
for s in selectors:
loc = scope.locator(s)
if await loc.count():
v = await loc.first.get_attribute(name)
if v: return v
return None


async def _normalize_url(page: Page, href: str | None) -> str:
if not href: return ''
if href.startswith('http'): return href
try:
base = page.url
from urllib.parse import urljoin
return urljoin(base, href)
except Exception:
return href


_def_float = re.compile(r"([0-9]+(?:\.[0-9]+)?)")


def _to_price(t: Optional[str]):
if not t: return None
s = ''.join(ch for ch in t if ch.isdigit() or ch == '.')
return float(s) if s else None


def _to_float(t: Optional[str]):
if not t: return None
m = _def_float.search(t)
return float(m.group(1)) if m else None


def _to_int(t: Optional[str]):
if not t: return None
digits = ''.join(ch for ch in t if ch.isdigit())
return int(digits) if digits else None
