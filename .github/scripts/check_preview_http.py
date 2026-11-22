"""Verify that the hosted decision preview works without authentication and rejects indexing."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]


class RobotsMeta(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.noindex = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.noindex = "noindex" in attrs.get("content", "").lower().split(", ")


def verify(base_url):
    base_url = base_url.rstrip("/")
    if not base_url.startswith("https://"):
        raise ValueError("Preview must use HTTPS")
    sources = [path for path in ROOT.rglob("*.html") if not path.is_relative_to(ROOT / ".preview-site") and not path.is_relative_to(ROOT / ".site-build") and ".git" not in path.parts]
    routes = ["/" if p == ROOT / "index.html" else "/" + p.relative_to(ROOT).as_posix().removesuffix("index.html") for p in sources]
    routes += ["/assets/css/main.css", "/assets/js/site.js", "/assets/pdf/Gewaltschutzkonzept.pdf", "/robots.txt"]

    def check(route, expected=200):
        try:
            response = urlopen(Request(base_url + route, headers={"Cache-Control": "no-cache"}), timeout=30)
        except HTTPError as error:
            response = error
        with response:
            assert response.status == expected, f"{route}: HTTP {response.status}, expected {expected}"
            assert response.url.startswith(base_url + "/"), f"{route}: unexpected redirect {response.url}"
            assert "noindex" in response.headers.get("X-Robots-Tag", "").lower(), f"{route}: missing X-Robots-Tag noindex"
            assert not response.headers.get("WWW-Authenticate"), f"{route}: unexpected password protection"
            body = response.read()
            if "text/html" in response.headers.get("Content-Type", ""):
                assert RobotsMeta(body.decode("utf-8")).noindex, f"{route}: missing HTML robots noindex"
        return route

    with ThreadPoolExecutor(max_workers=5) as pool:
        checked = list(pool.map(check, routes))
    check("/this-preview-page-does-not-exist/", 404)
    try:
        urlopen(base_url + "/sitemap.xml", timeout=20)
    except HTTPError as error:
        assert error.code == 404, "Unexpected sitemap response"
    else:
        raise AssertionError("Preview must not publish a sitemap")
    print(f"Verified {len(checked)} pages/assets plus 404: trusted HTTPS, no password, HTTP/HTML noindex; no sitemap.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://dev.schlosszwerge.com")
    verify(parser.parse_args().base_url)
