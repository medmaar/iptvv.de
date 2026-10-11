"""Builds the indexable guide pages from content/<slug>.html fragments.

Each fragment starts with a JSON header in an HTML comment, followed by the
article body and, after a <!--faq--> marker, the FAQ as <h3>question</h3>
followed by one or more <p>answer</p>:

    <!--meta
    {"title": "...", "description": "...", "h1": "...", "badge": "...",
     "hero_sub": "...", "lead": "...", "breadcrumb": "...", "hub": "apps",
     "device": "...", "related": ["iptv-tivimate", ...]}
    -->
    <h2>...</h2><p>...</p> ...
    <!--faq-->
    <h3>Frage?</h3>
    <p>Antwort.</p>

Existing pages are updated in place (head, schema, hero, content, FAQ);
pages that don't exist yet are cloned from BASE_PAGE first. Every .html
file in the site also gets the shared footer and the short country list.

Run:  python3 build_seo_pages.py            (all fragments)
      python3 build_seo_pages.py iptv-vlc   (one page)
"""
import glob
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://iptvv.de'
BASE_PAGE = 'iptv-extreme.html'
BASE_REF = 'c990b02'  # last commit before the content rebuild
TODAY = '2026-10-11'

# ============================================================
# PAGE REGISTRY — label used in footer, breadcrumbs and related cards
# ============================================================
HUBS = {
    'kauf':     ('IPTV kaufen', '/iptv-abo'),
    'apps':     ('IPTV Apps', '/iptv-apps-vergleich'),
    'geraete':  ('IPTV Geräte', '/iptv-box'),
    'ratgeber': ('IPTV Ratgeber', '/was-ist-iptv'),
    'sender':   ('Sender & Sport', None),
}

