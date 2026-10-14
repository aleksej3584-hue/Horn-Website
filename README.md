# Horn Website

Neue Website für **Thomas Horn Elektrische Anlagen**, Bromberger Str. 24a, 21629 Neu Wulmstorf.

## Seiten

| Datei | Inhalt |
|---|---|
| `index.html` | Startseite (Installationsplan im ersten Bildschirm, darunter Leistungen, Ablauf, Über uns, Karriere) |
| `leistungen.html` | Alle 11 Leistungen in 6 Bereichen, mit Sprungmarken (`#knx`, `#datentechnik`, `#pruefung`, `#notbeleuchtung`, `#schaltanlagenbau`, `#sicherheit`) |
| `beratung.html`, `planung.html`, `herstellung.html`, `wartung.html` | Ablauf in 4 Schritten |
| `ueber-uns.html`, `ausbildung.html` | Unternehmen, Ausbildung |
| `kontakt.html` | Kontaktdaten und Anfrageformular (öffnet das E-Mail-Programm, speichert nichts) |
| `impressum.html`, `datenschutz.html` | Rechtliches |
| `404.html` | Fehlerseite |
| `beratung/`, `planung/`, `herstellung/`, `wartung/`, `wir-ueber-uns/`, `kontakt/`, `impressum/`, `datenschutz/` | Weiterleitungen von den alten WordPress-Adressen |
| `sitemap.xml`, `robots.txt` | für Suchmaschinen |

## Bearbeiten

Alle Texte und Seiten (auch die Startseite) stehen in `tools/build.py`.
Nach jeder Änderung neu bauen:

```
python3 tools/build.py
```

Gemeinsames Design der Unterseiten: `assets/site.css`, Verhalten (Menü, Formular): `assets/site.js`.
Animierter Installationsplan (Hintergrund): `assets/circuit.js`.
Die Website lädt nichts von fremden Servern.

## Offene Punkte (vom Kunden)

Auf den Seiten gelb markiert:

- **Datenschutz:** endgültiger Hosting-Anbieter (Domain liegt bei Netcup); Text rechtlich prüfen lassen

Außerdem:

- **Fotos, Referenzen:** fehlen noch.
- **ISO 9001:** Zurzeit ein neutrales, selbst gestaltetes Siegel. Das offizielle Siegel des Zertifizierers (z. B. TÜV/DEKRA) als Datei anfragen und ersetzen.
- **Logo:** neu als einfaches SVG-Zeichen nachgebaut. Original als Vektordatei anfragen.

## Online ansehen

GitHub Pages: Settings → Pages → Deploy from a branch → `main` / root.
Danach unter https://aleksej3584-hue.github.io/Horn-Website/

`ANALYSE-horn-elektro.md` enthält die Analyse der alten Seite.
