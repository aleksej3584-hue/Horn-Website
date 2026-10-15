#!/usr/bin/env python3
"""Baut die Horn-Website.

    python3 tools/build.py

- index.html: Startseite mit Installationsplan und Abschnitten (Leistungen, Ablauf, Fotos, Über uns)

- Alle Unterseiten aus den Inhalten unten, mit gemeinsamem Header, Menü und Footer.
- Weiterleitungen von den alten WordPress-Adressen, sitemap.xml, robots.txt, 404.html.
"""
import base64
import hashlib
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'https://horn-elektro.de/'
PHONE_TEL = 'tel:+49407006101'
PHONE = '040 – 700 61 01'
PHONE_BTN = '040 700 61 01'
MAIL = 'info@horn-elektro.de'

ARROW = '<svg aria-hidden="true"><use href="#arrow"/></svg>'
MORE_ARROW = '<svg viewBox="0 0 21.5 18" aria-hidden="true"><path d="M0 9H20.1M12.1 1L20.1 9L12.1 17" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

LOGO_SVG = '''<svg viewBox="0 0 46 46" aria-hidden="true">
          <path d="M3.5 13.5L10 6.5H36L42.5 13.5V42.5H3.5Z" fill="none" style="stroke:var(--ink)" stroke-width="3" stroke-linejoin="miter"/>
          <path d="M30 11V33M24.5 27.5L30 33.5L35.5 27.5" fill="none" style="stroke:var(--acc)" stroke-width="3" stroke-linecap="butt"/>
          <path d="M8.5 36.5H11M13.5 36.5H16M18.5 36.5H21M36 36.5H38.5" fill="none" style="stroke:var(--acc)" stroke-width="2.4" stroke-linecap="butt"/>
        </svg>'''

# ---------------------------------------------------------------- navigation
SERVICES_NAV = [
    ('knx', 'KNX-Gebäudesteuerung'),
    ('datentechnik', 'Daten- & Glasfasertechnik'),
    ('pruefung', 'Anlagen- & Geräteprüfung'),
    ('notbeleuchtung', 'Notbeleuchtung'),
    ('schaltanlagenbau', 'Schaltanlagenbau'),
    ('sicherheit', 'Sicherheit & Zutritt'),
]
COMPANY_NAV = [
    ('ueber-uns.html', 'Über uns'),
    ('ausbildung.html', 'Ausbildung'),
    ('beratung.html', 'Beratung'),
    ('planung.html', 'Planung'),
    ('herstellung.html', 'Herstellung'),
    ('wartung.html', 'Wartung'),
]
COMPANY_FILES = {f for f, _ in COMPANY_NAV}

STEPS = [
    ('beratung.html', 'Beratung', 'Bedarf klären, vor Ort aufnehmen'),
    ('planung.html', 'Planung', 'Lösung, Termine und Ablauf festlegen'),
    ('herstellung.html', 'Herstellung', 'Installation durch unsere Fachleute'),
    ('wartung.html', 'Wartung', 'Prüfen, instand halten, reparieren'),
]


def e(s):
    return html.escape(s, quote=False)


def cur(cond, kind='page'):
    return f' aria-current="{kind}"' if cond else ''


def header(active):
    svc = '\n'.join(f'              <li><a href="leistungen.html#{a}">{e(t)}</a></li>' for a, t in SERVICES_NAV)
    com = '\n'.join(f'              <li><a href="{f}"{cur(f == active)}>{e(t)}</a></li>' for f, t in COMPANY_NAV)
    msvc = '\n'.join(f'            <li><a href="leistungen.html#{a}">{e(t)}</a></li>' for a, t in SERVICES_NAV)
    mcom = '\n'.join(f'            <li><a href="{f}"{cur(f == active)}>{e(t)}</a></li>' for f, t in COMPANY_NAV)
    act = lambda c: ' is-active' if c else ''
    return f'''<header class="site-head">
  <a class="logo" href="index.html" aria-label="Horn Elektrische Anlagen – Startseite">
        {LOGO_SVG}
        <span class="wm"><b>HORN</b><small>Elektrische Anlagen</small></span>
  </a>
  <nav class="nav" aria-label="Hauptnavigation">
        <ul>
          <li class="ni"><a href="index.html">Start</a></li>
          <li class="ni{act(active == 'leistungen.html')}">
            <a href="leistungen.html" aria-haspopup="true"{cur(active == 'leistungen.html')}>Leistungen<svg aria-hidden="true"><use href="#chev"/></svg></a>
            <ul class="dd">
{svc}
            </ul>
          </li>
          <li class="ni{act(active in COMPANY_FILES)}">
            <a href="ueber-uns.html" aria-haspopup="true">Unternehmen<svg aria-hidden="true"><use href="#chev"/></svg></a>
            <ul class="dd">
{com}
            </ul>
          </li>
          <li class="ni{act(active == 'kontakt.html')}"><a href="kontakt.html"{cur(active == 'kontakt.html')}>Kontakt</a></li>
        </ul>
  </nav>
  <button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="menu"><i></i><i></i><i></i></button>
  <a class="btn btn-top" href="{PHONE_TEL}" aria-label="Anrufen: {PHONE_BTN}"><span>{PHONE_BTN}</span>{ARROW}</a>
</header>

<div id="menu" class="menu" aria-hidden="true" inert>
  <div class="menu-tex" aria-hidden="true"></div>
  <div class="menu-in">
    <span class="menu-rule" aria-hidden="true"></span>
    <p class="menu-eye">Menü</p>
    <ul class="mlist">
      <li><a class="mrow" href="index.html">Start</a></li>
      <li class="acc">
        <button class="mrow" type="button" aria-expanded="false" aria-controls="m-leist">Leistungen<i class="pm" aria-hidden="true"></i></button>
        <div class="msub" id="m-leist"><div><ul>
            <li><a href="leistungen.html"{cur(active == 'leistungen.html')}>Alle Leistungen</a></li>
{msvc}
        </ul></div></div>
      </li>
      <li class="acc">
        <button class="mrow" type="button" aria-expanded="false" aria-controls="m-unt">Unternehmen<i class="pm" aria-hidden="true"></i></button>
        <div class="msub" id="m-unt"><div><ul>
{mcom}
        </ul></div></div>
      </li>
      <li><a class="mrow" href="kontakt.html"{cur(active == 'kontakt.html')}>Kontakt</a></li>
    </ul>
    <div class="mfoot">
      <a class="btn btn-menu" href="{PHONE_TEL}"><span>Jetzt anrufen</span>{ARROW}</a>
      <p class="mnote">{PHONE} &nbsp;/&nbsp; {MAIL}</p>
      <p class="mlegal"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></p>
    </div>
  </div>
</div>'''


