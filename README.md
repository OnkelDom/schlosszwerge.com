# schlosszwerge.com

Statische Website fuer `schlosszwerge.com`.

Dieses Repository enthaelt die fertige HTML-Version der bisherigen Schlosszwerge-Website. Jekyll wird hier nicht mehr im Produktiv-Workflow benoetigt. Aenderungen erfolgen direkt an HTML-, CSS-, JS- oder Asset-Dateien.

## Architektur

- Quelle: GitHub Repository `OnkelDom/schlosszwerge.com`
- Branch: `main`
- Auslieferung: statische Dateien
- Zielsystem: Hetzner Webspace per SFTP
- Zielpfad: Domain-Ordner `schlosszwerge.com`
- Deployment: `.github/workflows/deploy.yml`

## Bearbeitung

HTML-Dateien direkt bearbeiten:

```bash
vim index.html
vim einrichtung/team/index.html
vim anmeldung/index.html
```

Styles und Skripte liegen unter:

```bash
vim assets/css/main.css
vim assets/js/main.min.js
```

## Lokale Vorschau

```bash
python3 -m http.server 8083
```

Danach im Browser:

```text
http://localhost:8083/
```

## Deployment

Der Deploy laeuft automatisch bei jedem Push auf `main`.

Manueller Start:

```bash
gh workflow run deploy.yml --repo OnkelDom/schlosszwerge.com --ref main
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

- `main` ist der Hauptbranch.
- `CNAME` wird nicht mehr verwendet, weil die Auslieferung ueber Hetzner erfolgt.
- Die statische Seite wurde aus dem erfolgreichen Hetzner/Jekyll-Build uebernommen.
- Die Einladung fuer `Birdy1980` mit Schreibrechten ist im neuen Repository ausstehend.