PAGES = {
    # slug: (label, hub, blurb)
    'iptv-abo': ('IPTV Abo kaufen', 'kauf', 'Laufzeiten, Geräteanzahl und Bestellung'),
    'iptv-preise': ('IPTV Preise', 'kauf', 'Alle Pakete und Monatspreise im Überblick'),
    'iptv-kostenlos-testen': ('IPTV kostenlos testen', 'kauf', '24-Stunden-Test anfordern'),
    'iptv-anbieter-vergleich': ('IPTV Anbieter Vergleich', 'kauf', 'Woran Sie einen guten Anbieter erkennen'),
    'iptv-bewertungen': ('Kundenbewertungen', 'kauf', 'Erfahrungen unserer Kunden'),

    'iptv-apps-vergleich': ('IPTV Apps im Vergleich', 'apps', 'Die besten Player für jedes Gerät'),
    'iptv-smarters-pro': ('IPTV Smarters Pro', 'apps', 'Einrichtung, Download und Fehlerhilfe'),
    'iptv-tivimate': ('TiviMate', 'apps', 'Einrichtung, Premium und Einstellungen'),
    'iptv-xciptv': ('XCIPTV Player', 'apps', 'Einrichten auf Fire TV und Android'),
    'iptv-siptv': ('Smart IPTV (SIPTV)', 'apps', 'Playlist auf Samsung und LG hochladen'),
    'iptv-ss-iptv': ('SS IPTV', 'apps', 'Playlist laden auf Smart TVs'),
    'iptv-smartone': ('SmartOne IPTV', 'apps', 'MAC-Adresse und Playlist einrichten'),
    'iptv-flixiptv': ('FlixIPTV', 'apps', 'Einrichtung auf Smart TV und Android'),
    'iptv-gse-smart-iptv': ('GSE Smart IPTV', 'apps', 'Für iPhone, iPad und Apple TV'),
    'iptv-implayer': ('iMPlayer', 'apps', 'Moderner Player für Android TV'),
    'iptv-extreme': ('IPTV Extreme', 'apps', 'Kostenloser Player für Android'),
    'iptv-perfect-player': ('Perfect Player', 'apps', 'Schlanker Player mit EPG'),
    'iptv-stb-emulator': ('STB Emulator', 'apps', 'MAG-Portal auf Android nutzen'),
    'iptv-kodi': ('Kodi IPTV', 'apps', 'PVR IPTV Simple Client einrichten'),
    'iptv-vlc': ('VLC Player', 'apps', 'M3U-Playlist am PC abspielen'),
    'iptv-plex-jellyfin': ('Plex & Jellyfin', 'apps', 'Live-TV im eigenen Medienserver'),

    'iptv-box': ('IPTV Box & Stick', 'geraete', 'Welches Gerät passt zu Ihnen?'),
    'iptv-fire-stick': ('Fire TV Stick', 'geraete', 'Apps installieren und einrichten'),
    'iptv-android-box': ('Android TV Box', 'geraete', 'Nvidia Shield, Google TV und Co.'),
    'iptv-android': ('Android Handy & Tablet', 'geraete', 'IPTV unterwegs auf Android'),
    'iptv-smart-tv': ('Smart TV', 'geraete', 'Samsung, LG, Sony, Hisense und Philips'),
    'iptv-samsung-tv': ('Samsung TV', 'geraete', 'Apps für Tizen-Fernseher'),
    'iptv-lg-tv': ('LG TV', 'geraete', 'Apps für webOS-Fernseher'),
    'iptv-apple-tv': ('Apple TV', 'geraete', 'Die besten tvOS-Player'),
    'iptv-iphone-ipad': ('iPhone & iPad', 'geraete', 'IPTV auf iOS und iPadOS'),
    'iptv-mac': ('Mac & MacBook', 'geraete', 'IPTV unter macOS'),
    'iptv-windows-pc': ('Windows PC', 'geraete', 'Player für Windows 10 und 11'),
    'iptv-browser': ('IPTV im Browser', 'geraete', 'Ohne Installation streamen'),
    'iptv-chromecast': ('Chromecast & Google TV', 'geraete', 'Streamen und Casten'),
    'iptv-roku': ('Roku', 'geraete', 'Was auf Roku geht und was nicht'),
    'iptv-mag-box': ('MAG Box', 'geraete', 'Portal-URL eintragen'),
    'iptv-formuler': ('Formuler Box', 'geraete', 'MyTVOnline einrichten'),
    'iptv-receiver': ('IPTV Receiver', 'geraete', 'Enigma2, VU+, Dreambox und Co.'),

    'was-ist-iptv': ('Was ist IPTV?', 'ratgeber', 'Technik einfach erklärt'),
    'iptv-m3u-playlist': ('M3U Playlist', 'ratgeber', 'M3U, M3U8 und EPG erklärt'),
    'iptv-xtream-codes': ('Xtream Codes', 'ratgeber', 'Server, Benutzername, Passwort'),
    'iptv-4k': ('IPTV in 4K', 'ratgeber', 'Bandbreite, Geräte und Einstellungen'),
    'iptv-legal': ('Ist IPTV legal?', 'ratgeber', 'Die Rechtslage in Deutschland'),
    'iptv-vs-kabel': ('IPTV vs. Kabel', 'ratgeber', 'Kosten und Technik im Vergleich'),
    'iptv-zattoo': ('IPTV vs. Zattoo', 'ratgeber', 'Unterschiede im Überblick'),
    'iptv-telekom': ('Telekom MagentaTV', 'ratgeber', 'IPTV statt MagentaTV'),
    'iptv-vodafone': ('Vodafone TV', 'ratgeber', 'IPTV statt Vodafone Kabel'),
    'iptv-1und1': ('1&1 TV', 'ratgeber', 'IPTV statt 1&1 TV-Paket'),
    'iptv-einrichten': ('IPTV einrichten', 'ratgeber', 'Zugangsdaten in jede App eintragen'),
    'iptv-checker': ('IPTV Checker', 'ratgeber', 'Line, M3U und Server prüfen'),
    'iptv-senderliste': ('IPTV Senderliste', 'ratgeber', 'Sendergruppen und Kategorien'),
    'german-iptv': ('German IPTV (English)', 'kauf', 'Guide for English speakers'),

    'iptv-bundesliga': ('Bundesliga', 'sender', ''),
    'iptv-champions-league': ('Champions League', 'sender', ''),
    'iptv-sky': ('Sky Kanäle', 'sender', ''),
    'iptv-tuerkische-sender': ('Türkische Sender', 'sender', ''),
    'iptv-polnische-sender': ('Polnische Sender', 'sender', ''),
    'iptv-russische-sender': ('Russische Sender', 'sender', ''),
    'iptv-rumaenische-sender': ('Rumänische Sender', 'sender', ''),
    'iptv-albanische-sender': ('Albanische Sender', 'sender', ''),
}


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def json_block(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=2) + '</script>'