def cta_band(title='Sprechen wir über Ihr Projekt.', eyebrow='Kontakt', subject=None):
    contact = 'kontakt.html' + (f'?thema={subject}' if subject else '') + '#anfrage'
    return f'''<section class="cta-band wrap" aria-label="Kontakt aufnehmen">
    <div>
      <p class="eyebrow">{e(eyebrow)}</p>
      <h2>{e(title)}</h2>
      <p>{PHONE} &nbsp;/&nbsp; {MAIL}</p>
    </div>
    <div class="actions">
      <a class="btn" href="{PHONE_TEL}"><span>Jetzt anrufen</span>{ARROW}</a>
      <a class="btn btn-ghost" href="{contact}"><span>Anfrage senden</span>{ARROW}</a>
    </div>
  </section>'''


def footer():
    svc = '\n'.join(f'          <li><a href="leistungen.html#{a}">{e(t)}</a></li>' for a, t in SERVICES_NAV)
    com = '\n'.join(f'          <li><a href="{f}">{e(t)}</a></li>' for f, t in COMPANY_NAV)
    return f'''<footer class="site-foot wrap">
  <div class="foot-grid">
    <div class="foot-brand">
      <a class="logo" href="index.html" aria-label="Horn Elektrische Anlagen – Startseite">
        {LOGO_SVG}
        <span class="wm"><b>HORN</b><small>Elektrische Anlagen</small></span>
      </a>
      <p>Thomas Horn Elektrische Anlagen<br>Bromberger Str. 24a<br>21629 Neu Wulmstorf</p>
      {seal('seal seal-foot')}
    </div>
    <div class="foot-col">
      <p class="foot-h">Kontakt</p>
      <ul>
        <li><a href="{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><a href="kontakt.html#anfrage">Anfrage senden</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <p class="foot-h">Leistungen</p>
      <ul>
{svc}
      </ul>
    </div>
    <div class="foot-col">
      <p class="foot-h">Unternehmen</p>
      <ul>
{com}
      </ul>
    </div>
  </div>
  <div class="foot-base">
    <span>© <span data-year>2026</span> Thomas Horn Elektrische Anlagen · Meisterbetrieb seit 1993 · ISO 9001</span>
    <nav aria-label="Rechtliches"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
  </div>
</footer>'''


SVGDEFS = '''<svg class="svgdefs" aria-hidden="true" focusable="false">
  <symbol id="seal" viewBox="0 0 120 120">
    <circle cx="60" cy="60" r="57" fill="none" stroke="currentColor" stroke-width="2"/>
    <circle cx="60" cy="60" r="49" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3"/>
    <rect x="34" y="70" width="52" height="4" fill="#fbba00"/>
    <text x="60" y="44" text-anchor="middle" font-family="JB, monospace" font-size="11" letter-spacing="3" fill="currentColor">ISO</text>
    <text x="60" y="66" text-anchor="middle" font-family="SG, sans-serif" font-weight="700" font-size="25" letter-spacing="-.5" fill="currentColor">9001</text>
    <text x="60" y="88" text-anchor="middle" font-family="JB, monospace" font-size="7.2" letter-spacing="1.2" fill="currentColor">ZERTIFIZIERT</text>
  </symbol>
  <symbol id="arrow" viewBox="0 0 21.5 18"><path d="M0 9H20.1M12.1 1L20.1 9L12.1 17" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="chev" viewBox="0 0 11 6.5"><path d="M1 1L5.5 5L10 1" fill="none" stroke="currentColor" stroke-width="1.7"/></symbol>
</svg>'''


def ver(rel):
    return hashlib.sha1(open(os.path.join(ROOT, rel), 'rb').read()).hexdigest()[:8]


def page(file, title, desc, body, active=None, noindex=False, bg=None, head_extra=''):
    canonical = DOMAIN + ('' if file == 'index.html' else file)
    robots = '\n<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{html.escape(desc)}">{robots}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#fafaf8">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="de_DE">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">{head_extra}
<link rel="preload" href="assets/fonts/sg.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/jb.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={ver('assets/site.css')}">
<script>
(function(){{var d=document.documentElement;
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  d.classList.add('intro');setTimeout(function(){{d.classList.remove('intro');}},2500);}})();
</script>
</head>
<body>
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
{SVGDEFS}
{bg or '<div class="page-glow" aria-hidden="true"><canvas class="circuit"></canvas></div>'}
{header(active or file)}

<main id="inhalt">
{body}
</main>

