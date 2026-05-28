import os, re, copy

# ── Full price matrix (EUR, matching the $ values 1:1) ──
prices = {
    1:  {'1-monat': 9,   '3-monate': 29,  '6-monate': 39,  '1-jahr': 49},
    2:  {'1-monat': 18,  '3-monate': 50,  '6-monate': 69,  '1-jahr': 89},
    3:  {'1-monat': 27,  '3-monate': 75,  '6-monate': 105, '1-jahr': 135},
    4:  {'1-monat': 36,  '3-monate': 99,  '6-monate': 140, '1-jahr': 180},
    5:  {'1-monat': 45,  '3-monate': 120, '6-monate': 175, '1-jahr': 225},
    6:  {'1-monat': 54,  '3-monate': 144, '6-monate': 210, '1-jahr': 270},
    7:  {'1-monat': 63,  '3-monate': 168, '6-monate': 245, '1-jahr': 315},
    8:  {'1-monat': 72,  '3-monate': 192, '6-monate': 280, '1-jahr': 360},
    9:  {'1-monat': 81,  '3-monate': 216, '6-monate': 315, '1-jahr': 405},
    10: {'1-monat': 90,  '3-monate': 240, '6-monate': 350, '1-jahr': 450},
}

durations = ['1-monat', '3-monate', '6-monate', '1-jahr']
dur_labels = {'1-monat': '1 Monat', '3-monate': '3 Monate', '6-monate': '6 Monate', '1-jahr': '1 Jahr'}

def slug(d): return d  # e.g. "1-monat"
def gerat_slug(n): return '1-gerat' if n == 1 else f'{n}-gerate'
def fmt(p): return f'{p},00'   # e.g. 9 -> "9,00"
def fmt_schema(p): return f'{p}.00'

def gerat_label(n):
    return '1 Gerät' if n == 1 else f'{n} Geräte'

def file_slug(dur, n):
    return f'{dur}-{gerat_slug(n)}'

def pill_row(dur, n):
    lines = []
    for d in durations:
        p = prices[n][d]
        path = f'/{file_slug(d, n)}.html'
        active = 'active' if d == dur else ''
        lines.append(f'<a href="{path}" class="dur-pill {active}">{dur_labels[d]} — {fmt(p)}€</a>')
    return '\n'.join(lines)

def cross_sell_pills(dur, n):
    # Show all durations for this device count, plus jump to different device count
    lines = []
    for d in durations:
        p = prices[n][d]
        path = f'/{file_slug(d, n)}.html'
        star = ' ⭐' if d == '1-jahr' else ''
        lines.append(f'<a href="{path}" class="plan-pill">{dur_labels[d]} · {gerat_label(n)} — {fmt(p)}€{star}</a>')
    # add a few cross-device links
    if n < 10:
        nn = n + 1
        p = prices[nn]['1-monat']
        lines.append(f'<a href="/{file_slug("1-monat", nn)}.html" class="plan-pill">{gerat_label(nn)} ab {fmt(p)}€</a>')
    lines.append('<a href="/preise.html" class="plan-pill">Alle Preise →</a>')
    return '\n        '.join(lines)

# Read template (1-monat-1-gerat.html)
with open('public/1-monat-1-gerat.html') as f:
    template = f.read()