# ============================================================
# FOOTER (shared by every page on the site)
# ============================================================
def footer_links(hub):
    items = [(s, p[0]) for s, p in PAGES.items() if p[1] == hub]
    return '\n'.join(
        f'                        <li><a href="/{s}" class="text-gray-400 hover:text-white transition text-sm">{esc(label)}</a></li>'
        for s, label in items)


def render_footer():
    cols = []
    for hub, title in (('kauf', 'IPTV kaufen'), ('apps', 'Apps'), ('geraete', 'Geräte'),
                       ('ratgeber', 'Ratgeber'), ('sender', 'Sender &amp; Sport')):
        extra = ''
        if hub == 'kauf':
            extra = '\n                        <li><a href="/kontakt/wa" target="_blank" rel="noopener" class="text-gray-400 hover:text-white transition text-sm">Kontakt / Support</a></li>'
        cols.append(f'''                <div>
                    <h4 class="font-bold mb-4 text-sm uppercase tracking-wider text-gray-300">{title}</h4>
                    <ul class="space-y-3">
{footer_links(hub)}{extra}
                    </ul>
                </div>''')
    return f'''<footer class="border-t border-white/10 py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="mb-12">
                <a href="/de/" class="flex items-center gap-2 mb-4">
                    <img loading="lazy" src="germany-icon.png" alt="IPTV Deutschland Logo" width="40" height="40" class="w-10 h-10 object-contain">
                    <span class="text-xl font-bold">IPTV<span class="text-gradient"> Deutschland</span></span>
                </a>
                <p class="text-gray-400 max-w-2xl leading-relaxed text-sm">IPTV Deutschland (iptvv.de) liefert Ihren IPTV-Zugang als M3U-Playlist, Xtream-Codes-Login oder MAG-Portal – passend für Smart TV, Fire TV Stick, Android, Apple-Geräte, PC und Receiver. Support auf Deutsch per WhatsApp.</p>
            </div>
            <div class="grid sm:grid-cols-2 md:grid-cols-5 gap-8 mb-12">
{chr(10).join(cols)}
            </div>

            <div class="border-t border-white/10 pt-8 mb-8 text-center">
                <p class="text-xs text-gray-500 uppercase tracking-wider mb-4">Akzeptierte Zahlungsmethoden</p>
                <img loading="lazy" src="payment-methods.png" alt="Akzeptierte Zahlungsmethoden: Mastercard, Visa, American Express, PayPal, Klarna, Banküberweisung, Google Pay, Apple Pay" class="w-full max-w-md h-auto mx-auto" style="box-shadow: 0 8px 30px rgba(0,0,0,0.35)">
            </div>

            <div class="flex flex-col md:flex-row items-center justify-between gap-4 border-t border-white/10 pt-8">
                <p class="text-gray-500 text-sm">© 2026 IPTV Deutschland – iptvv.de · Alle Rechte vorbehalten.</p>
                <div class="flex items-center gap-4 text-gray-500 text-sm">
                    <a href="/impressum" class="hover:text-white transition">Impressum</a>
                    <a href="/datenschutz" class="hover:text-white transition">Datenschutz</a>
                    <a href="/agb" class="hover:text-white transition">AGB</a>
                    <a href="/dmca" class="hover:text-white transition">DMCA</a>
                </div>
            </div>
        </div>
    </footer>'''


FOOTER_RE = re.compile(r'<footer class="border-t border-white/10 py-16">.*?</footer>', re.S)
COUNTRY_SEP = '<option disabled>──────────</option>'
COUNTRY_SCRIPT = '<script src="/form-countries.js"></script>'


def apply_sitewide(page):
    """Shared footer + short inline country list (rest is added by JS)."""
    page = FOOTER_RE.sub(lambda m: render_footer(), page, count=1)
    # Keep DACH inline; drop the ~200 other <option>s from the HTML.
    page = re.sub(re.escape(COUNTRY_SEP) + r'.*?(?=\s*</select>)', COUNTRY_SEP, page, count=1, flags=re.S)
    if COUNTRY_SEP in page and COUNTRY_SCRIPT not in page:
        page = page.replace('<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>',
                            COUNTRY_SCRIPT + '\n    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>', 1)
    return page