{footer()}
<script src="assets/circuit.js?v={ver('assets/circuit.js')}" defer></script>
<script src="assets/site.js?v={ver('assets/site.js')}" defer></script>
</body>
</html>
'''


def hero(eyebrow, title, lead, actions=''):
    return f'''  <section class="phero wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>{actions}
  </section>'''


def block(label, inner, id_=None):
    idattr = f' id="{id_}"' if id_ else ''
    return f'''  <section class="block wrap"{idattr}>
    <p class="block-label">{label}</p>
    <div class="block-body">
{inner}
    </div>
  </section>'''


def more(href, text):
    return f'      <a class="more" href="{href}">{e(text)}{MORE_ARROW}</a>'


def ticks(items):
    lis = '\n'.join(f'        <li>{x}</li>' for x in items)
    return f'      <ul class="ticks">\n{lis}\n      </ul>'


def steps(active_file):
    lis = []
    for i, (f, t, d) in enumerate(STEPS, 1):
        lis.append(f'        <li><a href="{f}"{cur(f == active_file, "step")}><span class="n">Schritt {i} von 4</span><b>{t}</b><em>{d}</em></a></li>')
    return '      <ol class="steps">\n' + '\n'.join(lis) + '\n      </ol>'


def hero_actions(subject=None, call=True):
    contact = 'kontakt.html' + (f'?thema={subject}' if subject else '') + '#anfrage'
    first = f'<a class="btn" href="{PHONE_TEL}"><span>{PHONE_BTN}</span>{ARROW}</a>' if call else ''
    return f'''
    <div class="actions">
      {first}
      <a class="btn btn-ghost" href="{contact}"><span>Anfrage senden</span>{ARROW}</a>
    </div>'''


def related(keys):
    names = dict(SERVICES_NAV)
    return '\n'.join(more(f'leistungen.html#{k}', names[k]) for k in keys)


# ---------------------------------------------------------------- Leistungen
ICONS = {
    'knx': '<path d="M4 15.5L16 5l12 10.5V28H4z"/><path d="M9 22h14"/><circle cx="9" cy="22" r="1.6" fill="currentColor" stroke="none"/><circle cx="16" cy="22" r="1.6" fill="currentColor" stroke="none"/><circle cx="23" cy="22" r="1.6" fill="currentColor" stroke="none"/>',
    'datentechnik': '<rect x="6" y="6" width="20" height="14"/><path d="M10 6v4M13 6v4M16 6v4M19 6v4M22 6v4"/><path d="M12 20v4h8v-4M16 24v5"/>',
    'pruefung': '<rect x="8" y="3.5" width="16" height="25"/><rect x="11" y="7" width="10" height="6"/><circle cx="16" cy="20.5" r="4"/><path d="M16 20.5l2.6-2.6"/>',
    'notbeleuchtung': '<rect x="3.5" y="9" width="25" height="14"/><path d="M9 16h12M17 12l4 4-4 4"/>',
    'schaltanlagenbau': '<rect x="6" y="3.5" width="20" height="25"/><path d="M6 10.5h20M6 18h20"/><path d="M10 12.5v3.5M13.5 12.5v3.5M17 12.5v3.5M20.5 12.5v3.5"/><path d="M10 5.5v3M13.5 5.5v3"/>',
    'sicherheit': '<rect x="8" y="14" width="16" height="13"/><path d="M11 14v-3.5a5 5 0 0 1 10 0V14"/><circle cx="16" cy="19.5" r="1.6"/><path d="M16 21v2.5"/>',
}


SEAL_FILES = ['assets/dekra-iso9001.svg', 'assets/dekra-iso9001.png', 'assets/dekra-iso9001.webp', 'assets/dekra-iso9001.jpg']


def seal(cls='seal'):
    # Offizielles DEKRA-Siegel, sobald die Datei in assets/ liegt; sonst neutrales Siegel.
    for rel in SEAL_FILES:
        if os.path.exists(os.path.join(ROOT, rel)):
            return f'<img class="{cls} seal-img" src="{rel}" alt="DEKRA-Siegel: Qualitätsmanagement ISO 9001 zertifiziert" loading="lazy">'
    return f'<svg class="{cls}" role="img" aria-label="Zertifiziert nach ISO 9001"><use href="#seal"/></svg>'


PHOTOS = {
    'unterverteilung': ('Unterverteilung mit FI-Schutzschaltern, Leitungsschutzschaltern und Überspannungsschutz', 1500, 2000),
    'pruefungsbrett': ('Das Prüfungsbrett von Aykan Gezici aus der Abschlussprüfung', 1500, 1495),
    'zaehlerschrank': ('Zählerschrank mit Zählerplatz, Vorsicherungen, Fehlerstrom- und Leitungsschutzschaltern', 1500, 2000),
    'zaehlerschrank-montage': ('Zählerschrank und Unterverteilung während der Installation', 900, 1600),
    'steuerung': ('Steuerungsbau mit Motorschutzschalter, Schützen und Reihenklemmen', 1179, 1544),
    'aykan': ('Aykan Gezici, einer der Jahrgangsbesten 2025, stellt sein Prüfungsbrett vor', 2000, 1333),
    'aykan-hoch': ('Aykan Gezici, einer der Jahrgangsbesten 2025, stellt sein Prüfungsbrett vor', 999, 1333),
}


def photo(name, caption=True, cls='shot', eager=False):
    alt, w, h = PHOTOS[name]
    big = min(1400, w)
    cap = f'\n      <figcaption>{e(alt)}</figcaption>' if caption else ''
    load = 'eager' if eager else 'lazy'
    return f'''      <figure class="{cls}">
        <picture>
          <source type="image/webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1400.webp {big}w" sizes="(max-width: 760px) 100vw, 50vw">
          <img src="assets/img/{name}-800.jpg" srcset="assets/img/{name}-800.jpg 800w, assets/img/{name}-1400.jpg {big}w" sizes="(max-width: 760px) 100vw, 50vw" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="{load}" decoding="async">
        </picture>{cap}
      </figure>'''


def icon(key):
    return f'<svg class="ico" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{ICONS[key]}</svg>'


SERVICES = [
    ('knx', 'KNX', 'Intelligente Gebäudesteuerung mit KNX', [
        ('p', 'Energieeffizient, komfortabel, sicher und flexibel: KNX ist der weltweite Standard für die Haus- und Gebäudeautomation. Sonnenschutz, Licht, Klimaanlage, Heizung und Sicherheitssysteme lassen sich damit zentral über ein Bedienelement steuern.'),
        ('p', 'Diese Lösungen bieten wir für alle Gebäude und Anwendungen, vom Einfamilienhaus bis zum Gewerbeobjekt. Im Vorführraum mit SPS-Technik zeigen wir, wie das im Alltag aussieht.'),
    ]),
    ('datentechnik', 'Netzwerk', 'Daten- und Glasfasertechnik', [
        ('h3', 'Datentechnik'),
        ('p', 'Wir beraten, liefern und montieren eine stabile EDV-Infrastruktur, vom Anschlussschrank bis zu den aktiven Komponenten. Aktive und passive Datentechnik installieren wir passend zu Ihrem Bedarf.'),
        ('h3', 'Glasfasertechnik'),
        ('p', 'Für LWL-Glasfasertechnik sind wir Ihr fachkundiger Ansprechpartner und verlegen Glasfaserverkabelung für alle Anforderungen.'),
    ]),
    ('pruefung', 'Prüfung', 'Prüfung von Elektroanlagen und Geräten', [
        ('h3', 'Prüfen von Elektroanlagen'),
        ('p', 'Durch den Betrieb und durch Alterung können an elektrischen Anlagen Gefahren entstehen. Deshalb müssen sie regelmäßig geprüft werden. Auch nach einer Mängelbehebung ist die Sicherheit der Anlage mit einer Prüfung nachzuweisen. Wir bieten Ihnen das Komplettpaket für die rechtssichere Prüfung Ihrer Anlage.'),
        ('h3', 'Prüfen ortsveränderlicher Geräte'),
        ('p', 'Jeder Unternehmer muss seinen Mitarbeitern sichere elektrische Arbeitsmittel bereitstellen. Mit einer professionellen Betriebsmittelprüfung stellen Sie sicher, dass alle Geräte sicher sind und ordnungsgemäß funktionieren. Nur eine rechtskonform durchgeführte Prüfung weist nach, dass Sie dieser Pflicht nachgekommen sind.'),
        ('p', 'Ortsveränderliche Elektrogeräte dürfen ausschließlich Elektrofachkräfte prüfen. Unsere Fachkräfte erfüllen diese Anforderungen.'),
    ]),
    ('notbeleuchtung', 'Sicherheitslicht', 'Notbeleuchtungsanlagen', [
        ('p', 'Im Gefahrenfall zeigt die Notbeleuchtung Menschen an einem unbekannten Ort den Weg. Gerade in Gebäuden mit Publikumsverkehr halten wir die Vorschriften nach DIN und VDE zur Notbeleuchtung umfassend ein.'),
        ('p', 'Jedes Gebäude ist anders. Deshalb planen wir die Sicherheitsbeleuchtung vorab und besprechen sie mit Ihnen, bevor wir sie installieren.'),
    ]),
    ('schaltanlagenbau', 'Werkstatt', 'Schaltanlagenbau', [
        ('p', 'Wir planen und fertigen individuelle Schaltschränke, zugeschnitten auf die gewünschten Funktionen und die Gegebenheiten vor Ort. Dafür arbeiten wir mit bewährten Zulieferern zusammen.'),
        ('p', 'Verteilungen planen und bauen wir in unserer eigenen Werkstatt.'),
    ]),
    ('sicherheit', 'Gebäude', 'Sprechanlagen, Sicherheitstechnik, Zutritt und Schließanlagen', [
        ('h3', 'Sprechanlagen'),
        ('p', 'Wir installieren Tür- und Gegensprechanlagen für Wohnhäuser und Gewerbeobjekte, von der klassischen Klingelanlage bis zur Video-Türsprechanlage.'),
        ('h3', 'Sicherheitstechnik'),
        ('p', 'Wir planen Sicherheitstechnik passend zu Ihrem Gebäude und binden sie sauber in die bestehende Elektroinstallation ein.'),
        ('h3', 'Zutrittskontrollen'),
        ('p', 'Mit einer elektronischen Zutrittskontrolle legen Sie fest, wer wann welche Tür öffnen darf, zum Beispiel per Transponder, Karte oder Code.'),
        ('h3', 'Schließanlagen'),
        ('p', 'Elektronische Schließanlagen machen verlorene Schlüssel zu einer Einstellungssache: Sie sperren das Medium, statt Schlösser zu tauschen.'),
    ]),
]


def leistungen():
    idx = '\n'.join(
        f'      <a href="#{k}">{icon(k)}<b>{e(t)}</b><span>{e(lbl)}</span></a>'
        for (k, t), (_, lbl, _h, _c) in zip(SERVICES_NAV, SERVICES))
    blocks = []
    for key, lbl, h2, content in SERVICES:
        parts = [f'      <h2>{e(h2)}</h2>']
        for kind, txt in content:
            parts.append(f'      <{kind}>{e(txt)}</{kind}>')
        parts.append(more(f'kontakt.html?thema={key}#anfrage', 'Anfrage zu diesem Thema'))
        if key == 'schaltanlagenbau':
            parts.append(photo('steuerung', cls='shot shot-inline'))
        blocks.append(block(icon(key) + e(lbl), '\n'.join(parts), key))
    body = '\n'.join([
        hero('Leistungen',
             'Elektrotechnik für Wohnhaus, Gewerbe und Industrie.',
             'Elf Leistungen in sechs Bereichen, aus einer Hand geplant, installiert und gewartet.',
             hero_actions()),
        f'  <nav class="index wrap" aria-label="Leistungsbereiche">\n{idx}\n  </nav>',
        *blocks,
        cta_band('Welche Leistung brauchen Sie?'),
    ])
    return page('leistungen.html', 'Leistungen – Horn Elektrische Anlagen, Neu Wulmstorf',
                'KNX-Gebäudesteuerung, Daten- und Glasfasertechnik, Prüfung von Elektroanlagen und Geräten, Notbeleuchtung, Schaltanlagenbau, Sprech- und Sicherheitstechnik.',
                body)


# ---------------------------------------------------------------- Startseite
HOME_SVC = {
    'knx': 'Licht, Heizung und Sonnenschutz zentral steuern',
    'datentechnik': 'EDV-Netzwerke und LWL-Verkabelung',
    'pruefung': 'Rechtssichere Prüfung von Anlagen und Geräten',
    'notbeleuchtung': 'Sicherheitsbeleuchtung nach DIN und VDE',
    'schaltanlagenbau': 'Schaltschränke aus eigener Werkstatt',
    'sicherheit': 'Sprechanlagen, Zutritt und Schließanlagen',
}

JSONLD = """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Electrician","name":"Thomas Horn Elektrische Anlagen","url":"https://horn-elektro.de/","telephone":"+49 40 7006101","email":"info@horn-elektro.de","foundingDate":"1993","founder":{"@type":"Person","name":"Thomas Horn"},"address":{"@type":"PostalAddress","streetAddress":"Bromberger Str. 24a","postalCode":"21629","addressLocality":"Neu Wulmstorf","addressCountry":"DE"}}
</script>"""


def home():
    idx = '\n'.join(
        f'      <a href="leistungen.html#{k}">{icon(k)}<b>{e(t)}</b><span>{e(HOME_SVC[k])}</span></a>'
        for k, t in SERVICES_NAV)
    body = '\n'.join([
        f'''  <section class="stage wrap" aria-labelledby="h1">
    <div class="stage-main">
      <p class="eyebrow">Meisterbetrieb seit 1993 · ISO 9001</p>
      <h1 id="h1">Elektrotechnik, die<br>einfach funktioniert</h1>
      <p class="lead">Beratung, Planung, Installation, Wartung.<br>Ihr Meisterbetrieb in Neu Wulmstorf.</p>
      <div class="actions">
        <a class="btn" href="kontakt.html#anfrage"><span>Projekt anfragen</span>{ARROW}</a>
        <a class="btn btn-ghost" href="leistungen.html"><span>Leistungen</span>{ARROW}</a>
      </div>
    </div>
    <div class="facts stage-facts" aria-label="Kennzahlen">
      <div class="fact"><span class="num">1993</span><span class="lab">Gegründet</span></div>
      <div class="fact"><span class="num">11</span><span class="lab">Leistungen</span></div>
      <div class="fact"><span class="num">7+2</span><span class="lab">Mitarbeiter + Azubis</span></div>
      <div class="fact fact-seal">{seal()}</div>
    </div>
  </section>''',
        f'''  <section class="home-sec wrap" aria-labelledby="h-leist">
    <div class="home-head">
      <div><p class="eyebrow">Leistungen</p><h2 id="h-leist">Elf Leistungen in sechs Bereichen.</h2></div>
{more('leistungen.html', 'Alle Leistungen')}
    </div>
    <nav class="index" aria-label="Leistungsbereiche">
{idx}
    </nav>
  </section>''',
        f'''  <section class="home-sec wrap" aria-labelledby="h-ablauf">
    <div class="home-head">
      <div><p class="eyebrow">Ablauf</p><h2 id="h-ablauf">Von der ersten Frage bis zur Wartung.</h2></div>
    </div>
{steps(None)}
  </section>''',
        f'''  <section class="home-sec wrap" aria-labelledby="h-arbeit">
    <div class="home-head">
      <div><p class="eyebrow">Aus unserer Arbeit</p><h2 id="h-arbeit">Sauber verdrahtet, ordentlich beschriftet.</h2></div>
    </div>
    <div class="gallery gallery-4">
{photo('zaehlerschrank')}
{photo('steuerung')}
{photo('unterverteilung')}
{photo('aykan-hoch')}
    </div>
  </section>''',
        block('Über uns', seal('seal seal-lg') + '''
      <h2>Meisterbetrieb seit 1993, zertifiziert nach ISO 9001.</h2>
      <p>Thomas Horn hat den Betrieb 1993 gegründet. Heute arbeiten bei uns sieben Mitarbeiter und zwei Auszubildende, mit moderner Ausstattung, eigener Werkstatt und einem Qualitätsmanagement nach ISO 9001.</p>
