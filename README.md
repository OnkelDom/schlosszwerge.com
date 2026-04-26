# schlosszwerge.com

Website des Vereins `Die Schlosszwerge e.V.` fuer `schlosszwerge.com`.

Die Seite bleibt vorerst ein Jekyll-Projekt auf Basis von Minimal Mistakes. Inhaltliche Aenderungen erfolgen weiterhin ueber Markdown-Dateien und die vorhandene Navigation. Der Unterschied zur bisherigen GitHub-Pages-Auslieferung: GitHub Actions baut die Seite und deployed das generierte `_site/` per SFTP auf den Hetzner-Webspace.

## Architektur

- Quelle: GitHub Repository `OnkelDom/schlosszwerge.com`
- Branch: `master`
- Generator: Jekyll
- Theme: Minimal Mistakes
- Zielsystem: Hetzner Webspace per SFTP
- Zielpfad: Domain-Ordner `schlosszwerge.com`
- Deployment: `.github/workflows/deploy.yml`

## Inhalt bearbeiten

Neue oder bestehende Seiten liegen unter `_pages/`.

```bash
vim _pages/konzept.md
vim _pages/team.md
```

Navigation bearbeiten:

```bash
vim _data/navigation.yml
```

Aktuelles/Blogbeitraege liegen unter `_posts/`.

```bash
vim _posts/2026-01-01-beispiel.md
```

## Lokale Vorschau

Ruby und Bundler muessen lokal installiert sein.

```bash
bundle install
bundle exec jekyll serve
```

Danach im Browser:

```text
http://localhost:4000/
```

## Deployment

Der Deploy laeuft automatisch bei jedem Push auf `master`.

Manueller Start:

```bash
gh workflow run deploy.yml --repo OnkelDom/schlosszwerge.com --ref master
```

Status pruefen:

```bash
gh run list --repo OnkelDom/schlosszwerge.com --limit 5
```

## GitHub Secrets

Der Workflow erwartet folgende Repository-Secrets:

```text
HETZNER_HOST
HETZNER_PORT
HETZNER_USER
HETZNER_PASSWORD
HETZNER_TARGET_DIR
```

`HETZNER_TARGET_DIR` ist `schlosszwerge.com`.

## Migrationshinweise

- `CNAME` wird nicht mehr verwendet, weil die produktive Auslieferung ueber Hetzner erfolgen soll.
- Die bisherige produktive GitHub-Pages-Seite bleibt unberuehrt, solange DNS nicht auf Hetzner zeigt.
- Die Berechtigung fuer `Birdy1980` wurde im neuen Repository eingeladen und muss bei Bedarf von der Person angenommen werden.