# ============================================================
# FRAGMENT PARSING
# ============================================================
def parse_fragment(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'\s*<!--meta\s*(\{.*?\})\s*-->', raw, re.S)
    if not m:
        raise SystemExit(f'{path}: missing <!--meta {{...}} --> header')
    meta = json.loads(m.group(1))
    rest = raw[m.end():]
    if '<!--faq-->' not in rest:
        raise SystemExit(f'{path}: missing <!--faq--> marker')
    body, faq_raw = rest.split('<!--faq-->', 1)
    faqs = []
    for q, a in re.findall(r'<h3>(.*?)</h3>\s*((?:<p>.*?</p>\s*)+)', faq_raw, re.S):
        faqs.append((strip_tags(q), a.strip()))
    if len(faqs) < 4:
        raise SystemExit(f'{path}: needs at least 4 FAQ entries, found {len(faqs)}')
    return meta, body.strip(), faqs


def add_heading_ids(body):
    used = set()
    toc = []

    def slug(t):
        t = strip_tags(t).lower()
        for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
            t = t.replace(a, b)
        t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60].strip('-')
        base, n = t or 'abschnitt', 2
        while t in used:
            t = f'{base}-{n}'
            n += 1
        used.add(t)
        return t

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if 'id=' in attrs:
            return m.group(0)
        i = slug(inner)
        toc.append((i, strip_tags(inner)))
        return f'<h2 id="{i}"{attrs}>{inner}</h2>'

    body = re.sub(r'<h2([^>]*)>(.*?)</h2>', repl, body, flags=re.S)
    return body, toc


# ============================================================
# RENDERING
# ============================================================
def render_content(meta, body, faqs, slug):
    en = meta.get('lang') == 'en'
    body, toc = add_heading_ids(body)
    toc_html = ''
    if len(toc) >= 4:
        lis = '\n'.join(f'                    <li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
        toc_html = f'''
            <nav class="toc" aria-label="{'Contents' if en else 'Inhaltsverzeichnis'}">
                <p class="toc-title">{'Contents' if en else 'Inhalt'}</p>
                <ol>
{lis}
                </ol>
            </nav>'''
    faq_items = '\n'.join(f'''                <div class="faq-item glass rounded-2xl overflow-hidden slide-up">
                    <button class="faq-toggle w-full text-left px-6 py-4 flex items-center justify-between font-semibold">
                        <span>{esc(q)}</span>
                        <span class="faq-icon text-2xl transition-transform">+</span>
                    </button>
                    <div class="faq-content hidden px-6 pb-5 faq-answer">
                        {a}
                    </div>
                </div>''' for q, a in faqs)
    related = [s for s in meta.get('related', []) if s in PAGES and s != slug]
    for s in related:
        if not os.path.exists(os.path.join(ROOT, s + '.html')) and not os.path.exists(os.path.join(ROOT, 'content', s + '.html')):
            print(f'WARNING {slug}: related page {s} does not exist yet')
    cards = '\n'.join(f'''                <a href="/{s}" class="related-card glass rounded-2xl">
                    <span class="related-title">{esc(PAGES[s][0])}</span>
                    <span class="related-desc">{esc(PAGES[s][2])}</span>
                </a>''' for s in related)
    related_html = ''
    if cards:
        related_html = f'''
    <!-- ======== RELATED ======== -->
    <section class="py-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-2xl sm:text-3xl font-black mb-6 text-center">{'Related guides' if en else 'Passende Anleitungen'}</h2>
            <div class="related-grid">
{cards}
            </div>
        </div>
    </section>
'''
    return f'''<!-- ======== SEO CONTENT ======== -->
    <section class="py-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <p class="updated-note">{'Updated' if en else 'Aktualisiert am'} {TODAY[8:10]}.{TODAY[5:7]}.{TODAY[0:4]} · {'IPTV Deutschland editorial team' if en else 'Redaktion IPTV Deutschland'}</p>{toc_html}
            <article class="seo-prose">
{body}
            </article>
        </div>
    </section>

    <!-- ======== FAQ ======== -->
    <section class="py-12">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-2xl sm:text-3xl font-black mb-8 text-center slide-up">{'Frequently asked questions' if en else 'Häufige Fragen'}</h2>
            <div class="space-y-4">
{faq_items}
            </div>
        </div>
    </section>
{related_html}
    <!-- ======== OTHER PLANS ======== -->'''


def faq_schema(faqs):
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in faqs],
    }