''' + more('ueber-uns.html', 'Mehr über uns')),
        cta_band(),
    ])
    return page('index.html', 'Horn Elektrische Anlagen – Elektrotechnik in Neu Wulmstorf seit 1993',
                'Thomas Horn Elektrische Anlagen in Neu Wulmstorf: Beratung, Planung, Installation und Wartung. KNX, Daten- und Glasfasertechnik, Anlagenprüfung, Notbeleuchtung, Schaltanlagenbau. Meisterbetrieb seit 1993, ISO 9001.',
                body, active='index.html',
                bg='<div class="stage-bg" aria-hidden="true"><canvas class="circuit"></canvas></div>',
                head_extra=JSONLD)


# ---------------------------------------------------------------- Ablauf pages
PHASES = {
    'beratung.html': dict(
        n=1, name='Beratung', subject='beratung',
        title='Elektroberatung für Sicherheit, Komfort und Energieeffizienz.',
        lead='Nutzen Sie unsere Beratung und langjährige Projekterfahrung.',
        desc='Elektroberatung von Horn Elektrische Anlagen in Neu Wulmstorf: für Neubau und Renovierung, mit Aufnahme vor Ort.',
        blocks=[
            ('Was wir tun', 'Beratung vor Ort, für Neubau und Renovierung.', [
                'Wir kennen die Bedürfnisse unserer Kunden und bieten Ihnen als Elektriker moderne Lösungen für jeden Anspruch.',
                'Sie planen eine Renovierung oder einen Neubau? Wir unterstützen Sie dabei. Unser Fachpersonal nimmt Ihr Projekt auch vor Ort genau auf.',
                'Wir überzeugen mit freundlichem und fachkundigem Service, der weit über die reine Installation einzelner Komponenten hinausgeht.',
            ]),
        ],
        related=['knx', 'datentechnik', 'sicherheit'],
    ),
    'planung.html': dict(
        n=2, name='Planung', subject='planung',
        title='Elektroplanung, perfekt geplant von Horn.',
        lead='Möglichst vorher wissen, was später alles zu beachten ist.',
        desc='Elektroplanung von Horn Elektrische Anlagen: von der konventionellen Installation bis zur komplexen Automatisierung, mit Termin- und Zeitplanung.',
        blocks=[
            ('Was wir tun', 'Erst sorgfältig planen, dann sauber bauen.', [
                'Eine ordentliche und detaillierte Planung ist die Voraussetzung für jedes erfolgreiche Projekt. Unser erfahrenes Team findet für Ihre Planung eine Lösung und für jeden Wunsch eine Möglichkeit.',
                'Ob konventionelle Elektroinstallation oder komplexe Automatisierung: Planung und Organisation stimmen wir eng mit Ihnen ab. Terminplanung und Zeitmanagement schneiden wir auf jedes Projekt zu.',
            ]),
            ('Werkzeuge', 'Geplant mit E-CAD und eigener Kalkulation.', [
                'Für die Planung arbeiten wir mit E-CAD und einem eigenen Kalkulationsprogramm. So bekommen Sie nachvollziehbare Pläne und eine klare Kalkulation.',
            ]),
        ],
        related=['knx', 'notbeleuchtung', 'schaltanlagenbau'],
    ),
    'herstellung.html': dict(
        n=3, name='Herstellung', subject='herstellung',
        title='Installation von Elektroanlagen ist unsere Kernkompetenz.',
        lead='Sie bauen neu oder möchten modernisieren?',
        desc='Elektroinstallation für Neubau und Sanierung: Gebäudetechnik, Licht- und Netzwerktechnik vom Meisterbetrieb Horn in Neu Wulmstorf.',
        blocks=[
            ('Was wir tun', 'Neubau und Sanierung aus einer Hand.', [
                'Die Firma Horn ist seit 1993 Ihr Meisterbetrieb für hochwertige Elektroinstallationen und Gebäudetechnik sowie Licht- und Netzwerktechnik.',
                'Mit unseren erfahrenen Fachleuten bieten wir Ihnen die gesamte Kompetenz für Ihre Neubau- oder Sanierungsprojekte. Dabei stehen Qualität, Nachhaltigkeit, Klimafreundlichkeit und Umweltschutz im Fokus.',
            ]),
            ('Ausstattung', 'Eigene Werkstatt, moderne Fahrzeuge.', [
                'Verteilungen planen und bauen wir in der eigenen Werkstatt. Zeitgemäße Werkzeuge, gut ausgestattete Fahrzeuge und Arbeitsbühnen sorgen dafür, dass Aufträge zügig abgeschlossen werden.',
            ]),
        ],
        related=['datentechnik', 'schaltanlagenbau', 'sicherheit'],
        photo=['zaehlerschrank-montage', 'zaehlerschrank'],
    ),
    'wartung.html': dict(
        n=4, name='Wartung', subject='wartung',
        title='Zuverlässige Wartung von Elektroanlagen.',
        lead='Reparatur und Wartung von Elektroanlagen in Büros, Läden und Werkstätten.',
        desc='Wartung, Reparatur und Instandhaltung von Elektroanlagen, Wartungs- und Rufbereitschaftsverträge: Horn Elektrische Anlagen, Neu Wulmstorf.',
        blocks=[
            ('Was wir tun', 'Wartung, Instandhaltung und Reparatur.', [
                'Als Experten für Wartungs- und Reparaturarbeiten in der Elektrotechnik bieten wir Ihnen umfangreichen Service für die Wartung und Instandhaltung Ihrer Elektroanlagen.',
                'Durch regelmäßige Fachkurse sind wir immer auf dem neuesten Stand der gesetzlichen Bestimmungen.',
            ]),
            ('Verträge', 'Wartungs- und Rufbereitschaftsverträge.', [
                'Maximale Sicherheit und Kostenkontrolle bieten Ihnen unsere Wartungs- und Rufbereitschaftsverträge. Mit einem Rufbereitschaftsvertrag sind wir bei Störungen schnell für Sie da. Sprechen Sie uns an, wir stellen den passenden Umfang für Ihren Betrieb zusammen.',
            ]),
        ],
        related=['pruefung', 'notbeleuchtung'],
    ),
}


def phase(file):
    p = PHASES[file]
    parts = [hero(f'Ablauf &nbsp;·&nbsp; Schritt {p["n"]} von 4', e(p['title']), e(p['lead']), hero_actions(p['subject']))]
    for lbl, h2, paras in p['blocks']:
        inner = [f'      <h2>{e(h2)}</h2>'] + [f'      <p>{e(x)}</p>' for x in paras]
        parts.append(block(e(lbl), '\n'.join(inner)))
    if p.get('photo'):
        pics = p['photo'] if isinstance(p['photo'], list) else [p['photo']]
        inner = '\n'.join(photo(x) for x in pics)
        parts.append(block('Aus der Praxis', f'      <div class="gallery">\n{inner}\n      </div>' if len(pics) > 1 else photo(pics[0], cls='shot shot-inline')))
    parts.append(block('Ablauf', '      <h2>Von der ersten Frage bis zur Wartung.</h2>\n' + steps(file)))
    parts.append(block('Passende Leistungen', '      <h2>Häufig gefragt in dieser Phase.</h2>\n' + related(p['related'])))
    parts.append(cta_band(subject=p['subject']))
    return page(file, f'{p["name"]} – Horn Elektrische Anlagen, Neu Wulmstorf', p['desc'], '\n'.join(parts))


# ---------------------------------------------------------------- Über uns
def ueber_uns():
    facts = '''      <div class="facts">
        <div class="fact"><span class="num">1993</span><span class="lab">Gegründet</span></div>
        <div class="fact"><span class="num">7+2</span><span class="lab">Mitarbeiter + Azubis</span></div>
        <div class="fact"><span class="num">11</span><span class="lab">Leistungen</span></div>
      </div>'''
    body = '\n'.join([
        hero('Unternehmen &nbsp;·&nbsp; Über uns',
             'Seit 1993 ist Ihre Elektrotechnik in guten Händen.',
             'Thomas Horn hat den Betrieb 1993 gegründet. Heute arbeiten bei uns sieben Mitarbeiter und zwei Auszubildende.'),
        block('In Zahlen', facts),
        block('Ausstattung', '''      <h2>Modern ausgestattet, im Büro und auf der Baustelle.</h2>
      <p>Zügige Auftragsbearbeitung und -abwicklung sichern wir mit modernem Equipment.</p>
      <div class="cols">
        <div>
          <h3>Büro</h3>
