# Die Schlosszwerge – Website

Die Website wird als statisches HTML und CSS ausgeliefert. GitHub Actions setzt redaktionelle Markdown-Texte in feste HTML-Vorlagen ein und prüft das Ergebnis.

## Lokal ansehen

```bash
git switch codex/modern-html-css-website
python3 -m venv .venv
.venv/bin/python -m pip install -r .github/scripts/requirements.txt
.venv/bin/python .github/scripts/build_site.py --output .site-build
.venv/bin/python -m http.server 8084 --bind 127.0.0.1 --directory .site-build
```

Aufruf: [http://127.0.0.1:8084/](http://127.0.0.1:8084/). Für einen erneuten Build einen neuen Ausgabeordner wählen oder den bisherigen generierten Ordner vorher verschieben. Texte lassen sich auch lokal bearbeiten, etwa mit `vim inhalte/vereinsgeschichte.md`.

## Texte direkt über GitHub ändern

1. In GitHub den Branch `codex/modern-html-css-website` auswählen und die passende Markdown-Datei öffnen.
2. Auf das Stiftsymbol klicken. Eine Leerzeile trennt Absätze, `##` beginnt eine Überschrift und `###` eine Unterüberschrift.
3. In einem neuen Arbeitsbranch speichern und den Pull Request gegen `codex/modern-html-css-website` öffnen. GitHub prüft die erzeugte Website.
4. Nach erfolgreicher Prüfung in den Entwurfsbranch mergen. Dadurch aktualisiert GitHub die [Dev-Vorschau](https://dev.schlosszwerge.com/).

```markdown
## Unsere neue Überschrift

Hier steht der Text für die Website.

[Mehr zur Anmeldung](/anmeldung/)
```

Zusätze wie `{#verein-heute}` an bestehenden Überschriften erhalten alte Direktlinks. Bilder nach `assets/images/` hochladen und mit `![Der Gruppenraum](/assets/images/gruppenraum.jpg)` einbinden. Historische Fotos und Fotos von Personen vorab freigeben lassen.

## Welche Datei gehört zu welcher Seite?

| Seite | Datei |
| --- | --- |
| Startseite / Einrichtungsübersicht | `index.html` |
| Aktuelles | `inhalte/aktuelles.md` und `inhalte/meldungen/` |
| Anmeldung und Mitgliedschaft | `anmeldung/index.html` |
| Team und Vorstand | `einrichtung/team/index.html` |
| Pädagogisches Konzept | `inhalte/paedagogik.md` |
| Gewaltschutzkonzept | `einrichtung/gewaltschutzkonzept/index.html` |
| Tagesablauf | `einrichtung/tagesablauf/index.html` |
| Öffnungszeiten und Termine | `einrichtung/oeffnungszeiten/index.html` |
| Räume und Außengelände | `einrichtung/raeumlichkeiten/index.html` |
| Finanzierung und Unterstützung | `einrichtung/finanzen/index.html` |
| Vereinsgeschichte | `inhalte/vereinsgeschichte.md` |
| Karriere | `inhalte/karriere.md` |
| Kontakt und Anfahrt | `unsfinden/index.html` |
| Impressum / Datenschutz | `impressum/index.html` / `datenschutz/index.html` |
| Seitenübersicht / Fehlerseite | `categories/index.html` / `404.html` |

`einrichtung/index.html` leitet die bisherige Adresse `/einrichtung/` auf die Startseite weiter. Den Einstieg daher nur in der obersten `index.html` bearbeiten.

## Eine Neuigkeit ergänzen

Unter `inhalte/meldungen/` eine Datei wie `2026-11-22-vereinsfest.md` anlegen. Das Datum im Dateinamen bestimmt Anzeige und Sortierung. Die neueste Meldung steht oben.

```markdown
## Überschrift der Meldung

Hier steht der freigegebene Text.
```

Für eine neue Station der Vereinsgeschichte einen vorhandenen Eintrag aus der nummerierten Markdown-Liste kopieren. Die eingerückten Zeilen gehören zur jeweiligen Station.

## Layout und gemeinsame Angaben

- `assets/css/main.css`: Farben stehen als Variablen ganz oben. Darunter folgen nach Bereichen kommentierte Regeln; Mobilansicht und Druckansicht stehen am Ende.
- `assets/js/site.js`: Kleine, unabhängige Ergänzung für das mobile Menü und dessen Tastaturbedienung. Inhalte, Links und häufige Fragen funktionieren auch ohne JavaScript.
- Kopf- und Fußzeile sind bewusst normales HTML in jeder Datei. Bei einer Änderung gemeinsamer Menüs oder Kontaktdaten müssen die entsprechenden Blöcke auf allen Seiten angepasst werden. Die Kommentare `KOPFZEILE` und `FUSSZEILE` markieren sie. Die Prüfung erkennt abweichende Hauptmenüs.
- PDFs liegen in `assets/pdf/`. Bei Dateinamen auf Groß-/Kleinschreibung achten.

## Technische Prüfung

```bash
python3 .github/scripts/check_site.py --root .site-build
node --check assets/js/site.js
```

Python prüft die erzeugten HTML-Dateien. HTML-Tags im Markdown werden als Text dargestellt. Node prüft die Syntax des Navigationsskripts.

## Betrieb und Veröffentlichung

Aus Sicht des Betriebs bleibt die Architektur statisch: GitHub ist die Quelle, Apache auf dem Hetzner-Webspace liefert die Dateien aus. Schriften, Bilder, CSS und JavaScript werden lokal vom selben Webspace geladen. Es gibt keine externe Schriftbibliothek, kein Tracking und keine serverseitige Anwendung.

- Pull Requests: `.github/workflows/validate.yml` baut und prüft die Website. Für `main` verlangt GitHub den erfolgreichen Check `validate` und eine unabhängige Freigabe, auch bei Admins.
- Push auf `main`: `.github/workflows/deploy.yml` prüft erneut und überträgt anschließend per SFTP in den Domain-Ordner `schlosszwerge.com`.
- Der Entwurfsbranch aktualisiert ausschließlich die Entscheidungsvorschau auf `dev.schlosszwerge.com`. Ein späterer Merge nach `main` ist eine produktive Veröffentlichung und gehört nicht zur Entwurfsprüfung.
- Die bestehenden `HETZNER_*`-Secrets bleiben unverändert. Zugangsdaten gehören nicht in HTML oder Git.

Vor einer späteren Veröffentlichung sind die bestehenden Terminangaben fachlich zu prüfen: In der übernommenen Tabelle für 2026 passen einzelne Wochentage und Jahreswechselangaben nicht zusammen. Diese Daten wurden beim Designwechsel nicht neu festgelegt. Impressum und Website-Datenschutzhinweise wurden am 20.11.2026 anhand amtlicher Quellen, des aktuellen Vereinsregisterauszugs und des technischen Entwurfs überarbeitet. Die noch offenen fachlichen Prüfungen (insbesondere unabhängige DSB-Rolle, tatsächliche Log-/Löschkonfiguration und gegebenenfalls erteilte Steuer-Identifikationsnummern) stehen im [Prüfprotokoll in Outline](https://docs.lenmail.de/doc/website-impressum-und-datenschutz-prufung-und-entwurfsstand-20112026-IeGwmolqAt). Der Entwurf ist dadurch nicht automatisch produktiv oder abschließend rechtlich freigegeben.

## Entscheidungsvorschau auf Hetzner

Der Entwurf wird unter **https://dev.schlosszwerge.com/** zur Abstimmung bereitgestellt. Der Link ist ohne Anmeldung aufrufbar. Ein Hinweis im Seitenkopf kennzeichnet die Website als Entwurf.

Die Vorschau verwendet ein eigenes Webroot `schlosszwerge-vorschau`, getrennt vom Domain-Ordner `schlosszwerge.com`. Die neue Subdomain wird in konsoleH verwaltet und verwendet ein eigenes Let's-Encrypt-Zertifikat.

Der Workflow `.github/workflows/preview.yml` aktualisiert ausschließlich dieses Vorschauverzeichnis bei einem Push auf `codex/modern-html-css-website`. Anschließend prüft er HTTPS, die Seiten und den Indexierungsschutz. Der Produktionsworkflow wird dafür nicht gestartet; ein Merge nach `main` bleibt ein gesonderter Schritt.

Das Vorschaupaket wird mit `.github/scripts/build_preview.py` erstellt. Dabei werden nur HTML-Seiten und tatsächlich referenzierte Assets übernommen. Git-Metadaten, interne Dokumentation und Zugangsdaten gehören nicht ins Paket. Die Originaldateien behalten ihre produktiven Einstellungen.

Indexierungsschutz der Vorschau:

- HTTP-Header `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet` für alle Antworten, auch PDFs und Fehlerseiten.
- Zusätzlicher `robots`-Meta-Tag mit `noindex` in jeder HTML-Seite.
- Keine Sitemap und keine Canonical-Verweise auf die Produktionswebsite im Vorschaupaket.
- `robots.txt` erlaubt den Abruf, damit Suchmaschinen die `noindex`-Anweisung lesen können. Ein pauschales Crawling-Verbot würde diesen Mechanismus behindern.
- Verzeichnisauflistung deaktiviert; HTTP wird auf HTTPS umgeleitet. Der ACME-Prüfpfad ist für die Zertifikatserneuerung von dieser Weiterleitung ausgenommen.

Lokales Erstellen und Prüfen:

```bash
.venv/bin/python .github/scripts/build_preview.py --source .site-build
python3 .github/scripts/check_preview_http.py --base-url https://dev.schlosszwerge.com
```

Das lokale Paket liegt in `.preview-site/` und wird von Git ignoriert. Die lokale Vorschau verwendet die gerenderten Dateien in `.site-build`.

## Lokaler Inhaltsentwurf (20.11.2026)

Vereinsgeschichte, Pädagogik, Team/Verein, Anmeldung, Finanzierung, Karriere und die Informationsseite wurden redaktionell überarbeitet. Die Chronik verwendet ausschließlich die bereits dokumentierten Stationen von 2004, 2012, 2013 und 2018. Ergänzungen stehen in `inhalte/vereinsgeschichte.md`. Historische Erinnerungen und Fotos müssen vor der Aufnahme belegt beziehungsweise freigegeben sein.

Vor einer Veröffentlichung dieser Textfassung mit der Leitung abgleichen:

- Betreuungsmodelle: bisheriges U3-Abholende um 15 Uhr gegenüber allgemeinen Öffnungszeiten bis 16 Uhr; Überschneidung von Ü3-Mittagessen und Ruhezeit. Die Zeitangaben wurden nicht eigenmächtig geändert.
- Aktueller Stand des vollständigen pädagogischen Konzepts und des bisher genannten Würzburger Sprachprogramms. Veraltete Ankündigungen werden im Text nicht als laufende Angebote dargestellt.
- Geltende Beiträge, Eingewöhnungsablauf und verfügbare Stellen. Keine unbestätigten Preise, Zeitversprechen oder Arbeitgeberleistungen ergänzt.

Die Inhaltsrunde und die Entfernung des seitlichen Themenmenüs sind zur Veröffentlichung auf `dev.schlosszwerge.com` freigegeben. Ein Push auf den Entwurfsbranch aktualisiert diese Entscheidungsvorschau. Alle Unterseiten verwenden eine zentrierte Lesespalte; die Einrichtungsthemen sind über die Startseite erreichbar. Der Draft bleibt ungemergt.
