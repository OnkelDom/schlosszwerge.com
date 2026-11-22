"""Render editorial Markdown into a separate directory of static website files."""

import argparse
from datetime import date
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[2]
PAGES = {
    "aktuelles": "aktuelles",
    "vereinsgeschichte": "einrichtung/vereinsgeschichte",
    "paedagogik": "einrichtung/konzept",
    "karriere": "karriere",
}
MARKER = "<!-- MARKDOWN-INHALT -->"
SITE_DIRECTORIES = (
    "aktuelles", "anmeldung", "assets", "categories", "datenschutz",
    "einrichtung", "impressum", "karriere", "unsfinden",
)
ROOT_FILE_TYPES = {".html", ".ico", ".png", ".txt", ".webmanifest", ".xml"}
ANCHOR = re.compile(r" \{#([\w-]+)\}$")
MARKDOWN = MarkdownIt("commonmark", {"html": False})


def allowed_link(url):
    return urlsplit(url).scheme in {"", "https", "http", "mailto", "tel"}


MARKDOWN.validateLink = allowed_link


def render(path, timeline=False, news=False):
    source = path.read_text(encoding="utf-8").strip()
    if not source:
        raise ValueError(f"{path.name}: Inhalt fehlt")
    tokens = MARKDOWN.parse(source)
    if news and (not tokens or tokens[0].tag != "h2"):
        raise ValueError(f"{path.name}: Meldung muss mit einer ## Überschrift beginnen")
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        if token.tag == "h1":
            raise ValueError(f"{path.name}: Bitte ## oder ### für Überschriften verwenden")
        title = tokens[index + 1]
        anchor = ANCHOR.search(title.content)
        if anchor:
            token.attrSet("id", anchor[1])
            title.children = MARKDOWN.parseInline(title.content[:anchor.start()])[0].children
    if timeline:
        for token in tokens:
            if token.type == "ordered_list_open" and token.level == 0:
                token.attrSet("class", "history-timeline")
    return MARKDOWN.renderer.render(tokens, MARKDOWN.options, {})


def render_news():
    articles = []
    for path in sorted((ROOT / "inhalte/meldungen").glob("*.md"), reverse=True):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md", path.name):
            raise ValueError(f"{path.name}: Erwartet wird JJJJ-MM-TT-kurzer-titel.md")
        published = date.fromisoformat(path.name[:10])
        articles.append(
            f'<article class="news-entry"><time datetime="{published}">'
            f'{published:%d.%m.%Y}</time>\n{render(path, news=True)}</article>'
        )
    return "\n".join(articles)


def build(output):
    output = output.resolve()
    # Never overwrite source files or an existing deployment directory.
    output.mkdir(parents=True, exist_ok=False)
    for name in SITE_DIRECTORIES:
        shutil.copytree(ROOT / name, output / name)
    for path in ROOT.iterdir():
        if path.is_file() and path.suffix in ROOT_FILE_TYPES:
            shutil.copy2(path, output / path.name)

    for name, route in PAGES.items():
        page = output / route / "index.html"
        template = page.read_text(encoding="utf-8")
        if template.count(MARKER) != 1:
            raise ValueError(f"{route}: exakt ein Platzhalter {MARKER} erforderlich")
        body = render(ROOT / "inhalte" / f"{name}.md", timeline=name == "vereinsgeschichte")
        if name == "aktuelles":
            body = render_news() + "\n" + body
        page.write_text(template.replace(MARKER, body.rstrip()), encoding="utf-8")
    print(f"Website gebaut: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    build(parser.parse_args().output)
