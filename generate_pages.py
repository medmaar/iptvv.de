import re

TEMPLATE = open('_template.html', encoding='utf-8').read()

# ============================================================
# PRICING MATRIX (matches homepage iptvPlans JS object)
# ============================================================
PRICES = {
    1: {'monthly': 9,  'three': 29,  'six': 39,  'year': 49},
    2: {'monthly': 18, 'three': 50,  'six': 69,  'year': 89},
    3: {'monthly': 27, 'three': 75,  'six': 105, 'year': 135},
    4: {'monthly': 36, 'three': 99,  'six': 140, 'year': 180},
    5: {'monthly': 45, 'three': 120, 'six': 175, 'year': 225},
}
DURATION_MONTHS = {'monthly': 1, 'three': 3, 'six': 6, 'year': 12}
DURATION_ORDER = ['monthly', 'three', 'six', 'year']
DEVICE_ORDER = [1, 2, 3, 4, 5]

def device_slug(n):
    return '1-geraet' if n == 1 else f'{n}-geraete'

def device_label(n):
    return '1 Gerät' if n == 1 else f'{n} Geräte'

DURATION_LABEL = {'monthly': '1 Monat', 'three': '3 Monate', 'six': '6 Monate', 'year': '1 Jahr'}
DURATION_SLUG = {'monthly': '1-monat', 'three': '3-monate', 'six': '6-monate', 'year': '1-jahr'}