''' + ticks(['Kommunikations- und EDV-Anlagen', 'E-CAD und Kalkulationsprogramm', 'SPS-Technik im Vorführraum']) + '''
        </div>
        <div>
          <h3>Technik</h3>
''' + ticks(['Zeitgemäße Werkzeuge und Fahrzeugausstattung', 'Arbeitsbühnen', 'Verteilungsplanung und -bau in eigener Werkstatt']) + '''
        </div>
      </div>'''),
        block('Qualität', seal('seal seal-lg') + '''
      <h2>Meisterbetrieb, zertifiziert nach ISO 9001.</h2>
      <p>Als Meisterbetrieb im Elektrotechniker-Handwerk arbeiten wir mit einem nach ISO 9001 zertifizierten Qualitätsmanagement. Abläufe, Prüfungen und Dokumentation sind klar geregelt, damit Sie sich auf das Ergebnis verlassen können.</p>'''),
        block('Auftreten', '''      <h2>Pünktlich, sauber, einheitlich.</h2>
      <p>Für ein kompetentes Auftreten beim Kunden sorgt unser einheitliches Erscheinungsbild vom Lehrling bis zum Meister. Saubere Kleidung und neue Fahrzeuge sind für uns selbstverständlich. Pünktliches Erscheinen hat oberste Priorität.</p>'''),
        block('Unser Ziel', '''      <h2>Kunden, die wiederkommen.</h2>
      <p>Wir möchten Sie nicht nur als Kunden gewinnen, sondern Sie auch in Zukunft wieder bei uns begrüßen. Deshalb begleiten wir Sie mit unserem Service von der Auftragserteilung bis zum Abschluss.</p>
