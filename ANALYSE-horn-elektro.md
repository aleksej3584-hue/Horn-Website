# Analyse horn-elektro.de (Stand 13.10.2026)

## 1. Firma
- **Name:** Thomas Horn Elektrische Anlagen ("Horn Elektro"), Inhaber Thomas Horn
- **Adresse:** Bromberger Str. 24a, 21629 Neu Wulmstorf (auf der Seite steht im Footer "Staße", ein Tippfehler)
- **Tel.:** 040 – 700 61 01 · **E-Mail:** info@horn-elektro.de
- **Gegründet:** 1993, heute 7 Mitarbeiter und 2 Auszubildende
- **Positionierung:** Meisterbetrieb / Elektrofachbetrieb für Elektroanlagen und Automatisierungstechnik
- **Claims:** "Faire Preise, schnelle Termine und kompetente saubere Arbeit", "Umfassende Leistungen. Professionell und gewissenhaft."

## 2. Sitemap (8 Seiten, alle Seiten Einzel-Pages)
| URL | Zweck |
|---|---|
| `/` | Start: Willkommen, Leistungsüberblick |
| `/beratung/` | Beratung (Neubau, Renovierung, Vor-Ort-Aufnahme) |
| `/planung/` | Elektroplanung (konventionell bis Automatisierung) |
| `/herstellung/` | Installation / Neubau / Sanierung |
| `/wartung/` | Wartung, Reparatur, Notfall, Rufbereitschaftsverträge |
| `/wir-ueber-uns/` | Firmenporträt, Ausstattung, Haltung |
| `/kontakt/` | Adresse, Telefon, E-Mail (kein Formular gefunden) |
| `/impressum/`, `/datenschutz/` | Rechtliches |

**Hauptmenü:** Beratung · Planung · Herstellung · Wartung · Wir über uns · Kontakt
**Kopfzeile:** Telefon und E-Mail, Suchfeld. **Footer:** Firmenadresse, Impressum, Datenschutz.

## 3. Aufbau jeder Seite
1. Großes Hero-Bild mit Headline (Zeilenumbrüche im Text)
2. Kurzer Einleitungstext
3. Leistungsliste mit 11 Punkten als Akkordeon / Toggle (auf jeder Seite identisch)
4. Logo-Band "3label" (Bild)

## 4. Leistungen (11) – Texte vorhanden bei 7
1. **Intelligente Gebäudesteuerung KNX:** Licht, Sonnenschutz, Klima, Heizung und Sicherheit zentral steuern
2. **Datentechnik:** aktive und passive Netzwerktechnik, vom Anschlussschrank bis zu den aktiven Komponenten
3. **Glasfasertechnik:** LWL-Verkabelung
4. **Notbeleuchtungsanlagen:** nach DIN und VDE, Planung vorab
5. **Prüfen von Elektroanlagen:** rechtssichere Prüfung
6. **Prüfen ortsveränderlicher Geräte:** Betriebsmittelprüfung (DGUV V3), nur durch Elektrofachkräfte
7. **Schaltanlagenbau:** individuelle Schaltschränke, gefertigt mit Zulieferern
8. **Sprechanlagen**, 9. **Sicherheitstechnik**, 10. **Zutrittskontrollen**, 11. **Schließanlagen**
   → Nur als Überschrift vorhanden, **ohne Beschreibung**. Hier muss der Kunde Texte liefern.

## 5. Inhalte pro Seite (Kerntexte)
- **Start:** "Herzlich willkommen bei Ihrem erfahrenden Elektrofachbetrieb. Faire Preise, schnelle Termine und kompetente saubere Arbeit. Wir sind bewährter Fachbetrieb für Elektroanlagen und Automatisierungstechnik. Als eingetragener Elektroinstallations- und Automatisierungsbetrieb …"
- **Beratung:** "Unsere Elektroberatung: für Sicherheit, Komfort und Energieeffizienz." Projekterfahrung, Renovierung/Neubau, Aufnahme vor Ort, freundlicher Service.
- **Planung:** "Elektroplanung – perfekt geplant von HORN." Abstimmung mit dem Kunden, Termin- und Zeitmanagement je Projekt.
- **Herstellung:** "Installation von Elektroanlagen gehört zu unserer Kernkompetenz." Elektroinstallation, Gebäudetechnik, Licht- und Netzwerktechnik. Fokus auf Qualität, Nachhaltigkeit, Klimafreundlichkeit.
- **Wartung:** "Zuverlässige Wartung von Elektroanlagen." Büros, Läden, Werkstätten. Instandhaltungsservice für Notfälle, Wartungs- und Rufbereitschaftsverträge, ständige Weiterbildung.
- **Wir über uns:** Seit 1993; moderne Ausstattung (E-CAD, Kalkulationsprogramm, SPS-Technik im Vorführraum, eigene Werkstatt für Verteilungsplanung und -bau, Bühnen); einheitliches Erscheinungsbild, saubere Kleidung, neue Fahrzeuge; Pünktlichkeit als oberste Priorität; Begleitung von der Auftragserteilung bis zum Abschluss.
- **Kontakt:** "Haben Sie Fragen, Wünsche oder Anregungen?" mit Adresse, Telefon, E-Mail.