# ============================================================
# DEVICE-SPECIFIC CONTENT BLOCKS
# ============================================================
DEVICE_CONTENT = {
    1: {
        'persona': 'Einzelnutzer',
        'seo_html': '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4">IPTV Abo für <span class="text-gradient">1 Gerät</span></h2>
            <p class="text-gray-400 leading-relaxed mb-6">Sie streamen allein auf einem Fernseher, Smartphone oder Tablet? Dann ist 1 Gerät genau richtig für Sie. Egal ob Sie eine <strong>smart ip tv</strong> App auf Ihrem Samsung- oder LG-Fernseher nutzen, eine <strong>iptv box</strong> bzw. einen <strong>iptv stick</strong> anschließen oder lieber über eine <strong>ip tv app</strong> auf einem <strong>iptv android</strong> Handy schauen – Ihr Stream läuft stabil und in voller 4K-Qualität.</p>
        ''',
        'faq': ('Reicht 1 Gerät für mich aus?',
                'Wenn Sie alleine streamen oder immer nur auf einem Bildschirm gleichzeitig schauen, ist das 1-Geräte-Paket ausreichend. Möchten Sie später erweitern, können Sie jederzeit auf ein Paket mit mehr Geräten wechseln.'),
    },
    2: {
        'persona': 'Paare & 2-Personen-Haushalte',
        'seo_html': '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4">IPTV Abo für <span class="text-gradient">2 Geräte</span></h2>
            <p class="text-gray-400 leading-relaxed mb-6">Ideal für Paare oder 2-Personen-Haushalte: Mit diesem <strong>iptv abo</strong> können zwei Personen gleichzeitig auf unterschiedlichen Geräten streamen – zum Beispiel einer im Wohnzimmer auf dem Smart TV, die andere unterwegs auf dem Handy. Als zuverlässiger <strong>iptv anbieter</strong> in <strong>deutschland iptv</strong> sorgen wir dafür, dass beide Streams gleichzeitig stabil und ruckelfrei laufen.</p>
        ''',
        'faq': ('Können beide Geräte gleichzeitig unterschiedliche Programme schauen?',
                'Ja, mit dem 2-Geräte-Paket können zwei unabhängige Streams gleichzeitig laufen – jede Person kann ihr eigenes Programm schauen.'),
    },
    3: {
        'persona': 'kleine Familien',
        'seo_html': '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4">IPTV Abo für <span class="text-gradient">3 Geräte</span></h2>
            <p class="text-gray-400 leading-relaxed mb-6">Perfekt für kleine Familien: Mit 3 gleichzeitigen Verbindungen können Eltern und Kind unabhängig voneinander schauen – auf dem Smart TV im Wohnzimmer, einer <strong>iptv box android</strong> im Kinderzimmer und einem Tablet. Egal ob über eine <strong>ip tv box</strong> oder eine App – alle drei Streams laufen parallel in 4K.</p>
        ''',
        'faq': ('Funktionieren alle 3 Geräte auch in unterschiedlichen Räumen?',
                'Ja, die Geräte müssen nicht im selben Raum oder am selben WLAN hängen – Hauptsache, jedes Gerät hat eine stabile Internetverbindung.'),
    },
    4: {
        'persona': 'die ganze Familie',
        'seo_html': '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4">IPTV Abo für <span class="text-gradient">4 Geräte</span></h2>
            <p class="text-gray-400 leading-relaxed mb-6">Für die ganze Familie gemacht: Mit 4 gleichzeitigen Verbindungen schaut jeder, was er möchte – ob Bundesliga im Wohnzimmer, Serien im Schlafzimmer oder Zeichentrickfilme im Kinderzimmer. Kompatibel mit <strong>iptv fire tv</strong> Sticks, <strong>iptv sticks</strong> generell, Smart TVs und Smartphones in jedem Raum.</p>
        ''',
        'faq': ('Brauche ich für jedes Gerät einen eigenen Account?',
                'Nein, Sie erhalten Zugangsdaten, mit denen Sie auf bis zu 4 Geräten gleichzeitig streamen können – ganz ohne separate Accounts.'),
    },
    5: {
        'persona': 'Großfamilien & WGs',
        'seo_html': '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4">IPTV Abo für <span class="text-gradient">5 Geräte</span></h2>
            <p class="text-gray-400 leading-relaxed mb-6">Unser größtes Geräte-Paket eignet sich für Großfamilien, WGs oder Haushalte mit mehreren Fernsehern. Als <strong>bester iptv anbieter</strong> für umfangreiche <strong>iptv subscription</strong> Bedürfnisse ermöglichen wir 5 gleichzeitige Streams – stabil, in 4K und ohne dass sich die Nutzer gegenseitig beim Streaming stören.</p>
        ''',
        'faq': ('Eignet sich das 5-Geräte-Paket auch für mehrere Wohnungen?',
                'Ja, solange die Geräte jeweils über eine eigene Internetverbindung verfügen, spielt der Standort keine Rolle.'),
    },
}

# ============================================================
# DURATION-SPECIFIC CONTENT BLOCKS
# ============================================================
DURATION_CONTENT = {
    'monthly': {
        'eyebrow': 'IPTV Test ohne Risiko',
        'badge_html': '',
        'seo_html': '''
            <h3 class="text-xl font-bold mb-3 mt-8 text-white">1 Monat Laufzeit – der ideale IPTV Test</h3>
            <p class="text-gray-400 leading-relaxed mb-4">Wer nach <strong>iptv kaufen</strong>, <strong>iptv test</strong> oder <strong>iptv free trial</strong> sucht, möchte meist einen Anbieter zuerst unverbindlich ausprobieren. Das 1-Monats-Abo läuft automatisch aus und verlängert sich nicht von selbst – perfekt, um unsere Qualität ohne Risiko kennenzulernen, bevor Sie sich für eine längere Laufzeit entscheiden.</p>
        ''',
        'faq': ('Verlängert sich das 1-Monats-Abo automatisch?',
                'Nein. Das Abo läuft nach einem Monat automatisch aus. Sie entscheiden danach selbst, ob und mit welcher Laufzeit Sie verlängern möchten.'),
    },
    'three': {
        'eyebrow': 'Meistgewählter Einstieg',
        'badge_html': '',
        'seo_html': '''
            <h3 class="text-xl font-bold mb-3 mt-8 text-white">3 Monate Laufzeit – german IPTV in bester Qualität</h3>
            <p class="text-gray-400 leading-relaxed mb-4">Drei Monate reichen für eine ganze Bundesliga-Hinrunde, mehrere Serien-Staffeln und zahlreiche Filme – ohne sich gleich für ein Jahr zu binden. Als verlässlicher <strong>iptv anbieter</strong> für <strong>german iptv</strong> liefern wir Ihnen über diesen Zeitraum alle deutschen Sender, internationale Kanäle und eine riesige <strong>iptv playlist deutsch</strong> mit VOD-Inhalten.</p>
        ''',
        'faq': ('Kann ich nach 3 Monaten auf eine längere Laufzeit wechseln?',
                'Ja, Sie können jederzeit vor Ablauf auf ein 6-Monats- oder Jahresabo verlängern und sparen dabei zusätzlich.'),
    },
    'six': {
        'eyebrow': '🔥 Unser beliebtestes Paket',
        'badge_html': '''                <div class="popular-badge">
                    <span class="gradient-blue text-white text-xs font-bold px-4 py-1.5 rounded-full">🔥 BELIEBTESTE LAUFZEIT</span>
                </div>''',
        'seo_html': '''
            <h3 class="text-xl font-bold mb-3 mt-8 text-white">6 Monate Laufzeit – bester IPTV Anbieter im Vergleich</h3>
            <p class="text-gray-400 leading-relaxed mb-4">Im <strong>iptv anbieter vergleich</strong> überzeugt unser 6-Monats-Abo mit dem besten Verhältnis aus Preis, Stabilität und Funktionsumfang. Statt sich in einem anonymen <strong>iptv forum</strong> durch widersprüchliche Empfehlungen zu wühlen, erhalten Sie bei uns transparente Preise, PPV-Events und direkten Support über WhatsApp – als <strong>bester iptv anbieter</strong> für alle, die Wert auf Zuverlässigkeit legen.</p>
        ''',
        'faq': ('Warum ist die 6-Monats-Laufzeit so beliebt?',
                'Sie bietet das beste Verhältnis aus Preis pro Monat und Flexibilität – ohne sich gleich für ein ganzes Jahr zu binden.'),
    },
    'year': {
        'eyebrow': '💰 Bester Preis pro Monat',
        'badge_html': '''                <div class="popular-badge">
                    <span class="bg-yellow-500 text-black text-xs font-bold px-4 py-1.5 rounded-full">💰 BESTER PREIS + BONUS</span>
                </div>''',
        'seo_html': '''
            <h3 class="text-xl font-bold mb-3 mt-8 text-white">1 Jahr Laufzeit – maximale Ersparnis + gratis Bonus</h3>
            <p class="text-gray-400 leading-relaxed mb-4">Für alle, die dauerhaft <strong>beste iptv</strong> Qualität wollen, ist das Jahresabo am günstigsten – der niedrigste Preis pro Monat im gesamten Sortiment. Egal ob Sie mit <strong>iptv smarters pro</strong>, <strong>kodi xbmc iptv</strong> oder über <strong>iptv fire tv</strong> streamen: Mit 12 Monaten Laufzeit müssen Sie sich ein ganzes Jahr lang um nichts kümmern.</p>
            <div class="bg-yellow-500/10 border border-yellow-500/30 rounded-2xl p-4 my-6 flex items-center gap-3">
                <span class="text-2xl">⭐</span>
                <div>
                    <p class="font-bold text-sm text-yellow-400 leading-tight">IBO Player Pro Premium Abo</p>
                    <p class="text-xs text-gray-400">kostenlos inklusive bei jedem 1-Jahres-Abo</p>
                </div>
            </div>
        ''',
        'faq': ('Was ist im gratis IBO Player Pro Bonus enthalten?',
                'Mit jedem 1-Jahres-Abo erhalten Sie ein IBO Player Pro Premium Abo komplett kostenlos dazu – ideal für besonders stabiles Streaming auf unterstützten Geräten.'),
    },
}

# ============================================================
# SHARED CONTENT (same across all 20 pages)
# ============================================================
SHARED_COMPAT_HTML = '''
            <h3 class="text-xl font-bold mb-3 mt-8 text-white">Kompatible Apps & Geräte</h3>
            <p class="text-gray-400 leading-relaxed mb-4">Unser IPTV Abo funktioniert mit allen gängigen Apps und Geräten: IPTV Smarters Pro, TiviMate, GSE Smart IPTV, VLC Player sowie Kodi/XBMC über ein IPTV-Addon. Unterstützte Geräte sind Android, iOS, Fire TV Stick, Smart TVs (Samsung, LG), MAG-Boxen und PC/Mac. Die Einrichtung dauert in der Regel nur wenige Minuten – unser 24/7 Support hilft bei Bedarf kostenlos weiter.</p>
'''

SHARED_FAQ_1 = ('Wie schnell wird mein IPTV Abo nach der Bestellung aktiviert?',
                 'In der Regel innerhalb weniger Minuten nach Zahlungseingang. Sie erhalten Ihre Zugangsdaten per WhatsApp oder E-Mail.')
SHARED_FAQ_2 = ('Auf welchen Geräten funktioniert mein IPTV Abo?',
                 'Auf allen gängigen Geräten: Smart TV, Fire TV Stick, Android/iOS, MAG Box, PC und mehr – über Apps wie IPTV Smarters Pro oder TiviMate.')

print("Content blocks loaded")

# ============================================================
# KEYWORD POOLS (from Germany keyword research)
# ============================================================
DEVICE_KEYWORDS = {
    1: ['ip tv app', 'smart ip tv', 'iptv stick', 'iptv box', 'iptv android'],
    2: ['iptv anbieter', 'iptv abo', 'deutschland iptv'],
    3: ['iptv box android', 'ip tv box', 'iptv sticks'],
    4: ['iptv fire tv', 'fire tv iptv', 'iptv sticks'],
    5: ['bester iptv anbieter', 'iptv subscription'],
}
DURATION_KEYWORDS = {
    'monthly': ['iptv test', 'iptv free trial', 'iptv trial', 'kostenlos iptv'],
    'three': ['german iptv', 'deutschland iptv', 'iptv playlist deutsch', 'iptv abo'],
    'six': ['iptv anbieter', 'bester iptv anbieter', 'iptv anbieter vergleich', 'beste iptv'],
    'year': ['beste iptv', 'best iptv', 'iptv subscription', 'iptv smarters pro', 'kodi xbmc iptv'],
}
CORE_KEYWORDS = ['iptv kaufen', 'iptv anbieter', 'iptv deutschland']

# ============================================================
# COUNTRY DIAL-CODE LIST (German names), Germany pinned + selected
# ============================================================
PINNED_COUNTRIES = [
    ('Deutschland', '49'),
    ('Österreich', '43'),
    ('Schweiz', '41'),
]

WORLD_COUNTRIES = [
    ('Afghanistan', '93'), ('Ägypten', '20'), ('Albanien', '355'), ('Algerien', '213'),
    ('Andorra', '376'), ('Angola', '244'), ('Argentinien', '54'), ('Armenien', '374'),
    ('Aserbaidschan', '994'), ('Äthiopien', '251'), ('Australien', '61'), ('Bahamas', '1242'),
    ('Bahrain', '973'), ('Bangladesch', '880'), ('Barbados', '1246'), ('Belarus', '375'),
    ('Belgien', '32'), ('Belize', '501'), ('Benin', '229'), ('Bhutan', '975'),
    ('Bolivien', '591'), ('Bosnien und Herzegowina', '387'), ('Botsuana', '267'), ('Brasilien', '55'),
    ('Brunei', '673'), ('Bulgarien', '359'), ('Burkina Faso', '226'), ('Burundi', '257'),
    ('Chile', '56'), ('China', '86'), ('Costa Rica', '506'), ('Dänemark', '45'),
    ('Dominikanische Republik', '1849'), ('Dschibuti', '253'), ('Ecuador', '593'), ('El Salvador', '503'),
    ('Elfenbeinküste', '225'), ('Eritrea', '291'), ('Estland', '372'), ('Eswatini', '268'),
    ('Fidschi', '679'), ('Finnland', '358'), ('Frankreich', '33'), ('Gabun', '241'),
    ('Gambia', '220'), ('Georgien', '995'), ('Ghana', '233'), ('Griechenland', '30'),
    ('Grenada', '1473'), ('Guatemala', '502'), ('Guinea', '224'), ('Guinea-Bissau', '245'),
    ('Guyana', '592'), ('Haiti', '509'), ('Honduras', '504'), ('Indien', '91'),
    ('Indonesien', '62'), ('Irak', '964'), ('Iran', '98'), ('Irland', '353'),
    ('Island', '354'), ('Israel', '972'), ('Italien', '39'), ('Jamaika', '1876'),
    ('Japan', '81'), ('Jemen', '967'), ('Jordanien', '962'), ('Kambodscha', '855'),
    ('Kamerun', '237'), ('Kanada', '1'), ('Kap Verde', '238'), ('Kasachstan', '7'),
    ('Katar', '974'), ('Kenia', '254'), ('Kirgisistan', '996'), ('Kiribati', '686'),
    ('Kolumbien', '57'), ('Komoren', '269'), ('Kongo', '242'), ('Kosovo', '383'),
    ('Kroatien', '385'), ('Kuba', '53'), ('Kuwait', '965'), ('Laos', '856'),
    ('Lesotho', '266'), ('Lettland', '371'), ('Libanon', '961'), ('Liberia', '231'),
    ('Libyen', '218'), ('Liechtenstein', '423'), ('Litauen', '370'), ('Luxemburg', '352'),
    ('Madagaskar', '261'), ('Malawi', '265'), ('Malaysia', '60'), ('Malediven', '960'),
    ('Mali', '223'), ('Malta', '356'), ('Marokko', '212'), ('Mauretanien', '222'),
    ('Mauritius', '230'), ('Mexiko', '52'), ('Moldau', '373'), ('Monaco', '377'),
    ('Mongolei', '976'), ('Montenegro', '382'), ('Mosambik', '258'), ('Myanmar', '95'),
    ('Namibia', '264'), ('Nepal', '977'), ('Neuseeland', '64'), ('Nicaragua', '505'),
    ('Niederlande', '31'), ('Niger', '227'), ('Nigeria', '234'), ('Nordkorea', '850'),
    ('Nordmazedonien', '389'), ('Norwegen', '47'), ('Oman', '968'), ('Pakistan', '92'),
    ('Palästina', '970'), ('Panama', '507'), ('Papua-Neuguinea', '675'), ('Paraguay', '595'),
    ('Peru', '51'), ('Philippinen', '63'), ('Polen', '48'), ('Portugal', '351'),
    ('Ruanda', '250'), ('Rumänien', '40'), ('Russland', '7'), ('Sambia', '260'),
    ('Samoa', '685'), ('San Marino', '378'), ('Saudi-Arabien', '966'), ('Schweden', '46'),
    ('Senegal', '221'), ('Serbien', '381'), ('Seychellen', '248'), ('Sierra Leone', '232'),
    ('Simbabwe', '263'), ('Singapur', '65'), ('Slowakei', '421'), ('Slowenien', '386'),
    ('Somalia', '252'), ('Spanien', '34'), ('Sri Lanka', '94'), ('Südafrika', '27'),
    ('Sudan', '249'), ('Südkorea', '82'), ('Südsudan', '211'), ('Suriname', '597'),
    ('Syrien', '963'), ('Tadschikistan', '992'), ('Taiwan', '886'), ('Tansania', '255'),
    ('Thailand', '66'), ('Togo', '228'), ('Tonga', '676'), ('Trinidad und Tobago', '1868'),
    ('Tschad', '235'), ('Tschechien', '420'), ('Tunesien', '216'), ('Türkei', '90'),
    ('Turkmenistan', '993'), ('Uganda', '256'), ('Ukraine', '380'), ('Ungarn', '36'),
    ('Uruguay', '598'), ('Usbekistan', '998'), ('Vanuatu', '678'), ('Venezuela', '58'),
    ('Vereinigte Arabische Emirate', '971'), ('Vereinigte Staaten (USA)', '1'), ('Vereinigtes Königreich (UK)', '44'),
    ('Vietnam', '84'), ('Zentralafrikanische Republik', '236'), ('Zypern', '357'),
]

def render_country_options():
    out = []
    for name, code in PINNED_COUNTRIES:
        selected = ' selected' if name == 'Deutschland' else ''
        out.append(f'                                <option value="{name}" data-code="{code}"{selected}>{name} (+{code})</option>')
    out.append('                                <option disabled>──────────</option>')
    for name, code in WORLD_COUNTRIES:
        out.append(f'                                <option value="{name}" data-code="{code}">{name} (+{code})</option>')
    out.append('                                <option value="Andere" data-code="">Andere</option>')
    return '\n'.join(out)

COUNTRY_OPTIONS_HTML = render_country_options()
print(f"Country list built: {len(PINNED_COUNTRIES) + len(WORLD_COUNTRIES) + 1} countries")

def dedupe(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

# ============================================================
# HELPERS
# ============================================================
def faq_html(items):
    out = []
    for q, a in items:
        out.append(f'''                <div class="faq-item glass rounded-2xl overflow-hidden slide-up">
                    <button class="faq-toggle w-full text-left px-6 py-4 flex items-center justify-between font-semibold">
                        <span>{q}</span>
                        <span class="faq-icon text-2xl transition-transform">+</span>
                    </button>
                    <div class="faq-content hidden px-6 pb-5">
                        <p class="text-gray-400 leading-relaxed text-sm">{a}</p>
                    </div>
                </div>''')
    return '\n'.join(out)

def faq_jsonld(items):
    out = []
    for i, (q, a) in enumerate(items):
        q_clean = re.sub('<[^<]+?>', '', q).replace('"', "'")
        a_clean = re.sub('<[^<]+?>', '', a).replace('"', "'")
        comma = ',' if i < len(items) - 1 else ''
        out.append('            { "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }%s' % (q_clean, a_clean, comma))
    return '\n'.join(out)

def keyword_footer(keywords):
    return ' · '.join(dedupe(keywords))

def render_page(replacements, out_path):
    html = TEMPLATE
    for token, value in replacements.items():
        html = html.replace(token, value)
    leftover = re.findall(r'__[A-Z_]+__', html)
    if leftover:
        print(f"WARNING: leftover tokens in {out_path}: {set(leftover)}")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Wrote {out_path} ({len(html)} chars)")

# ============================================================
# GENERATE THE 20 DEVICE x DURATION PAGES
# ============================================================
ALL_SLUGS = []  # (slug, plan_name, price) for cross-linking
for device in DEVICE_ORDER:
    for duration in DURATION_ORDER:
        slug = f'iptv-kaufen-{device_slug(device)}-{DURATION_SLUG[duration]}'
        price = PRICES[device][duration]
        plan_name = f'{DURATION_LABEL[duration]} IPTV Abo für {device_label(device)}'
        ALL_SLUGS.append((slug, plan_name, price, device, duration))

for slug, plan_name, price, device, duration in ALL_SLUGS:
    dc = DEVICE_CONTENT[device]
    duc = DURATION_CONTENT[duration]
    months = DURATION_MONTHS[duration]

    canonical_url = f'https://iptvv.de/{slug}.html'
    title = f'{plan_name} – {price}€ | IPTV Deutschland'
    meta_desc = f'{DURATION_LABEL[duration]} IPTV Abo für {device_label(device)} – {price}€. +50.000 Kanäle, +300.000 Filme & Serien, 4K Qualität, VPN-freundlich. Jetzt unverbindlich anfragen!'
    meta_keywords = ', '.join(dedupe(CORE_KEYWORDS + DEVICE_KEYWORDS[device] + DURATION_KEYWORDS[duration]))
    og_title = f'{plan_name} – {price}€'
    og_desc = f'IPTV kaufen: {DURATION_LABEL[duration]} für {device_label(device)} – nur {price}€. +50.000 Kanäle, +300.000 Filme & Serien in 4K.'

    if months == 1:
        price_note = f'{device_label(device)} · einmalig {price}€'
    else:
        rate = price / months
        rate_str = f'{rate:.2f}'.replace('.', ',')
        price_note = f'{device_label(device)} · {rate_str} €/Monat'

    wa_suffix = f'%20{DURATION_LABEL[duration].replace(" ", "%20")}%20IPTV%20Abo%20für%20{device_label(device).replace(" ", "%20")}.'

    faq_items = [SHARED_FAQ_1, SHARED_FAQ_2, dc['faq'], duc['faq']]
    seo_html = dc['seo_html'] + duc['seo_html'] + SHARED_COMPAT_HTML

    other_links = []
    # link to same device, other durations (3) + same duration, other devices (up to 2 for variety)
    for s2, name2, price2, d2, dur2 in ALL_SLUGS:
        if s2 == slug:
            continue
        if d2 == device and dur2 != duration:
            other_links.append((s2, name2, price2))
    for s2, name2, price2, d2, dur2 in ALL_SLUGS:
        if d2 != device and dur2 == duration and len(other_links) < 6:
            other_links.append((s2, name2, price2))

    other_plans_html_parts = []
    for s2, name2, price2 in other_links[:6]:
        other_plans_html_parts.append(
            f'                <a href="{s2}.html" class="glass rounded-2xl px-5 py-3 hover:bg-white/10 transition-all">\n'
            f'                    <span class="block font-bold text-sm">{name2}</span>\n'
            f'                    <span class="block text-xs text-gray-400">{price2}€</span>\n'
            f'                </a>'
        )

    replacements = {
        '__TITLE__': title,
        '__META_DESC__': meta_desc,
        '__META_KEYWORDS__': meta_keywords,
        '__CANONICAL_URL__': canonical_url,
        '__OG_TITLE__': og_title,
        '__OG_DESC__': og_desc,
        '__PLAN_NAME__': plan_name,
        '__PLAN_PRICE__': str(price),
        '__PLAN_PRICE_RAW__': str(price),
        '__PLAN_PRICE_RAW_LABEL__': f'{price} € ({device_label(device)}, {DURATION_LABEL[duration]})',
        '__PLAN_CURRENCY__': '€',
        '__PLAN_PRICE_NOTE__': price_note,
        '__PLAN_DEVICE_LABEL__': device_label(device),
        '__PLAN_EYEBROW__': duc['eyebrow'],
        '__PLAN_BADGE_HTML__': duc['badge_html'],
        '__PLAN_WA_SUFFIX__': wa_suffix,
        '__SEO_CONTENT_HTML__': seo_html,
        '__FAQ_HTML__': faq_html(faq_items),
        '__FAQ_JSONLD__': faq_jsonld(faq_items),
        '__OTHER_PLANS_HEADING__': 'Andere Pakete ansehen',
        '__OTHER_PLANS_HTML__': '\n'.join(other_plans_html_parts),
        '__KEYWORD_FOOTER_LINE__': keyword_footer(meta_keywords.split(', ')),
        '__COUNTRY_OPTIONS__': COUNTRY_OPTIONS_HTML,
    }

    render_page(replacements, f'{slug}.html')

print(f"\nGenerated {len(ALL_SLUGS)} device x duration pages")

# ============================================================
# GENERATE FREE TRIAL PAGE
# ============================================================
trial_title = 'IPTV Kostenlos Testen – Gratis IPTV Test | IPTV Deutschland'
trial_meta_desc = 'IPTV gratis testen ohne Risiko: Fordern Sie jetzt einen unverbindlichen IPTV Test an und erleben Sie +50.000 Kanäle, +300.000 Filme & Serien in 4K Qualität selbst.'
trial_meta_keywords = ', '.join(dedupe(CORE_KEYWORDS + ['iptv test', 'iptv free trial', 'iptv trial', 'iptv gratis testen', 'kostenlos iptv', 'testline iptv', 'iptv test line', 'iptv line test', 'german iptv', 'iptv kaufe', 'best iptv', 'beste iptv', 'iptv germany', 'germany iptv', 'iptv german', 'deutschland iptv', 'smarters iptv pro', 'iptv smarters pro', 'iptv extreme', 'app iptv', 'application iptv android', 'ip tv app']))
trial_og_title = 'IPTV Kostenlos Testen – Unverbindlicher IPTV Test'
trial_og_desc = 'Testen Sie IPTV Deutschland unverbindlich: +50.000 Kanäle, +300.000 Filme & Serien, 4K Qualität – ohne Risiko.'

trial_faq = [
    ('Ist der IPTV Test wirklich kostenlos?', 'Ja, Sie können unseren Service unverbindlich testen, bevor Sie sich für ein kostenpflichtiges Abo entscheiden. Füllen Sie einfach das Formular aus und wir melden uns bei Ihnen.'),
    SHARED_FAQ_2,
    ('Muss ich nach dem Test automatisch kaufen?', 'Nein, der Test ist komplett unverbindlich. Es entstehen keine automatischen Kosten oder Verpflichtungen.'),
    ('Wie lange dauert der IPTV Test?', 'In der Regel erhalten Sie kurzfristig nach Ihrer Anfrage Zugang, um unsere Kanäle, die Bildqualität und Stabilität selbst zu prüfen.'),
]

trial_seo_html = '''
            <h2 class="text-2xl sm:text-3xl font-black mb-4"><span class="text-gradient">IPTV gratis testen</span> – ganz ohne Risiko</h2>
            <p class="text-gray-400 leading-relaxed mb-4">Wer bei Google nach <strong>iptv free trial</strong>, <strong>iptv trial</strong> oder <strong>iptv gratis testen</strong> sucht, hat meist schon einmal schlechte Erfahrungen mit unzuverlässigen Anbietern gemacht. Statt eines instabilen Gratis-Streams aus zweifelhafter Quelle bieten wir einen echten, unverbindlichen <strong>iptv test</strong> an – damit Sie unsere Qualität selbst beurteilen können, bevor Sie sich für ein <strong>iptv kaufen</strong> Angebot entscheiden.</p>
            <p class="text-gray-400 leading-relaxed mb-6">Füllen Sie einfach das Formular weiter unten aus. Unser Team meldet sich kurzfristig bei Ihnen über WhatsApp oder E-Mail und richtet Ihren Test ein – mit echten Zugangsdaten zu unserem vollen Programm, nicht nur einer eingeschränkten Demo.</p>

            <h3 class="text-xl font-bold mb-3 mt-8 text-white">Was Sie beim IPTV Test erwartet</h3>
            <ul class="space-y-2 mb-6 text-gray-400">
                <li class="flex items-start gap-2"><span class="text-green-400 mt-1">✓</span><span>+50.000 Live-Kanäle inkl. deutscher Sender</span></li>
                <li class="flex items-start gap-2"><span class="text-green-400 mt-1">✓</span><span>+300.000 Filme & Serien (VOD)</span></li>
                <li class="flex items-start gap-2"><span class="text-green-400 mt-1">✓</span><span>4K Ultra HD Qualität mit Anti-Freeze-Technologie</span></li>
                <li class="flex items-start gap-2"><span class="text-green-400 mt-1">✓</span><span>Kompatibel mit Smart TV, Fire TV Stick, Android, iOS & mehr</span></li>
            </ul>
            <p class="text-gray-400 leading-relaxed mb-4">Überzeugt? Im Anschluss können Sie ganz einfach eines unserer <a href="index.html#preise" class="text-green-400 hover:text-green-300 underline">IPTV Abos</a> ab 9€ buchen – mit Laufzeiten von 1 Monat bis 1 Jahr und 1 bis 5 Geräten gleichzeitig.</p>
''' + SHARED_COMPAT_HTML

trial_other_links = []
for s2, name2, price2 in [(slug, pn, pr) for slug, pn, pr, d, dur in ALL_SLUGS if d == 1]:
    trial_other_links.append(
        f'                <a href="{s2}.html" class="glass rounded-2xl px-5 py-3 hover:bg-white/10 transition-all">\n'
        f'                    <span class="block font-bold text-sm">{name2}</span>\n'
        f'                    <span class="block text-xs text-gray-400">{price2}€</span>\n'
        f'                </a>'
    )

trial_replacements = {
    '__TITLE__': trial_title,
    '__META_DESC__': trial_meta_desc,
    '__META_KEYWORDS__': trial_meta_keywords,
    '__CANONICAL_URL__': 'https://iptvv.de/iptv-kostenlos-testen.html',
    '__OG_TITLE__': trial_og_title,
    '__OG_DESC__': trial_og_desc,
    '__PLAN_NAME__': 'IPTV Kostenlos Testen',
    '__PLAN_PRICE__': 'Kostenlos',
    '__PLAN_PRICE_RAW__': '0',
    '__PLAN_PRICE_RAW_LABEL__': 'Kostenloser IPTV Test (unverbindlich)',
    '__PLAN_CURRENCY__': '',
    '__PLAN_PRICE_NOTE__': 'unverbindlich · ohne Risiko · keine automatische Verlängerung',
    '__PLAN_DEVICE_LABEL__': 'noch offen',
    '__PLAN_EYEBROW__': 'Unverbindlicher IPTV Test',
    '__PLAN_BADGE_HTML__': '',
    '__PLAN_WA_SUFFIX__': '%20kostenlosen%20IPTV%20Test.',
    '__SEO_CONTENT_HTML__': trial_seo_html,
    '__FAQ_HTML__': faq_html(trial_faq),
    '__FAQ_JSONLD__': faq_jsonld(trial_faq),
    '__OTHER_PLANS_HEADING__': 'Bereit zu kaufen? Pakete für 1 Gerät ansehen',
    '__OTHER_PLANS_HTML__': '\n'.join(trial_other_links),
    '__KEYWORD_FOOTER_LINE__': keyword_footer(trial_meta_keywords.split(', ')),
    '__COUNTRY_OPTIONS__': COUNTRY_OPTIONS_HTML,
}

render_page(trial_replacements, 'iptv-kostenlos-testen.html')
print("\nDone — 20 plan pages + 1 trial page = 21 total")



# ============================================================
# GENERATE CITY PAGES
# ============================================================
def slugify_city(name):
    repl = {'ü': 'ue', 'ö': 'oe', 'ä': 'ae', 'ß': 'ss', 'Ü': 'Ue', 'Ö': 'Oe', 'Ä': 'Ae'}
    s = name
    for k, v in repl.items():
        s = s.replace(k, v)
    return s.lower().replace(' ', '-')

CITIES = ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart',
          'Düsseldorf', 'Leipzig', 'Dortmund', 'Dresden', 'Hannover', 'Nürnberg']

city_slugs = [(c, f'iptv-{slugify_city(c)}') for c in CITIES]

city_faq_template = [
    ('Funktioniert IPTV Deutschland auch in {city}?',
     'Ja, unser Service funktioniert über das Internet und ist daher in {city} und ganz Deutschland gleichermaßen verfügbar – unabhängig von Kabel- oder Satellitenanschluss.'),
    SHARED_FAQ_1,
    SHARED_FAQ_2,
    ('Welche Internetgeschwindigkeit brauche ich in {city}?',
     'Für ein optimales Streaming-Erlebnis empfehlen wir mindestens 10 Mbit/s für HD und 25 Mbit/s für 4K Inhalte – das ist in {city} mit den meisten DSL-, Kabel- oder Glasfaseranschlüssen problemlos erreichbar.'),
]

for city, slug in city_slugs:
    canonical_url = f'https://iptvv.de/{slug}.html'
    title = f'IPTV {city} – IPTV Anbieter in {city} | iptvv.de'
    meta_desc = f'IPTV {city} ab 9€/Monat. Über +50.000 Kanäle, +300.000 Filme & Serien in 4K Qualität. Bester IPTV Anbieter in {city} – jetzt unverbindlich anfragen!'
    meta_keywords = ', '.join(dedupe(CORE_KEYWORDS + [
        f'iptv {city.lower()}', f'iptv anbieter {city.lower()}', f'{city.lower()} iptv',
        'germany iptv', 'deutschland iptv', 'german iptv', 'bester iptv anbieter',
        'iptv abo', 'smart ip tv', 'iptv box', 'iptv stick'
    ]))
    og_title = f'IPTV {city} – Bester IPTV Anbieter'
    og_desc = f'IPTV {city} ab 9€/Monat. +50.000 Kanäle, +300.000 Filme & Serien in 4K Qualität.'

    seo_html = f'''
            <h2 class="text-2xl sm:text-3xl font-black mb-4"><span class="text-gradient">IPTV {city}</span> – Ihr lokaler Streaming-Anbieter</h2>
            <p class="text-gray-400 leading-relaxed mb-4">Wer in <strong>{city}</strong> nach einem zuverlässigen <strong>iptv anbieter</strong> sucht, ist bei IPTV Deutschland richtig. Als bundesweiter <strong>germany iptv</strong> Anbieter beliefern wir auch Kunden in {city} mit über 50.000 Live-Kanälen, deutschen Sendern, Bundesliga, Sky Sport und DAZN sowie einer riesigen VOD-Bibliothek mit über 300.000 Filmen und Serien – alles in 4K Ultra HD Qualität.</p>
            <p class="text-gray-400 leading-relaxed mb-6">Da unser Service komplett über das Internet läuft, spielt Ihr Standort innerhalb {city}s keine Rolle. Egal ob Mitte, Vorort oder Umland – mit einer stabilen Internetverbindung sind Sie in wenigen Minuten startklar.</p>
''' + SHARED_COMPAT_HTML

    other_links = []
    for c2, s2 in city_slugs:
        if s2 != slug:
            other_links.append((s2, f'IPTV {c2}', None))
        if len(other_links) >= 5:
            break
    other_plans_html_parts = []
    for s2, name2, _ in other_links:
        other_plans_html_parts.append(
            f'                <a href="{s2}.html" class="glass rounded-2xl px-5 py-3 hover:bg-white/10 transition-all">\n'
            f'                    <span class="block font-bold text-sm">{name2}</span>\n'
            f'                </a>'
        )
    other_plans_html_parts.append(
        '                <a href="iptv-preise.html" class="glass rounded-2xl px-5 py-3 hover:bg-white/10 transition-all">\n'
        '                    <span class="block font-bold text-sm">Alle Preise & Pakete</span>\n'
        '                </a>'
    )

    faq_items = [(q.format(city=city), a.format(city=city)) if '{city}' in q or '{city}' in a else (q, a)
                 for q, a in city_faq_template]

    replacements = {
        '__TITLE__': title,
        '__META_DESC__': meta_desc,
        '__META_KEYWORDS__': meta_keywords,
        '__CANONICAL_URL__': canonical_url,
        '__OG_TITLE__': og_title,
        '__OG_DESC__': og_desc,
        '__PLAN_NAME__': f'IPTV {city}',
        '__PLAN_PRICE__': 'ab 9',
        '__PLAN_PRICE_RAW__': '9',
        '__PLAN_PRICE_RAW_LABEL__': f'IPTV Abo in {city} (ab 9 €)',
        '__PLAN_CURRENCY__': '€ / Monat',
        '__PLAN_PRICE_NOTE__': 'Alle Laufzeiten verfügbar – 1 bis 12 Monate, 1 bis 5 Geräte',
        '__PLAN_DEVICE_LABEL__': 'Alle Geräte',
        '__PLAN_EYEBROW__': f'IPTV Anbieter in {city}',
        '__PLAN_BADGE_HTML__': '',
        '__PLAN_WA_SUFFIX__': f'%20IPTV%20Abo%20in%20{city}.',
        '__SEO_CONTENT_HTML__': seo_html,
        '__FAQ_HTML__': faq_html(faq_items),
        '__FAQ_JSONLD__': faq_jsonld(faq_items),
        '__OTHER_PLANS_HEADING__': 'Weitere Städte & alle Preise ansehen',
        '__OTHER_PLANS_HTML__': '\n'.join(other_plans_html_parts),
        '__KEYWORD_FOOTER_LINE__': keyword_footer(meta_keywords.split(', ')),
        '__COUNTRY_OPTIONS__': COUNTRY_OPTIONS_HTML,
    }

    render_page(replacements, f'{slug}.html')

print(f"\nGenerated {len(city_slugs)} city pages")