''' + steps(None)),
        cta_band(),
    ])
    return page('ueber-uns.html', 'Über uns – Horn Elektrische Anlagen, Neu Wulmstorf',
                'Meisterbetrieb seit 1993: Thomas Horn Elektrische Anlagen in Neu Wulmstorf mit sieben Mitarbeitern und zwei Auszubildenden.',
                body)


# ---------------------------------------------------------------- Ausbildung
def ausbildung():
    body = '\n'.join([
        hero('Unternehmen &nbsp;·&nbsp; Ausbildung',
             'Ausbildung im Elektrohandwerk bei Horn.',
             'Wir bilden aus zum Elektroniker für Energie- und Gebäudetechnik. Zurzeit lernen zwei Auszubildende in unserem Team.'),
        block('Ausbildung', '''      <h2>Elektroniker für Energie- und Gebäudetechnik.</h2>
      <p>Ausbildungsbeginn ist im August, die Ausbildung dauert 3,5 Jahre.</p>
''' + ticks([
            'Ein Team aus sieben Fachleuten, vom Gesellen bis zum Meister',
            'Moderne Werkzeuge, Fahrzeuge und Arbeitsbühnen',
            'Eigene Werkstatt für Verteilungsbau und SPS-Technik im Vorführraum',
            'Abwechslung von der Elektroinstallation über KNX bis zur Datentechnik',
        ])),
        block('Jahrgangsbeste 2025', '''      <h2>Aykan Gezici gehört zu den Jahrgangsbesten 2025.</h2>
      <p>Aykan Gezici hat seine Ausbildung bei uns gemacht und die Abschlussprüfung als einer der Jahrgangsbesten 2025 bestanden. Sein Prüfungsbrett zeigt eine Verteilung mit Kleinsteuerung, Schützen und Klemmleiste, verdrahtet zu Schaltern, Steckdosen und CEE-Anschlüssen.</p>
