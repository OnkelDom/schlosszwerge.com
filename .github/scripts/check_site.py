"""Dependency-free checks for the buildless HTML5 website."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[2]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
MENU = ["/", "/aktuelles/", "/einrichtung/team/", "/karriere/", "/unsfinden/", "/anmeldung/"]
TOPICS = ["konzept", "team", "tagesablauf", "oeffnungszeiten", "raeumlichkeiten", "gewaltschutzkonzept", "finanzen", "vereinsgeschichte"]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.errors = []
        self.stack = []
        self.headings = 0
        self.mains = 0
        self.menu = []
        self.in_menu = False
        self.feed(source)
        self.close()
        if self.stack:
            self.errors.append(f"Unclosed elements: {self.stack}")

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if name in attrs:
                self.links.append(attrs[name])
        if tag == "nav" and attrs.get("id") == "hauptmenue":
            self.in_menu = True
        if tag == "a" and self.in_menu:
            self.menu.append(attrs.get("href"))
        if tag == "h1":
            self.headings += 1
        if tag == "main":
            self.mains += 1
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image without alt attribute")
        if tag == "html" and attrs.get("lang") != "de":
            self.errors.append("Missing German document language")

    def handle_endtag(self, tag):
        if tag in VOID:
            self.errors.append(f"Void element has closing tag: {tag}")
        elif not self.stack or self.stack[-1] != tag:
            self.errors.append(f"Unexpected closing tag: {tag}; open: {self.stack[-3:]}")
        else:
            self.stack.pop()
        if tag == "nav":
            self.in_menu = False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)


errors = []
sources = {path: path.read_text() for path in ROOT.rglob("*.html") if not path.is_relative_to(ROOT / ".preview-site")}
pages = {path: Page(source) for path, source in sources.items()}
for path, page in pages.items():
    source = sources[path]
    label = path.relative_to(ROOT).as_posix()
    errors.extend(f"{label}: {error}" for error in page.errors)
    redirect = label == "einrichtung/index.html"
    if not source.lower().startswith("<!doctype html>"):
        errors.append(f"{label}: missing HTML5 doctype")
    if not redirect:
        if page.menu != MENU:
            errors.append(f"{label}: inconsistent main navigation")
        if page.headings != 1 or page.mains != 1:
            errors.append(f"{label}: expected one h1 and one main element")
        if "/assets/css/main.css" not in page.links or "/assets/js/site.js" not in page.links:
            errors.append(f"{label}: missing shared CSS or navigation script")
        if not {"/impressum/", "/datenschutz/"}.issubset(page.links):
            errors.append(f"{label}: missing legal links")
        if label not in {"index.html", "404.html", "impressum/index.html", "datenschutz/index.html"}:
            for topic in TOPICS:
                if f"/einrichtung/{topic}/" not in page.links:
                    errors.append(f"{label}: missing topic {topic}")
    if "[...]" in source:
        errors.append(f"{label}: truncated content found")
    for link in page.links:
        url = urlsplit(link)
        if url.scheme in {"mailto", "tel"}:
            continue
        if url.netloc and url.hostname != "schlosszwerge.com":
            continue
        if url.scheme and url.scheme not in {"http", "https"}:
            errors.append(f"{label}: unsupported URL {link}")
            continue
        if not url.path:
            target = path
        elif url.path.startswith("/"):
            target = ROOT / unquote(url.path).lstrip("/")
        else:
            target = path.parent / unquote(url.path)
        if target.is_dir():
            target /= "index.html"
        target = target.resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f"{label}: missing local target {link}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{label}: missing fragment {link}")

home = sources[ROOT / "index.html"]
for marker in ['id="einrichtung"', 'href="/anmeldung/"', 'href="/unsfinden/"', 'href="/einrichtung/gewaltschutzkonzept/"']:
    if marker not in home:
        errors.append(f"Homepage missing {marker}")
if 'content="0; url=/"' not in sources[ROOT / "einrichtung/index.html"]:
    errors.append("Legacy Einrichtung URL must lead to the homepage")
for name, minimum in {"anmeldung": 1200, "datenschutz": 5000, "impressum": 3000, "karriere": 300, "einrichtung/team": 1200, "einrichtung/konzept": 6000}.items():
    content = re.search(r'<!-- INHALT ANFANG:.*?-->(.*?)<!-- INHALT ENDE -->', sources[ROOT / name / "index.html"], re.S)
    if not content or len(content[1].strip()) < minimum:
        errors.append(f"{name}: full editorial content missing")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Validated {len(pages)} HTML5 pages: nesting, navigation, local targets, fragments, accessibility basics and editorial content.")
