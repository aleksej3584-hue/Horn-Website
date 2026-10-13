# Horn Website

Neue Website für **Thomas Horn Elektrische Anlagen**, Bromberger Str. 24a, 21629 Neu Wulmstorf.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite (Vollbild mit Video, eigenständige Datei mit eingebetteten Schriften) |
| `leistungen.html` | Alle 11 Leistungen in 6 Bereichen, mit Sprungmarken (`#knx`, `#datentechnik`, `#pruefung`, `#notbeleuchtung`, `#schaltanlagenbau`, `#sicherheit`) |
| `beratung.html`, `planung.html`, `herstellung.html`, `wartung.html` | Ablauf in 4 Schritten |
| `ueber-uns.html`, `ausbildung.html` | Unternehmen |
| `kontakt.html` | Kontaktdaten und Anfrageformular (öffnet das E-Mail-Programm, speichert nichts) |
| `impressum.html`, `datenschutz.html` | Rechtliches |
| `404.html` | Fehlerseite |
| `beratung/`, `planung/`, `herstellung/`, `wartung/`, `wir-ueber-uns/`, `kontakt/`, `impressum/`, `datenschutz/` | Weiterleitungen von den alten WordPress-Adressen |
| `sitemap.xml`, `robots.txt` | für Suchmaschinen |

## Bearbeiten

Texte und Seiten stehen in `tools/build.py`, die Startseite in `tools/home.src.html`.
Nach jeder Änderung neu bauen:

```
python3 tools/build.py
```

Gemeinsames Design der Unterseiten: `assets/site.css`, Verhalten (Menü, Formular): `assets/site.js`.

## Offene Punkte (vom Kunden)

Auf den Seiten gelb markiert:

- **Impressum:** Umsatzsteuer-ID, Berufsbezeichnung, zuständige Handwerkskammer, Handwerksrolle
- **Kontakt:** Öffnungszeiten / Erreichbarkeit
- **Datenschutz:** endgültiger Hosting-Anbieter, Datum; Text rechtlich prüfen lassen
- **Ausbildung:** Ausbildungsberuf und Beginn

Außerdem:

- **Texte als Entwurf neu geschrieben** (gab es auf der alten Seite nicht): Sprechanlagen, Sicherheitstechnik, Zutrittskontrollen, Schließanlagen, dazu die Seite Ausbildung. Bitte vom Kunden prüfen lassen.
- **Hintergrundvideo:** wird von Amazon CloudFront geladen (in der Datenschutzerklärung erwähnt). Besser: Video-Datei selbst hosten und die URL in `tools/home.src.html` ersetzen.
- **Fotos, Referenzen, Zertifikate:** fehlen noch komplett.
- **Logo:** neu als einfaches SVG-Zeichen nachgebaut. Original als Vektordatei anfragen.

## Online ansehen

GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
Danach unter https://aleksej3584-hue.github.io/horn-website/

`ANALYSE-horn-elektro.md` enthält die Analyse der alten Seite.