''' + '\n      <div class="gallery gallery-43">\n' + photo('aykan') + '\n' + photo('pruefungsbrett') + '\n      </div>'),
        cta_band(),
    ])
    return page('ausbildung.html', 'Ausbildung – Horn Elektrische Anlagen, Neu Wulmstorf',
                'Ausbildung zum Elektroniker für Energie- und Gebäudetechnik bei Horn Elektrische Anlagen in Neu Wulmstorf.',
                body)


# ---------------------------------------------------------------- Kontakt
def kontakt():
    maps = 'https://www.google.com/maps/search/?api=1&query=Bromberger+Str.+24a%2C+21629+Neu+Wulmstorf'
    opts = [('allgemein', 'Allgemeine Anfrage')] + [(k, t) for k, t in SERVICES_NAV] + [
        ('beratung', 'Beratung'), ('planung', 'Planung'), ('herstellung', 'Installation / Neubau / Sanierung'), ('wartung', 'Wartung / Reparatur')]
    options = '\n'.join(f'            <option value="{k}">{e(t)}</option>' for k, t in opts)
    body = '\n'.join([
        hero('Kontakt',
             'Haben Sie Fragen, Wünsche oder Anregungen?',
             'Nehmen Sie Kontakt mit uns auf, wir helfen Ihnen gern weiter.'),
        f'''  <section class="contact-grid wrap" aria-label="Kontaktdaten und Anfrage">
    <dl class="cdata">
      <div>
        <dt>Telefon</dt>
        <dd><a href="{PHONE_TEL}">{PHONE}</a></dd>
      </div>
      <div>
        <dt>E-Mail</dt>
        <dd><a href="mailto:{MAIL}">{MAIL}</a></dd>
      </div>
      <div>
        <dt>Adresse</dt>
        <dd>Thomas Horn Elektrische Anlagen<br>Bromberger Str. 24a<br>21629 Neu Wulmstorf
          <a class="more" href="{maps}" target="_blank" rel="noopener" style="display:flex;width:max-content;margin-top:14px;font-size:14px;border-bottom:0">Route planen{MORE_ARROW}</a>
        </dd>
      </div>
      <div>
        <dt>Erreichbarkeit</dt>
        <dd>08:00 – 17:00 Uhr</dd>
      </div>
      <div>
        <dt>Einsatzgebiet</dt>
        <dd>Von Neu Wulmstorf aus in der Region und darüber hinaus</dd>
      </div>
    </dl>

    <form id="anfrage" class="form" novalidate aria-labelledby="anfrage-h">
      <h2 id="anfrage-h" class="full" style="font-size:clamp(27px,2.6vw,40px);letter-spacing:-.03em;line-height:1.1">Anfrage senden</h2>
      <div class="field">
        <label for="f-name">Name</label>
        <input id="f-name" name="name" autocomplete="name" required aria-describedby="f-name-err">
        <span class="err" id="f-name-err"></span>
      </div>
      <div class="field">
        <label for="f-kontakt">Telefon oder E-Mail</label>
        <input id="f-kontakt" name="kontakt" required aria-describedby="f-kontakt-err">
        <span class="err" id="f-kontakt-err"></span>
      </div>
      <div class="field">
        <label for="f-ort">Ort des Projekts <span class="opt">optional</span></label>
        <input id="f-ort" name="ort" autocomplete="address-level2">
      </div>
      <div class="field">
        <label for="f-thema">Thema</label>
        <select id="f-thema" name="thema">
{options}
        </select>
      </div>
      <div class="field full">
        <label for="f-msg">Ihre Nachricht</label>
        <textarea id="f-msg" name="nachricht" rows="6" required aria-describedby="f-msg-err" placeholder="Worum geht es? Zum Beispiel Neubau, Umbau, Prüfung oder ein Defekt."></textarea>
        <span class="err" id="f-msg-err"></span>
      </div>
      <div class="field full check">
        <input type="checkbox" id="f-ds" name="datenschutz" required aria-describedby="f-ds-err">
        <label for="f-ds">Ich habe die <a href="datenschutz.html">Datenschutzerklärung</a> gelesen. Meine Angaben werden nur zur Bearbeitung der Anfrage verwendet.</label>
      </div>
      <span class="err full" id="f-ds-err"></span>
      <div class="full form-foot">
        <button class="btn" type="submit"><span>Anfrage per E-Mail</span>{ARROW}</button>
        <p class="hint">Der Button öffnet Ihr E-Mail-Programm mit der fertigen Nachricht. Auf dieser Website wird nichts gespeichert.</p>
      </div>
      <p class="form-msg full" role="status" aria-live="polite"></p>
    </form>
  </section>''',
    ])
    return page('kontakt.html', 'Kontakt – Horn Elektrische Anlagen, Neu Wulmstorf',
                f'Kontakt zu Thomas Horn Elektrische Anlagen, Bromberger Str. 24a, 21629 Neu Wulmstorf. Telefon {PHONE}, {MAIL}.',
                body)


# ---------------------------------------------------------------- Impressum
def impressum():
    t = '''      <div class="legal-text">
        <h2>Angaben gemäß § 5 DDG</h2>
        <p>Thomas Horn Elektrische Anlagen<br>Inhaber: Thomas Horn<br>Bromberger Str. 24a<br>21629 Neu Wulmstorf</p>
        <h2>Kontakt</h2>
        <p>Telefon: 040 – 700 61 01<br>E-Mail: <a href="mailto:info@horn-elektro.de">info@horn-elektro.de</a></p>
        <h2>Umsatzsteuer-ID</h2>
        <p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz: DE160962545</p>
        <h2>Berufsrechtliche Angaben</h2>
        <p>Berufsbezeichnung: Meisterbetrieb im Elektrotechniker-Handwerk<br>
           Verliehen in: Deutschland<br>
           Zuständige Kammer: Handwerkskammer Braunschweig-Lüneburg-Stade<br>
           Eingetragen in die Handwerksrolle der Handwerkskammer Braunschweig-Lüneburg-Stade<br>
           Es gilt die Handwerksordnung (HwO), einsehbar unter <a href="https://www.gesetze-im-internet.de/hwo/" target="_blank" rel="noopener">gesetze-im-internet.de/hwo</a>.</p>
        <h2>Verbraucherstreitbeilegung</h2>
        <p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
        <h2>Haftung für Links</h2>
        <p>Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.</p>
      </div>'''
    body = '\n'.join([
        hero('Rechtliches', 'Impressum', 'Erstellung von elektrischen Anlagen, seit 1993 in geprüfter Qualität.'),
        block('Anbieter', t),
    ])
    return page('impressum.html', 'Impressum – Horn Elektrische Anlagen',
                'Impressum von Thomas Horn Elektrische Anlagen, Neu Wulmstorf.', body)


# ---------------------------------------------------------------- Datenschutz
def datenschutz():
    t = '''      <div class="legal-text">
        <h2>1. Verantwortlicher</h2>
        <p>Thomas Horn Elektrische Anlagen, Inhaber Thomas Horn<br>Bromberger Str. 24a, 21629 Neu Wulmstorf<br>Telefon 040 – 700 61 01, E-Mail <a href="mailto:info@horn-elektro.de">info@horn-elektro.de</a></p>

        <h2>2. Allgemeines</h2>
        <p>Wir nehmen den Schutz Ihrer persönlichen Daten sehr ernst und behandeln sie vertraulich und entsprechend den gesetzlichen Datenschutzvorschriften, insbesondere der Datenschutz-Grundverordnung (DSGVO). Diese Website kann ohne Angabe personenbezogener Daten genutzt werden. Sie setzt keine Cookies und verwendet keine Analyse- oder Tracking-Werkzeuge.</p>

        <h2>3. Hosting und Server-Logfiles</h2>
        <p>Diese Website wird bei der netcup GmbH, Emmy-Noether-Straße 10, 76131 Karlsruhe, betrieben. Beim Aufruf der Seiten erhebt der Anbieter automatisch Informationen, die Ihr Browser übermittelt:</p>
        <ul class="ticks">
          <li>IP-Adresse, Datum und Uhrzeit der Anfrage</li>
          <li>Browsertyp und Browserversion, verwendetes Betriebssystem</li>
          <li>Referrer-URL und aufgerufene Seite</li>
        </ul>
        <p>Diese Daten sind technisch nötig, um die Website sicher und stabil auszuliefern. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Eine Zusammenführung mit anderen Datenquellen findet nicht statt.</p>

        <h2>4. Kontakt per E-Mail, Telefon und Anfrageformular</h2>
        <p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage und für Anschlussfragen. Das Anfrageformular auf der Kontaktseite speichert oder versendet selbst keine Daten. Es öffnet Ihr eigenes E-Mail-Programm mit einer vorbereiteten Nachricht, die Sie selbst absenden.</p>
        <p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, wenn Ihre Anfrage mit einem Vertrag oder vorvertraglichen Maßnahmen zusammenhängt, sonst Art. 6 Abs. 1 lit. f DSGVO. Wir geben Ihre Daten nicht ohne Ihre Einwilligung weiter und löschen sie, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten bestehen.</p>

        <h2>5. Schriftarten</h2>
        <p>Die verwendeten Schriftarten (Space Grotesk und JetBrains Mono) sind lokal auf dieser Website eingebunden. Beim Laden der Seite wird keine Verbindung zu Servern von Google oder anderen Anbietern aufgebaut. Die Website lädt keine Inhalte von fremden Servern.</p>

        <h2>6. SSL-/TLS-Verschlüsselung</h2>
        <p>Diese Seite nutzt aus Sicherheitsgründen eine SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte Verbindung erkennen Sie am Schloss-Symbol und an „https://“ in der Adresszeile Ihres Browsers.</p>

        <h2>7. Ihre Rechte</h2>
        <p>Sie haben jederzeit das Recht auf Auskunft über Ihre gespeicherten Daten (Art. 15 DSGVO), auf Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) sowie auf Widerspruch gegen die Verarbeitung (Art. 21 DSGVO). Wenden Sie sich dazu an die oben genannten Kontaktdaten.</p>
        <p>Außerdem haben Sie das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Für uns zuständig ist die Landesbeauftragte für den Datenschutz Niedersachsen, Prinzenstraße 5, 30159 Hannover.</p>

        <p style="margin-top:20px;font-family:var(--f-mono);font-size:13px;color:var(--lab)">Stand: Oktober 2026</p>
      </div>'''
    body = '\n'.join([
        hero('Rechtliches', 'Datenschutz', 'Wir berücksichtigen die gesetzlichen Vorschriften.'),
        block('Datenschutzerklärung', t),
    ])
    return page('datenschutz.html', 'Datenschutz – Horn Elektrische Anlagen',
                'Datenschutzerklärung von Thomas Horn Elektrische Anlagen, Neu Wulmstorf.', body)


# ---------------------------------------------------------------- 404 (self-contained)
NOT_FOUND = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seite nicht gefunden – Horn Elektrische Anlagen</title>
<meta name="robots" content="noindex">
<style>
:root{color-scheme:light}
html,body{height:100%;margin:0;background:#fafaf8;color:#121212}
body{display:flex;flex-direction:column;justify-content:center;padding:0 max(20px,6vw);font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  background:radial-gradient(ellipse 55% 65% at 84% 18%,rgba(251,186,0,.16),transparent 70%) #fafaf8}
p{margin:0}
.eye{font-family:ui-monospace,Menlo,monospace;font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#6e6e6e;display:flex;gap:12px;align-items:center}
.eye::before{content:"";width:22px;height:2px;background:#fbba00}
h1{margin:22px 0 0;font-size:clamp(38px,6vw,76px);line-height:1.05;letter-spacing:-.035em;max-width:14em}
.lead{margin-top:22px;font-family:ui-monospace,Menlo,monospace;color:#3b3b3b;font-size:16px;line-height:1.6}
.row{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}
a{display:inline-flex;align-items:center;height:52px;padding:0 22px;background:#fbba00;color:#0b0b0b;text-decoration:none;font-size:18px}
a.g{background:transparent;color:#121212;box-shadow:inset 0 0 0 1px rgba(0,0,0,.3)}
a:focus-visible{outline:2px solid #121212;outline-offset:3px}
</style>
</head>
<body>
<p class="eye">Fehler 404</p>
<h1>Diese Seite gibt es nicht mehr.</h1>
<p class="lead">Vielleicht wurde sie verschoben. Auf der Startseite finden Sie alles Wichtige.</p>
<p class="row"><a href="https://horn-elektro.de/">Zur Startseite</a><a class="g" href="tel:+49407006101">040 – 700 61 01</a></p>
</body>
</html>
'''