Die vollständigen Rohtexte liegen als WordPress-Export im Scratchpad (`site/pages.json`, `site/*.html`).

## 6. Design
- **Logo:** Schwarzes Haus-/Schaltschrank-Symbol mit gelbem "HORN", gelbem Blitz-/Strompfeil und Punktlinien, darunter "Elektrische Anlagen" in fetter Grotesk (JPG, 924×464, **kein Vektor**, weißer Hintergrund)
- **Farben:** Schwarz/Anthrazit (`#212934`), Weiß, **Signalgelb `#fbba00`** (Footer, Menü-Hover); weitere Akzente im CSS: Grün `#65bc7b`, Grau `#747474`
- **Schrift:** Roboto
- **Layout:** Seitenbreite 1200 px, H1 64 px, heller Header
- **Theme:** Avada (Fusion Builder) unter WordPress
- **Bilder (AdobeStock-Lizenzfotos, 2000 px breit, Querformat-Banner):**
  | Seite | Datei |
  |---|---|
  | Start | `AdobeStock_306955602_WEB.jpg` (Elektriker am Sicherungskasten, Textfläche links frei) |
  | Beratung | `AdobeStock_94040789-WEB.jpg` |
  | Planung | `AdobeStock_225536025_WEB.jpg` |
  | Herstellung | `AdobeStock_325047687_WEB.jpg` |
  | Wartung | `AdobeStock_327681313_WEB.jpg` |
  | Wir über uns | `AdobeStock_372432893_WEB.jpg` |
  | Kontakt, Impressum | `AdobeStock_236970362_WEB.jpg` |
  Die Fotos sind Stockbilder. Lizenz klären, bevor sie in die neue Seite übernommen werden.
  Reale Fotos von Team, Fahrzeugen und Werkstatt fehlen komplett.

## 7. Technik
- WordPress 7.1.3, Theme Avada, nginx, HTTPS, offene REST-API (`/wp-json/`), `xmlrpc.php` aktiv
- Sitemap: `wp-sitemap.xml`; `robots.txt` Standard
- **Kein Analytics, kein Tracking, kein Cookie-Banner, keine Karte, kein Kontaktformular** gefunden
- Meta-Titel überall nur "Horn Elektro"; `og:title` = "Start"; keine echte Meta-Description (OG-Description enthält den Seitentext)
- Seiten wurden zuletzt **Mai/Juni 2022** geändert

## 8. Schwächen, die die neue Seite beheben sollte
1. Kein Kontaktformular, keine Anfrage- oder Rückruf-Funktion; nur Telefon und E-Mail
2. Keine Referenzen, Projekte, Kundenstimmen, Zertifikate (Meisterbetrieb, Innung, KNX-Partner) und keine Team-Fotos
3. Keine Anfahrts-Karte, keine Öffnungszeiten, keine Notdienst-Nummer sichtbar
4. 4 von 11 Leistungen ohne Text; gleiche Leistungsliste auf jeder Seite (Duplicate Content)
5. SEO schwach: keine Meta-Descriptions, kein lokaler Bezug (Neu Wulmstorf / Hamburg-Süd / Harburg) in Titeln, kein Schema.org (LocalBusiness)
6. Rechtschreibfehler im Text: "erfahrenden", "Elektroanalgen", "Vorrausetzung", "detailierte", "Staße"
7. Datenschutzerklärung ist eine alte Vorlage (kein Hinweis auf Hosting, Schriften, Server-Logs beim Provider)
8. Logo als JPG mit weißem Hintergrund; Navigation nennt Arbeitsphasen statt Leistungen
9. Impressum ohne Umsatzsteuer-ID, Handwerkskammer, Berufsbezeichnung und Aufsichtsbehörde (bitte prüfen lassen)

## 9. Vorschlag Struktur der neuen Seite
**Navigation:** Leistungen · Über uns · Referenzen · Karriere · Kontakt (+ Telefon-Button)
- **Startseite:** Hero mit Telefon- und Anfrage-Button, Leistungs-Kacheln (KNX, Datentechnik, Glasfaser, Prüfungen, Notbeleuchtung, Schaltanlagen, Sicherheit), Zahlen (seit 1993, 7 Mitarbeiter, 2 Azubis), Ablauf (Beratung → Planung → Herstellung → Wartung), Notdienst, Kontakt
- **Je eine Unterseite pro Leistungsgruppe** mit eigenem Text
- **Über uns, Referenzen, Karriere/Ausbildung, Kontakt mit Formular und Karte, Impressum, Datenschutz**

## 10. Offene Fragen an den Kunden
- Bleibt das gelb-schwarze Logo? Gibt es eine Vektordatei (SVG/PDF)?
- Eigene Fotos (Team, Fahrzeuge, Werkstatt, Projekte) vorhanden?
- Texte für Sprechanlagen, Sicherheitstechnik, Zutrittskontrolle, Schließanlagen
- Referenzen, Zertifikate, Mitgliedschaften (Innung, KNX, VDE)?
- Notdienst / Rufbereitschaft: Nummer und Zeiten?
- Sollen Ausbildung und Stellenangebote eine Rolle spielen?
- Domain und Hosting bleiben gleich?
