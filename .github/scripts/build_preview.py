"""Package the review site with indexing disabled; production sources stay unchanged."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
ROBOTS = "noindex, nofollow, noarchive, nosnippet"


class References(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.urls = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("src", "href"):
            if name in attrs:
                self.urls.append(attrs[name])


def build(destination, base_url):
    url = urlsplit(base_url)
    if url.scheme != "https" or not url.hostname or url.path not in ("", "/") or url.query or url.fragment or url.username or url.password:
        raise ValueError("Preview URL must be an HTTPS origin without credentials or a path")
    if not re.fullmatch(r"[a-z0-9.-]+", url.hostname):
        raise ValueError("Invalid preview hostname")
    destination = destination.resolve()
    if destination == ROOT or destination in ROOT.parents:
        raise ValueError("Output cannot replace the repository or a parent directory")
    if destination.exists():
        if not (destination / ".preview-build").is_file():
            raise ValueError("Refusing to replace a directory without our build marker")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    (destination / ".preview-build").write_text("Generated preview; not a production source directory.\n")
    source_pages = sorted(path for path in ROOT.rglob("*.html") if not path.is_relative_to(destination) and not path.is_relative_to(ROOT / ".preview-site") and ".git" not in path.parts)
    files = set(source_pages)
    for path in source_pages:
        for reference in References(path.read_text()).urls:
            target = urlsplit(reference)
            if target.scheme or target.netloc or not target.path:
                continue
            local = ROOT / unquote(target.path).lstrip("/") if target.path.startswith("/") else path.parent / unquote(target.path)
            if local.is_dir():
                local /= "index.html"
            local = local.resolve()
            if not local.is_relative_to(ROOT) or not local.is_file():
                raise ValueError(f"Invalid local asset: {reference}")
            files.add(local)
    for path in sorted(files):
        relative = path.relative_to(ROOT)
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".html":
            content = path.read_text()
            content = re.sub(r'\s*<link\b[^>]*rel="canonical"[^>]*>', "", content)
            content = content.replace("</head>", f'  <meta name="robots" content="{ROBOTS}">\n</head>')
            banner = '<div class="preview-banner">Website-Entwurf zur gemeinsamen Abstimmung</div>'
            content = content.replace("<body>", "<body>\n  " + banner, 1)
            output.write_text(content)
        else:
            shutil.copy2(path, output)
    css = destination / "assets/css/main.css"
    with css.open("a") as handle:
        handle.write('\n/* Nur im Vorschaupaket: klare Kennzeichnung des unveröffentlichten Entwurfs. */\n.preview-banner { padding: 7px 20px; background: #193e4b; color: white; text-align: center; font: 500 .8rem/1.5 "Segoe UI", Arial, sans-serif; }\n')
    (destination / "robots.txt").write_text("User-agent: *\nAllow: /\n\n# Crawling is allowed so search engines can read noindex in HTTP headers and HTML.\n# This preview intentionally has no sitemap.\n")
    (destination / ".htaccess").write_text(f'''Options -Indexes
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
  Header always set X-Robots-Tag "{ROBOTS}"
  Header always set Referrer-Policy "no-referrer"
</IfModule>
RewriteEngine On
RewriteCond %{{HTTPS}} !=on
RewriteCond %{{REQUEST_URI}} !^/\\.well-known/acme-challenge/
RewriteRule ^ https://{url.hostname}%{{REQUEST_URI}} [R=302,L,NE]
''')
    print(f"Packaged {len(source_pages)} HTML pages and {len(files) - len(source_pages)} referenced assets for {base_url}")
    print(f"Preview directory: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".preview-site")
    parser.add_argument("--base-url", default="https://dev.schlosszwerge.com")
    args = parser.parse_args()
    build(args.output, args.base_url)