def breadcrumb_schema(slug, meta):
    items = [('Startseite', f'{SITE}/de/')]
    hub = HUBS.get(PAGES.get(slug, ('', meta.get('hub'), ''))[1] or meta.get('hub', ''))
    if hub and hub[1] and hub[1] != '/' + slug:
        items.append((hub[0], SITE + hub[1]))
    items.append((meta['breadcrumb'], f'{SITE}/{slug}'))
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u}
                            for i, (n, u) in enumerate(items)],
    }


def about_entity(slug, meta):
    if 'about' in meta:
        a = dict(meta['about'])
        t = a.pop('type', 'Thing')
        out = {'@type': t, 'name': a.pop('name', meta['breadcrumb'])}
        if 'os' in a:
            out['operatingSystem'] = a.pop('os')
        if t == 'SoftwareApplication':
            out['applicationCategory'] = 'MultimediaApplication'
        out.update(a)
        return out
    hub = PAGES.get(slug, ('', '', ''))[1]
    if hub == 'apps':
        return {'@type': 'SoftwareApplication', 'name': meta['breadcrumb'], 'applicationCategory': 'MultimediaApplication'}
    return {'@type': 'Thing', 'name': meta['breadcrumb']}


def webpage_schema(page, slug, meta):
    pub = re.search(r'"datePublished": "([^"]*)"', page)
    hub = PAGES.get(slug, ('', '', ''))[1]
    obj = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': meta['breadcrumb'],
        'headline': meta.get('h1', meta['title']),
        'url': f'{SITE}/{slug}',
        'description': meta['description'],
        'inLanguage': 'en' if meta.get('lang') == 'en' else 'de-DE',
        'datePublished': pub.group(1) if pub else TODAY,
        'dateModified': TODAY,
        'isPartOf': {'@type': 'WebSite', 'name': 'iptvv.de', 'url': f'{SITE}/de/'},
        'publisher': {'@type': 'Organization', 'name': 'IPTV Deutschland', 'url': f'{SITE}/de/',
                      'logo': {'@type': 'ImageObject', 'url': f'{SITE}/germany-icon.png'}},
        'about': about_entity(slug, meta),
    }
    img = re.search(r'<meta property="og:image" content="([^"]*)"', page)
    if img:
        obj['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': img.group(1)}
    if hub in ('apps', 'geraete', 'ratgeber'):
        obj['@type'] = ['WebPage', 'TechArticle'] if hub != 'ratgeber' else ['WebPage', 'Article']
        obj['author'] = {'@type': 'Organization', 'name': 'Redaktion IPTV Deutschland', 'url': f'{SITE}/de/'}
    return obj


def replace_ld(page, typ, obj):
    pat = re.compile(r'<script type="application/ld\+json">\{\s*"@context": "https://schema.org",\s*"@type": (?:"' + typ + r'"|\[\s*"' + typ + r'"[^\]]*\]).*?</script>', re.S)
    if not pat.search(page):
        raise SystemExit(f'no {typ} JSON-LD found')
    return pat.sub(lambda m: json_block(obj), page, count=1)


def set_meta(page, attr, name, value):
    pat = re.compile(r'(<meta ' + attr + '="' + re.escape(name) + r'" content=")[^"]*(">)')
    if not pat.search(page):
        raise SystemExit(f'meta {name} not found')
    return pat.sub(lambda m: m.group(1) + esc(value) + m.group(2), page, count=1)


