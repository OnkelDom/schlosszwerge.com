# Die Schlosszwerge – Website

Die Website besteht aus normalen **HTML5-Seiten und einer CSS-Datei**. Es gibt kein CMS, kein Framework, keine Paketinstallation und keinen Build-Schritt. Die HTML-Dateien sind die tatsächlich ausgelieferten Seiten.

Der Entwurf liegt im Branch `codex/modern-html-css-website`. Er ist zur lokalen Ansicht und zur Entscheidungsvorschau unter https://dev.schlosszwerge.com/ vorgesehen. Die öffentliche Hauptwebsite wird weiterhin aus `main` ausgeliefert.

## Lokal ansehen

Im Repository-Verzeichnis:

```bash
git switch codex/modern-html-css-website
python3 -m http.server 8084 --bind 127.0.0.1
```

Danach [http://127.0.0.1:8084/](http://127.0.0.1:8084/) öffnen. Der Server läuft bis `Strg+C`. Nach einer Änderung die Browserseite neu laden. Zum Bearbeiten beispielsweise:

```bash
vim index.html
vim einrichtung/team/index.html
vim assets/css/main.css
```

Die Vorschau braucht einen lokalen Webserver, weil Links und Bilder mit `/` beginnen. Eine HTML-Datei per Doppelklick zu öffnen genügt deshalb nicht.

## Texte direkt über GitHub ändern

1. Oben links den gewünschten Branch auswählen. Für die Entwurfsprüfung `codex/modern-html-css-website` verwenden.
2. Die passende HTML-Datei aus der Tabelle unten öffnen und auf das Stiftsymbol klicken.
3. Nach `INHALT ANFANG` suchen. Zwischen diesem Kommentar und `INHALT ENDE` stehen die Texte der Unterseite. Auf der Startseite heißen die Markierungen `STARTSEITE ANFANG` und `STARTSEITE ENDE`.
4. Nur den gewünschten Text ändern und die umgebenden HTML-Tags stehen lassen.
5. Die Änderung mit einer kurzen Beschreibung committen. Der Pull Request prüft automatisch HTML-Struktur, Navigation und lokale Verweise.

Ein Absatz sieht so aus:

```html
<p>Hier steht der Text, der auf der Website erscheint.</p>
```

Eine Überschrift und ein Link:

```html
<h2>Unsere neue Überschrift</h2>
<p>Mehr erfahren Sie auf der <a href="/anmeldung/">Anmeldeseite</a>.</p>
```

Ein Bild: Datei nach `assets/images/` hochladen und im HTML referenzieren. Ein aussagekräftiger Alternativtext beschreibt das Bild für Menschen, die es nicht sehen können.

```html
<img src="/assets/images/mein-neues-bild.jpg"
     alt="Der neu gestaltete Gruppenraum"
     loading="lazy">
```

Bei Bildern von Menschen müssen die erforderlichen Freigaben vorliegen. Der Entwurf verwendet vorhandene Raum- und Geländefotos; die früher entfernten Teamfotos werden nicht wieder eingebunden.

## Welche Datei gehört zu welcher Seite?

| Seite | Datei |
| --- | --- |
| Startseite / Einrichtungsübersicht | `index.html` |
| Aktuelles | `aktuelles/index.html` |
| Anmeldung und Mitgliedschaft | `anmeldung/index.html` |
| Team und Vorstand | `einrichtung/team/index.html` |
| Pädagogisches Konzept | `einrichtung/konzept/index.html` |
| Gewaltschutzkonzept | `einrichtung/gewaltschutzkonzept/index.html` |
| Tagesablauf | `einrichtung/tagesablauf/index.html` |
| Öffnungszeiten und Termine | `einrichtung/oeffnungszeiten/index.html` |
| Räume und Außengelände | `einrichtung/raeumlichkeiten/index.html` |
| Finanzierung und Unterstützung | `einrichtung/finanzen/index.html` |
| Vereinsgeschichte | `einrichtung/vereinsgeschichte/index.html` |
| Karriere | `karriere/index.html` |
| Kontakt und Anfahrt | `unsfinden/index.html` |
| Impressum / Datenschutz | `impressum/index.html` / `datenschutz/index.html` |
| Seitenübersicht / Fehlerseite | `categories/index.html` / `404.html` |

`einrichtung/index.html` leitet die bisherige Adresse `/einrichtung/` auf die Startseite weiter. Den Einstieg daher nur in der obersten `index.html` bearbeiten.

## Eine Neuigkeit ergänzen

In `aktuelles/index.html` innerhalb der Inhaltsmarkierungen einen solchen Block einfügen. Das Datum und alle Beispieltexte ersetzen und den Hinweis „Hier gibt es bald Neues“ entfernen, sobald die erste tatsächliche Meldung veröffentlicht wird:

```html
<article>
  <p class="eyebrow"><time datetime="2026-11-20">20. November 2026</time></p>
  <h2>Überschrift der tatsächlichen Neuigkeit</h2>
  <p>Hier den freigegebenen Text der Meldung eintragen.</p>
</article>
```

## Layout und gemeinsame Angaben

- `assets/css/main.css`: Farben stehen als Variablen ganz oben. Darunter folgen nach Bereichen kommentierte Regeln; Mobilansicht und Druckansicht stehen am Ende.
- `assets/js/site.js`: Kleine, unabhängige Ergänzung für das mobile Menü und dessen Tastaturbedienung. Inhalte, Links und häufige Fragen funktionieren auch ohne JavaScript.
- Kopf- und Fußzeile sind bewusst normales HTML in jeder Datei. Bei einer Änderung gemeinsamer Menüs oder Kontaktdaten müssen die entsprechenden Blöcke auf allen Seiten angepasst werden. Die Kommentare `KOPFZEILE` und `FUSSZEILE` markieren sie. Die Prüfung erkennt abweichende Hauptmenüs.
- PDFs liegen in `assets/pdf/`. Bei Dateinamen auf Groß-/Kleinschreibung achten.

## Technische Prüfung

```bash
python3 .github/scripts/check_site.py
node --check assets/js/site.js
```

Python prüft alle HTML-Seiten ohne zusätzliche Bibliotheken. Node ist ausschließlich für die optionale Syntaxprüfung des kleinen Skripts nötig; zum Bearbeiten und Ausliefern der Website wird Node nicht gebraucht.

## Betrieb und Veröffentlichung

Aus Sicht des Betriebs bleibt die Architektur statisch: GitHub ist die Quelle, Apache auf dem Hetzner-Webspace liefert die Dateien aus. Schriften, Bilder, CSS und JavaScript werden lokal vom selben Webspace geladen. Es gibt keine externe Schriftbibliothek, kein Tracking und keine serverseitige Anwendung.

- Pull Requests: `.github/workflows/validate.yml` prüft die Website.
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
python3 .github/scripts/build_preview.py
python3 .github/scripts/check_preview_http.py --base-url https://dev.schlosszwerge.com
```

Das lokale Paket liegt in `.preview-site/` und wird von Git ignoriert. Die normale lokale Vorschau der bearbeitbaren Quelldateien funktioniert weiterhin wie oben beschrieben.
