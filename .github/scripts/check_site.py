"""Check navigation, restored content and local assets before deployment."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[2]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append(attrs[name])


errors = []
sources = {path: path.read_text() for path in ROOT.rglob("*.html")}
pages = {path: Page(source) for path, source in sources.items()}
menu = ["/einrichtung/", "/aktuelles/", "/anmeldung/", "/karriere/", "/impressum/", "/datenschutz/"]
for path, page in pages.items():
    source = sources[path]
    label = path.relative_to(ROOT)
    nav = re.search(r'<ul class="visible-links">(.*?)</ul>', source, re.S)
    if not nav or re.findall(r'href="([^"]+)"', nav[1]) != menu:
        errors.append(f"{label}: inconsistent main navigation")
    if "/assets/css/main.css" not in page.links or "/assets/js/main.min.js" not in page.links:
        errors.append(f"{label}: missing site layout assets")
    if 'class="nav__items"' in source and "/einrichtung/konzept/" in page.links:
        if "/einrichtung/gewaltschutzkonzept/" not in page.links:
            errors.append(f"{label}: missing Gewaltschutzkonzept navigation")
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = ROOT / unquote(url.path).lstrip("/") if url.path.startswith("/") else path.parent / unquote(url.path)
        if not url.path:
            target = path
        elif target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            errors.append(f"{label}: missing target {link}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{label}: missing fragment {link}")

home = sources[ROOT / "index.html"]
facility = sources[ROOT / "einrichtung/index.html"]
if home != facility.replace("https://schlosszwerge.com/einrichtung/", "https://schlosszwerge.com/"):
    errors.append("Homepage must show Einrichtung content directly")
for name, minimum in {"anmeldung": 1000, "datenschutz": 1500, "impressum": 1000, "karriere": 300, "einrichtung/team": 1000}.items():
    content = re.search(r'<section[^>]*class="page__content[^"]*"[^>]*>(.*?)</section>', sources[ROOT / name / "index.html"], re.S)
    if not content or len(content[1].strip()) < minimum:
        errors.append(f"{name}: full page content missing")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(pages)} pages: navigation, local links/assets, restored content and Einrichtung homepage.")