def clone_base(slug, meta):
    # Read the base page from git so a rebuilt iptv-extreme.html can't change the clone source.
    page = subprocess.run(['git', 'show', BASE_REF + ':' + BASE_PAGE], cwd=ROOT, check=True,
                          capture_output=True).stdout.decode('utf-8')
    page = page.replace(f'{SITE}/iptv-extreme', f'{SITE}/{slug}')
    page = page.replace('Frage%20zu%20IPTV%20Extreme.', 'Frage%20zu%20' + meta['device'].replace(' ', '%20') + '.')
    page = page.replace('"name": "IPTV Extreme – IPTV Deutschland"', '"name": ' + json.dumps(meta['breadcrumb'] + ' – IPTV Deutschland', ensure_ascii=False))
    page = page.replace('"name": "IPTV Extreme",\n  "url"', '"name": ' + json.dumps(meta['breadcrumb'], ensure_ascii=False) + ',\n  "url"')
    page = page.replace('"datePublished": "2026-01-01"', f'"datePublished": "{TODAY}"')
    page = page.replace('<input type="hidden" name="device" value="IPTV Extreme">',
                        f'<input type="hidden" name="device" value="{esc(meta["device"])}">')
    page = page.replace('<input type="hidden" name="plan" value="IPTV Abo – ab 9 EUR">',
                        f'<input type="hidden" name="plan" value="{esc(meta["device"])} – ab 9 EUR">')
    page = re.sub(r'<link rel="alternate" hreflang="de" href="[^"]*">',
                  f'<link rel="alternate" hreflang="de" href="{SITE}/{slug}">', page)
    return page


def build(slug):
    frag = os.path.join(ROOT, 'content', slug + '.html')
    meta, body, faqs = parse_fragment(frag)
    required = ('title', 'description', 'breadcrumb') if meta.get('keep_hero') else \
        ('title', 'description', 'h1', 'badge', 'hero_sub', 'lead', 'breadcrumb')
    for k in required:
        if not meta.get(k):
            raise SystemExit(f'{slug}: meta.{k} missing')
    out = os.path.join(ROOT, slug + '.html')
    if os.path.exists(out):
        page = open(out, encoding='utf-8').read()
    else:
        meta.setdefault('device', meta['breadcrumb'])
        page = clone_base(slug, meta)

    # ---- head ----
    page = re.sub(r'<title>.*?</title>', '<title>' + esc(meta['title']) + '</title>', page, count=1)
    page = set_meta(page, 'name', 'description', meta['description'])
    page = re.sub(r'\s*<meta name="keywords" content="[^"]*">', '', page, count=1)
    page = set_meta(page, 'property', 'og:title', meta['title'])
    page = set_meta(page, 'property', 'og:description', meta['description'])
    page = set_meta(page, 'name', 'twitter:title', meta['title'])
    page = set_meta(page, 'name', 'twitter:description', meta['description'])
    page = re.sub(r'(<meta name="robots" content=")[^"]*(">)',
                  r'\1index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1\2', page, count=1)
    page = re.sub(r'("@type": "Product",\s*"name": "[^"]*",\s*"description": )"[^"]*"',
                  lambda m: m.group(1) + json.dumps(meta['description'], ensure_ascii=False), page, count=1)
    page = replace_ld(page, 'WebPage', webpage_schema(page, slug, meta))
    lang = meta.get('lang', 'de')
    page = re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', page, count=1)
    page = re.sub(r'<link rel="alternate" hreflang="(de|en)" href=', f'<link rel="alternate" hreflang="{lang}" href=', page, count=1)
    page = re.sub(r'(<meta property="og:locale" content=")[^"]*(">)', r'\g<1>' + ('en_GB' if lang == 'en' else 'de_DE') + r'\g<2>', page, count=1)
    page = replace_ld(page, 'FAQPage', faq_schema(faqs))
    page = replace_ld(page, 'BreadcrumbList', breadcrumb_schema(slug, meta))
    if 'href="content.css"' not in page:
        page = page.replace('<link rel="stylesheet" href="style.css">',
                            '<link rel="stylesheet" href="style.css">\n    <link rel="stylesheet" href="content.css">', 1)

    # ---- hero ---- (pages with their own hero layout, like iptv-preise, keep it)
    if not meta.get('keep_hero'):
        page = update_hero(page, meta, slug)

    # ---- content + FAQ + related ----
    pat = re.compile(r'<!-- ======== SEO CONTENT ======== -->.*?<!-- ======== OTHER PLANS ======== -->', re.S)
    if not pat.search(page):
        # pages without the plans strip: content runs up to the footer
        pat = re.compile(r'<!-- ======== SEO CONTENT ======== -->.*?(?=\n<footer|\n    <!-- ======== FOOTER)', re.S)
        if not pat.search(page):
            raise SystemExit(f'{slug}: content markers not found')
        page = pat.sub(lambda m: render_content(meta, body, faqs, slug).rsplit('<!--', 1)[0].rstrip() + '\n', page, count=1)
    else:
        page = pat.sub(lambda m: render_content(meta, body, faqs, slug), page, count=1)
    return finish(page, meta, body, faqs, slug, out)