# ---------------------------------------------------------------- redirects from old WordPress URLs
REDIRECTS = {
    'beratung': 'beratung.html', 'planung': 'planung.html', 'herstellung': 'herstellung.html',
    'wartung': 'wartung.html', 'wir-ueber-uns': 'ueber-uns.html', 'kontakt': 'kontakt.html',
    'impressum': 'impressum.html', 'datenschutz': 'datenschutz.html',
}


def redirect(target):
    return f'''<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Weiterleitung</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{DOMAIN}{target}">
<meta http-equiv="refresh" content="0; url=../{target}"></head>
<body style="background:#fafaf8;color:#121212;font-family:system-ui,sans-serif;padding:24px"><a style="color:#8a5a00" href="../{target}">Weiter zur Seite</a></body></html>
'''


FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 46 46"><rect width="46" height="46" fill="#000"/><path d="M3.5 13.5L10 6.5H36L42.5 13.5V42.5H3.5Z" fill="none" stroke="#fff" stroke-width="3"/><path d="M30 11V33M24.5 27.5L30 33.5L35.5 27.5" fill="none" stroke="#fbba00" stroke-width="3"/></svg>
'''


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    pages = {
        'index.html': home(),
        'leistungen.html': leistungen(),
        'ueber-uns.html': ueber_uns(),
        'ausbildung.html': ausbildung(),
        'kontakt.html': kontakt(),
        'impressum.html': impressum(),
        'datenschutz.html': datenschutz(),
    }
    for f in PHASES:
        pages[f] = phase(f)
    for f, c in pages.items():
        write(f, c)

    write('404.html', NOT_FOUND)
    write('assets/favicon.svg', FAVICON)
    for old, target in REDIRECTS.items():
        write(f'{old}/index.html', redirect(target))

    urls = list(pages)
    sm = '\n'.join(f'  <url><loc>{DOMAIN}{"" if u == "index.html" else u}</loc></url>'
                   for u in urls if u not in ('impressum.html', 'datenschutz.html'))
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n')
    print('built', len(pages), 'pages,', len(REDIRECTS), 'redirects')


if __name__ == '__main__':
    main()