def make_page(dur, n):
    p = prices[n][dur]
    p_fmt = fmt(p)
    p_schema = fmt_schema(p)
    d_label = dur_labels[dur]
    g_label = gerat_label(n)
    g_slug = gerat_slug(n)
    fslug = file_slug(dur, n)
    canonical = f'https://mojo4k.de/{fslug}'
    plan_name = f'IPTV {d_label} – {g_label}'
    plan_name_full = f'{plan_name} – {p_fmt}€'

    html = template

    # ── title / meta ──
    html = re.sub(r'<title>[^<]+</title>', f'<title>{plan_name} | {p_fmt}€ | MOJO4K.DE</title>', html)
    html = re.sub(r'(<meta name="description" content=")[^"]+(")', 
        f'\\g<1>IPTV Abonnement {d_label} für {g_label} nur {p_fmt}€. 50.000+ Kanäle, 4K Qualität, Bundesliga & Sky inklusive. Keine Bindung. Sofortige Aktivierung.\\2', html)
    html = re.sub(r'(<link rel="canonical" href=")[^"]+(")', f'\\g<1>{canonical}\\2', html)
    html = re.sub(r'(<meta property="og:title" content=")[^"]+(")', f'\\g<1>{plan_name} | {p_fmt}€ | MOJO4K.DE\\2', html)
    html = re.sub(r'(<meta property="og:description" content=")[^"]+(")',
        f'\\g<1>IPTV Abonnement {d_label} für {g_label} nur {p_fmt}€. 50.000+ Kanäle, 4K Qualität, Bundesliga & Sky inklusive.\\2', html)

    # ── JSON-LD schema ──
    html = re.sub(
        r'"name":"MOJO4K\.DE [^"]*"',
        f'"name":"MOJO4K.DE {plan_name}"', html)
    html = re.sub(
        r'"description":"IPTV Abonnement [^"]*"',
        f'"description":"IPTV Abonnement {d_label} für {g_label} nur {p_fmt}€. 50.000+ Kanäle, 4K Qualität, Bundesliga & Sky inklusive. Keine Bindung. Sofortige Aktivierung."', html)
    html = re.sub(r'"price":"[0-9]+\.[0-9]+"', f'"price":"{p_schema}"', html, count=1)
    html = re.sub(r'"url":"https://mojo4k\.de/[^"]*"', f'"url":"{canonical}"', html, count=1)

    # ── eyebrow ──
    html = re.sub(r'MOJO4K\.DE &middot; [^<]+', f'MOJO4K.DE &middot; {g_label}', html)

    # ── H1 ──
    html = re.sub(r'<h1>[^<]+</h1>', f'<h1>{plan_name}</h1>', html)

    # ── price display ──
    html = re.sub(r'<span class="plan-price-num">[^<]+</span>', f'<span class="plan-price-num">{p_fmt}€</span>', html)

    # ── duration pills (active pill + links) ──
    html = re.sub(
        r'(<div class="duration-pills">)(.*?)(</div>)',
        f'\\g<1>\n      {pill_row(dur, n)}\n    \\g<3>',
        html, flags=re.DOTALL)

    # ── hidden plan field in form ──
    html = re.sub(
        r'(<input type="hidden" name="plan" value=")[^"]*(")',
        f'\\g<1>{plan_name_full}\\2', html)

    # ── cross-sell pills ──
    html = re.sub(
        r'(<div class="plans-pill-row">)(.*?)(</div>)',
        f'\\g<1>\n        {cross_sell_pills(dur, n)}\n      \\g<3>',
        html, flags=re.DOTALL)

    return html

# ── Generate / update all 40 plan pages (4 durations × 10 devices) ──
created, updated = 0, 0
for n in range(1, 11):
    for dur in durations:
        fname = f'public/{file_slug(dur, n)}.html'
        content = make_page(dur, n)
        exists = os.path.exists(fname)
        with open(fname, 'w') as f:
            f.write(content)
        if exists:
            updated += 1
        else:
            created += 1
            print(f'  CREATED: {fname}')

print(f'\nDone — updated {updated} existing pages, created {created} new pages')

# ── Also update the -iptv.html redirect files for new device counts ──
redirect_template = '''<!DOCTYPE html><html><head><meta charset="UTF-8"/><meta name="robots" content="noindex, nofollow"/>
<meta http-equiv="refresh" content="0;url=/{slug}.html"/>
<title>Weiterleitung...</title>
<link rel="canonical" href="https://mojo4k.de/{slug}"/>
</head><body></body></html>'''

r_created = 0
for n in range(6, 11):
    for dur in durations:
        sl = file_slug(dur, n)
        fname = f'public/{sl}-iptv.html'
        if not os.path.exists(fname):
            with open(fname, 'w') as f:
                f.write(redirect_template.replace('{slug}', sl))
            r_created += 1

print(f'Created {r_created} new redirect files')