def update_hero(page, meta, slug):
    page = re.sub(r'(<span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>\s*<span class="text-sm text-gray-300">)[^<]*(</span>)',
                  lambda m: m.group(1) + esc(meta['badge']) + m.group(2), page, count=1)
    page = re.sub(r'(<h1 class="[^"]*">).*?(</h1>)', lambda m: m.group(1) + esc(meta['h1']) + m.group(2), page, count=1, flags=re.S)
    page = re.sub(r'(<p class="text-sm text-gray-400 text-center sm:text-right mt-3">)[^<]*(</p>)',
                  lambda m: m.group(1) + esc(meta['hero_sub']) + m.group(2), page, count=1)
    lead = f'<p class="hero-lead">{meta["lead"]}</p>'
    if 'class="hero-lead"' in page:
        page = re.sub(r'<p class="hero-lead">.*?</p>', lambda m: lead, page, count=1, flags=re.S)
    else:
        page = re.sub(r'(<p class="text-sm text-gray-500">\+1,5 Millionen[^<]*</p>)',
                      lambda m: lead + '\n            ' + m.group(1), page, count=1)
        if 'class="hero-lead"' not in page:
            raise SystemExit(f'{slug}: could not place hero lead')

    return page


def finish(page, meta, body, faqs, slug, out):
    page = apply_sitewide(page)
    if slug != 'iptv-extreme':
        own = body + ' '.join(q + a for q, a in faqs) + json.dumps(meta, ensure_ascii=False)
        leftovers = [l.strip() for l in page.splitlines()
                     if 'Extreme' in l and '/iptv-extreme' not in l and l.strip() not in own and 'Extreme' not in own]
        if leftovers:
            raise SystemExit(f'{slug}: base-page text left over: {leftovers[:3]}')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    return out


def write_sitemap():
    """sitemap.xml = every indexable page, by clean URL. Pages whose file
    didn't change keep their previous lastmod."""
    old = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    prev = dict(re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', old))
    rebuilt = {SITE + '/' + os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'content', '*.html'))}
    urls = [(SITE + '/de/', prev.get(SITE + '/de/', TODAY), 'daily', '1.0')]
    for p in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(p)[:-5]
        if name.startswith('_') or name.startswith('google') or name in ('404', 'index'):
            continue
        if re.search(r'<meta name="robots" content="[^"]*noindex', open(p, encoding='utf-8').read()):
            continue
        url = f'{SITE}/{name}'
        hub = PAGES.get(name, ('', '', ''))[1]
        prio = '0.9' if name in ('iptv-abo', 'iptv-preise', 'iptv-kostenlos-testen') else '0.8' if hub in ('apps', 'geraete', 'kauf') else '0.7'
        urls.append((url, TODAY if url in rebuilt else prev.get(url, TODAY), 'monthly', prio))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, cf, pr in urls:
        out += ['  <url>', f'    <loc>{u}</loc>', f'    <lastmod>{lm}</lastmod>',
                f'    <changefreq>{cf}</changefreq>', f'    <priority>{pr}</priority>', '  </url>']
    out.append('</urlset>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'sitemap.xml: {len(urls)} URLs')


def main(argv):
    slugs = argv or sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'content', '*.html')))
    for s in slugs:
        build(s)
        print('built', s)
    if not argv:
        # shared footer + short country list on every other page too
        for p in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'de', '*.html')):
            old = open(p, encoding='utf-8').read()
            new = apply_sitewide(old)
            if new != old:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(new)
        write_sitemap()


if __name__ == '__main__':
    main(sys.argv[1:])
