# -*- coding: utf-8 -*-
"""넥서스도시랩 정적 사이트 빌더 — 한국어/영어/일본어 페이지 생성

사용법: 이 폴더에서 `python3 build.py`
- 한국어: about.html, 영어: about-en.html, 일본어: about-ja.html (모두 같은 폴더)
- 문구는 content.py, 실적 목록은 records.json에서 고칩니다.
"""
import json, random, html, os
from urllib.parse import quote
from content import T, LANGS, CATS, TITLES, ORGS, PARTNER_FILES, AREA_IDS, AREA_ICONS, AREA_EN

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
RECORDS = json.load(open(os.path.join(HERE, 'records.json'), encoding='utf-8'))
esc = html.escape

PAGES = ['index', 'about', 'greeting', 'vision', 'partners', 'business', 'history', 'records', 'contact', '404']


def href(page, lang):
    """'business#area-1' → 'business-en.html#area-1'"""
    base, sep, rest = page.partition('#')
    if not sep:
        base, sep, rest = page.partition('?')
    name = base + ('' if lang == 'ko' else '-' + lang) + '.html'
    return name + (sep + rest if sep else '')


def rec_title(r, lang):
    return r[2] if lang == 'ko' else TITLES[r[2]][LANGS.index(lang) - 1]


def rec_org(r, lang):
    return r[3] if lang == 'ko' else ORGS[r[3]][LANGS.index(lang) - 1]


def recs_by(cat):
    return [r for r in RECORDS if r[1] == cat]


def n_orgs():
    s = set()
    for r in RECORDS:
        for o in r[3].replace('，', ',').split(','):
            s.add(o.strip())
    return len(s)


# ───────── icons ─────────
ICONS = {
    'h2': '<svg class="ico icon" viewBox="0 0 64 64" aria-hidden="true"><circle cx="21" cy="30" r="11"/><circle cx="43" cy="30" r="11"/><path d="M17 25v10M25 25v10M17 30h8M39 25v10M47 25v10M39 30h8"/><path class="a" d="M8 54h48"/></svg>',
    'leaf': '<svg class="ico icon" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 50C14 26 30 12 52 12c0 24-14 38-38 38z"/><path class="a" d="M14 50L38 26"/><path d="M26 38h10M31 33v10" class="a"/></svg>',
    'city': '<svg class="ico icon" viewBox="0 0 64 64" aria-hidden="true"><path d="M8 54h48M12 54V28h14v26M26 54V14h16v40M42 54V32h10v22"/><path class="a" d="M31 21h6M31 28h6M31 35h6M31 42h6M17 35h4M17 42h4"/></svg>',
    'rnd': '<svg class="ico icon" viewBox="0 0 64 64" aria-hidden="true"><path d="M26 10h12M28 10v16L14 50a3 3 0 002.6 4.5h30.8A3 3 0 0050 50L36 26V10"/><path class="a" d="M20 40h24"/><circle class="a" cx="30" cy="46" r="2"/><circle class="a" cx="38" cy="44" r="1.5"/></svg>',
    'globe': '<svg class="ico icon" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="22"/><path class="a" d="M10 32h44M32 10c7 7 10 14 10 22s-3 15-10 22c-7-7-10-14-10-22s3-15 10-22z"/></svg>',
    'badge': '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6l20 8v14c0 14-9 24-20 30C21 52 12 42 12 28V14z"/><path class="a" d="M23 31l7 7 12-13"/></svg>',
    'doc': '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><path d="M16 8h22l12 12v36H16z"/><path d="M38 8v12h12"/><path class="a" d="M23 32h20M23 40h20M23 48h12"/></svg>',
    'link': '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><circle cx="18" cy="32" r="8"/><circle cx="46" cy="18" r="8"/><circle cx="46" cy="46" r="8"/><path class="a" d="M25 28l14-7M25 36l14 7"/></svg>',
}
ARROW = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
HOME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 11l9-7 9 7M5 9.5V20h5v-6h4v6h5V9.5"/></svg>'
GLOBE_SM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/></svg>'

# ───────── art ─────────
def skyline(seed, w, base, hmin, hmax, x0=0, windows=True, op=.16):
    rnd = random.Random(seed)
    out, x = [], x0
    while x < w:
        bw = rnd.choice([34, 42, 50, 58, 70, 86])
        bh = rnd.randint(hmin, hmax)
        out.append(f'<rect x="{x}" y="{base-bh}" width="{bw}" height="{bh}"/>')
        if windows and bh > 90:
            for wy in range(base - bh + 18, base - 14, 22):
                for wx in range(x + 9, x + bw - 8, 12):
                    if rnd.random() < .22:
                        out.append(f'<rect class="w" x="{wx}" y="{wy}" width="3" height="6"/>')
        if rnd.random() < .12:
            out.append(f'<path d="M{x+bw/2} {base-bh}v-{rnd.randint(18,40)}"/>')
        x += bw + rnd.choice([0, 4, 8, 14])
    return (f'<g fill="none" stroke="#fff" stroke-opacity="{op}" stroke-width="1">'
            f'<style>.w{{fill:#8FC6CF;fill-opacity:.35;stroke:none}}</style>' + ''.join(out) + '</g>')

def turbine(x, y, s=1, op=.22):
    return (f'<g stroke="#fff" stroke-opacity="{op}" fill="none" stroke-width="1" transform="translate({x} {y}) scale({s})">'
            '<path d="M0 0V-150"/><path d="M0 -150l-4 -58M0 -150l52 26M0 -150l-48 30"/><circle cx="0" cy="-150" r="3"/></g>')

def tank(x, y, r, op=.22):
    return (f'<g stroke="#fff" stroke-opacity="{op}" fill="none" stroke-width="1">'
            f'<circle cx="{x}" cy="{y-r-24}" r="{r}"/><path d="M{x-r*.6} {y}l{r*.3} -{24+r*.2}M{x+r*.6} {y}l-{r*.3} -{24+r*.2}"/>'
            f'<path d="M{x-r} {y-r-24}h{2*r}" stroke-dasharray="2 4"/></g>')

GRAD = ('<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#127478" stop-opacity="0"/><stop offset=".25" stop-color="#1E9598"/>'
        '<stop offset=".7" stop-color="#8FC6CF"/><stop offset="1" stop-color="#8FC6CF" stop-opacity=".2"/></linearGradient>'
        '<radialGradient id="glow" cx=".72" cy=".62" r=".6"><stop offset="0" stop-color="#1E9598" stop-opacity=".28"/>'
        '<stop offset="1" stop-color="#1E9598" stop-opacity="0"/></radialGradient></defs>')

def n_pipe(x, base, top, r):
    d = f'M-40 {base}H{x}'
    d += f'V{top}a{r} {r} 0 0 1 {2*r} 0V{base-60}a{r} {r} 0 0 0 {2*r} 0V{top}a{r} {r} 0 0 1 {2*r} 0V{base}'
    return d, x + 6 * r

def hero_art():
    base = 700
    parts = ['<svg class="art" viewBox="0 0 1440 800" preserveAspectRatio="xMaxYMax slice" aria-hidden="true">', GRAD,
             '<rect width="1440" height="800" fill="url(#glow)"/>',
             skyline(7, 1480, base, 40, 250, x0=700, op=.13) + skyline(3, 700, base, 20, 90, x0=-20, windows=False, op=.08)]
    parts += [turbine(1360, base - 190, .9), turbine(1420, base - 230, 1.1), turbine(760, base - 120, .7)]
    parts += [tank(560, base, 34), tank(640, base, 26)]
    d, _ = n_pipe(980, base - 40, base - 250, 56)
    parts.append(f'<path class="pipe-glow" pathLength="1" d="{d}H1500" fill="none" stroke="#8FC6CF" stroke-opacity=".18" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append(f'<path class="pipe" pathLength="1" d="{d}H1500" fill="none" stroke="url(#pg)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append(f'<path d="M-40 {base}H1480" stroke="#fff" stroke-opacity=".25"/>')
    for i, (cx, cy) in enumerate([(980 + 56, base - 250 - 56), (980 + 56 * 5, base - 250 - 56), (700, base - 40), (1390, base - 40)]):
        parts.append(f'<g class="node" style="animation-delay:{1.4 + i*.35}s"><circle cx="{cx}" cy="{cy}" r="5" fill="#8FC6CF"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#8FC6CF" stroke-opacity=".4"/></g>')
    parts.append('</svg>')
    return ''.join(parts)

def sub_art(seed):
    base = 340
    d, _ = n_pipe(1090, base - 22, base - 170, 34)
    return (f'<svg class="art" viewBox="0 0 1440 340" preserveAspectRatio="xMaxYMax slice" aria-hidden="true">{GRAD}'
            '<rect width="1440" height="340" fill="url(#glow)"/>' + skyline(seed, 1480, base, 30, 190, x0=520, op=.12) +
            f'<path d="{d}H1500" fill="none" stroke="url(#pg)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ───────── per-language helpers ─────────
def nav(L, lang):
    """NAV with the records menu expanded into category links."""
    out = []
    for k, en, intro, items in L['nav']:
        items = list(items)
        if items[0][1] == 'records':
            items += [(esc(L['cats'][c]), 'records?cat=' + quote(c)) for c in CATS]
        out.append((k, en, intro, [(t, href(u, lang)) for t, u in items]))
    return out


def lang_switch(L, lang, page, cls):
    links = ''.join(
        f'<a href="{href(page, o)}" hreflang="{o}" lang="{o}"' + (' aria-current="true"' if o == lang else '') +
        f' title="{T[o]["label"]}">{T[o]["short"]}</a>' for o in LANGS)
    return f'<nav class="{cls}" aria-label="{L["lang_aria"]}">{GLOBE_SM}{links}</nav>'


def header(L, lang, page, current):
    NAV = nav(L, lang)
    lis = ''.join(f'<li{" class=\"is-current\"" if i == current else ""}><a href="{items[0][1]}">{k}</a></li>'
                  for i, (k, en, intro, items) in enumerate(NAV))
    cols = ''.join(f'<div><h3>{k}</h3>' + ''.join(f'<a href="{u}">{t}</a>' for t, u in items) + '</div>' for k, en, intro, items in NAV)
    drawer = ''.join(f'<details{" open" if i == current else ""}><summary>{k}</summary><ul>' +
                     ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in items) + '</ul></details>'
                     for i, (k, en, intro, items) in enumerate(NAV))
    alt = L['logo_alt']
    return f'''<a class="skip" href="#main">{L['skip']}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{href('index', lang)}" aria-label="{L['brand']} {L['home']}">
      <img class="mark mark-light" src="mark-light.svg" alt="" width="38" height="38">
      <img class="mark mark-dark" src="mark-dark.svg" alt="" width="38" height="38">
      <img class="word word-light" src="wordmark-light.svg" alt="{alt}" width="176" height="30">
      <img class="word word-dark" src="wordmark-dark.svg" alt="{alt}" width="176" height="30">
    </a>
    <nav class="gnb" aria-label="{L['nav_aria']}"><ul>{lis}</ul></nav>
    {lang_switch(L, lang, page, 'lang')}
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" aria-label="{L['menu_open']}" data-label-open="{L['menu_open']}" data-label-close="{L['menu_close']}"><span></span></button>
  </div>
  <div class="mega"><div class="wrap">
    <div class="mega-intro"><strong>{L['mega_strong']}</strong><p>{L['mega_p']}</p></div>
    <div class="mega-cols">{cols}</div>
  </div></div>
</header>
<nav class="drawer" id="drawer" aria-label="{L['mnav_aria']}">{drawer}</nav>'''


def footer(L, lang):
    C = L['company']
    links = ''.join(f'<a href="{href(u, lang)}">{k}</a>' for k, u in L['footer_links'])
    return f'''<footer class="site-footer">
  <div class="top"><div class="wrap">{links}</div></div>
  <div class="main"><div class="wrap">
    <img class="logo" src="wordmark-dark.svg" alt="{L['logo_alt']}" width="200" height="34">
    <div>
      <address>
        <span><b>{L['f_name']}</b>{C['name']}</span><span><b>{L['f_ceo']}</b>{C['ceo']}</span><br>
        <span><b>{L['f_addr']}</b>{C['addr']}</span><span><b>{L['f_tel']}</b><a href="tel:+82314270937">{C['tel']}</a></span>
      </address>
      <p class="copy">© 2026 NEXUS CITY LAB Co., Ltd. All rights reserved.</p>
    </div>
  </div></div>
</footer>
<button class="to-top" type="button" aria-label="{L['to_top']}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
<script src="main.js"></script>'''


FONTS = {
    'ko': '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">',
    'en': '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">',
    'ja': '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap">',
}


def page(L, lang, name, title, desc, body, current=-1, home=False):
    full_title = f'{title} | {L["brand"]}' if title else L['home_title']
    alts = ''.join(f'<link rel="alternate" hreflang="{o}" href="{href(name, o)}">' for o in LANGS)
    doc = f'''<!DOCTYPE html>
<html lang="{L['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{L['brand']}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#0E1C1F">
{alts}
<link rel="icon" type="image/svg+xml" href="mark-light.svg">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS[lang]}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body{' class="is-home"' if home else ''}>
{header(L, lang, name, current)}
<main id="main">
{body}
</main>
{footer(L, lang)}
</body>
</html>
'''
    open(os.path.join(OUT, href(name, lang)), 'w', encoding='utf-8').write(doc)


def sub_top(L, lang, ci, sub_label, sub_page, seed):
    NAV = nav(L, lang)
    k, en, intro, items = NAV[ci]
    kicker = en
    cur = href(sub_page, lang)
    d1 = ''.join(f'<li><a href="{it[3][0][1]}"' + (' aria-current="page"' if i == ci else '') + f'>{it[0]}</a></li>' for i, it in enumerate(NAV))
    sibs = [it for it in items if '#' not in it[1] and '?' not in it[1]]
    d2 = ''.join(f'<li><a href="{u}"' + (' aria-current="page"' if u == cur else '') + f'>{t}</a></li>' for t, u in sibs)
    return f'''<section class="sub-visual">
  {sub_art(seed)}
  <div class="wrap">
    <p class="en-title">{kicker}</p>
    <h1>{k}</h1>
    <p>{intro}</p>
  </div>
</section>
<nav class="location" aria-label="{L['loc_aria']}"><div class="wrap">
  <a class="loc-home" href="{href('index', lang)}" aria-label="{L['home']}">{HOME}</a>
  <div class="loc-drop"><button type="button" aria-expanded="false">{k}</button><ul>{d1}</ul></div>
  <div class="loc-drop"><button type="button" aria-expanded="false">{sub_label}</button><ul>{d2}</ul></div>
</div></nav>'''


def area_list(L, lang):
    return ''.join(f'<li><a href="{href("business#" + AREA_IDS[i], lang)}">{ICONS[AREA_ICONS[i]]}<h3>{a["title"]}</h3><p>{a["short"]}</p>{ARROW}</a></li>'
                   for i, a in enumerate(L['areas']))


def partner_items(L, captions):
    return ''.join(f'<li class="{"tall" if tall else ""}"><img src="{f}" alt="{n}" loading="lazy">' + (f'<span>{n}</span>' if captions else '') + '</li>'
                   for n, (f, tall) in zip(L['partners'], PARTNER_FILES))


# ───────── pages ─────────
def build_home(L, lang):
    recent = [r for r in RECORDS if r[0] == '2025']
    recent_li = ''.join(f'<li><span class="tag">{esc(L["cats"][r[1]])}</span><span class="t">{esc(rec_title(r, lang))}</span><span class="o">{esc(rec_org(r, lang))}</span></li>' for r in recent)
    facts = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in L['facts_home'])
    h1 = ''.join(f'<span>{s}</span>' for s in L['hero_h1'])
    txt = ''.join(f'<p>{p}</p>' for p in L['about_txt'])
    body = f'''<section class="hero">
  {hero_art()}
  <div class="wrap">
    <p class="kicker">{L['hero_kicker']}</p>
    <h1>{h1}</h1>
    <p>{L['hero_p']}</p>
    <div class="actions"><a class="btn fill" href="{href('business', lang)}">{L['hero_btn1']}</a><a class="btn ghost-light" href="{href('records', lang)}">{L['hero_btn2']}</a></div>
  </div>
  <span class="scroll">{L['scroll']}</span>
</section>

<section class="home-sec">
  <div class="wrap">
    <div class="about-intro">
      <div>
        <p class="en" style="color:var(--teal)">About</p>
        <p class="lead">{L['about_lead']}</p>
      </div>
      <div class="txt">
        {txt}
        <a class="btn" href="{href('about', lang)}">{L['about_btn']}</a>
      </div>
    </div>
    <dl class="fact-row">{facts}</dl>
  </div>
</section>

<section class="home-sec alt">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Business</p><h2>{L['sec_business']}</h2></div><a href="{href('business', lang)}">{L['sec_business_link']}</a></div>
    <ul class="area-list">{area_list(L, lang)}</ul>
  </div>
</section>

<section class="home-sec">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Recent Projects</p><h2>{L['sec_recent']}</h2></div><a href="{href('records', lang)}">{L['sec_recent_link']}</a></div>
    <ul class="recent">{recent_li}</ul>
  </div>
</section>

<section class="home-sec alt">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Partners</p><h2>{L['sec_partners']}</h2></div><a href="{href('partners', lang)}">{L['sec_partners_link']}</a></div>
    <ul class="partners">{partner_items(L, False)}</ul>
  </div>
</section>

<section class="cta-band">
  {sub_art(21)}
  <div class="wrap">
    <div><h2>{L['cta_h2']}</h2><p>{L['cta_p']}</p></div>
    <div class="actions"><a class="btn fill" href="tel:+82314270937">{L['company']['tel']}</a><a class="btn ghost-light" href="{href('contact', lang)}">{L['cta_btn2']}</a></div>
  </div>
</section>'''
    page(L, lang, 'index', None, L['home_desc'], body, home=True)


def build_about(L, lang):
    C = L['company']
    rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}' + (f'<small>{c}</small>' if c else '') + '</td></tr>' for a, b, c in L['info_rows'])
    rows += f'<tr><th scope="row">{L["row_addr"]}</th><td>{C["addr"]}</td></tr>'
    rows += f'<tr><th scope="row">{L["row_tel"]}</th><td><a href="tel:+82314270937">{C["tel"]}</a></td></tr>'
    certs = ''.join(f'<div class="cert">{ICONS[ic]}<div><h4>{h}</h4><p>{p}</p></div></div>' for ic, (h, p) in zip(['badge', 'doc'], L['certs']))
    nav0 = L['nav'][0][3]
    body = sub_top(L, lang, 0, nav0[0][0], 'about', 3) + f'''
<div class="page wrap">
  <div class="page-head"><h2>{L['about_h2']}</h2><p>{L['about_p']}</p></div>
  <section class="block">
    <div class="block-title"><h3>{L['b_general']}</h3><span class="en">General</span></div>
    <table class="info-table"><tbody>{rows}</tbody></table>
  </section>
  <section class="block">
    <div class="block-title"><h3>{L['b_cert']}</h3><span class="en">Certification</span></div>
    <div class="cert-list">{certs}</div>
  </section>
  <section class="block">
    <div class="block-title"><h3>{L['b_areas']}</h3><span class="en">Business Areas</span></div>
    <ul class="area-list">{area_list(L, lang)}</ul>
  </section>
</div>'''
    page(L, lang, 'about', L['about_title'], L['about_desc'], body, 0)


def build_greeting(L, lang):
    lead = ''.join(f'<span>{s}</span>' for s in L['greet_lead'])
    paras = ''.join(f'<p>{p}</p>' for p in L['greet_body'])
    body = sub_top(L, lang, 0, L['nav'][0][3][1][0], 'greeting', 5) + f'''
<div class="page wrap">
  <div class="greeting">
    <p class="lead">{lead}</p>
    <div class="body">
      {paras}
      <div class="sign"><span>{L['greet_sign']}</span></div>
    </div>
  </div>
</div>'''
    page(L, lang, 'greeting', L['greet_title'], L['greet_desc'], body, 0)


def build_vision(L, lang):
    goals = ''.join(f'<li>{ICONS[i]}<strong>{t}</strong></li>' for i, t in zip(['h2', 'leaf', 'city'], L['goals']))
    st = ''.join(f'<li>{ICONS[i]}<div><h4>{h}</h4><p>{p}</p></div></li>' for i, (h, p) in zip(['h2', 'badge', 'link', 'globe'], L['strengths']))
    body = sub_top(L, lang, 0, L['nav'][0][3][2][0], 'vision', 9) + f'''
<div class="page wrap">
  <section class="block">
    <div class="block-title"><h3>{L['b_vision']}</h3><span class="en">Vision</span></div>
    <div class="vision-core"><p class="en">Vision</p><p class="big">{L['vision_big']}</p></div>
    <ul class="goals">{goals}</ul>
  </section>
  <section class="block">
    <div class="block-title"><h3>{L['b_strength']}</h3><span class="en">Strengths</span></div>
    <ul class="strengths">{st}</ul>
  </section>
</div>'''
    page(L, lang, 'vision', L['vision_title'], L['vision_desc'], body, 0)


def build_partners(L, lang):
    body = sub_top(L, lang, 0, L['nav'][0][3][3][0], 'partners', 11) + f'''
<div class="page wrap">
  <div class="page-head"><h2>{L['partners_h2']}</h2><p>{L['partners_p']}</p></div>
  <ul class="partners">{partner_items(L, True)}</ul>
</div>'''
    page(L, lang, 'partners', L['partners_title'], L['partners_desc'], body, 0)


def build_business(L, lang):
    tabs = ''.join(f'<a href="#{AREA_IDS[i]}">{a["tab"]}</a>' for i, a in enumerate(L['areas'])) + f'<a href="#process">{L["tab_process"]}</a>'
    cats_for_area = ['수소도시', '탄소중립', '도시·지역개발', '국가 R&D', '국제협력']
    area_html = ''
    for i, a in enumerate(L['areas']):
        cat = cats_for_area[i]
        tasks = ''.join(f'<li>{t}</li>' for t in a['tasks'])
        basis = ''.join(f'<li>{b}</li>' for b in a['basis'])
        label = L['basis_law'] if i < 3 else L['basis_org']
        more = L['more_fmt'].format(cat=esc(L['cats'][cat]), n=len(recs_by(cat)))
        area_html += f'''<section class="area" id="{AREA_IDS[i]}">
  <div class="area-head">{ICONS[AREA_ICONS[i]]}<p class="en">{esc(AREA_EN[i])}</p><h3>{a['title']}</h3></div>
  <div class="area-body">
    <p>{a['desc']}</p>
    <h4>{L['tasks_label']}</h4><ul class="bullets">{tasks}</ul>
    <h4>{label}</h4><ul class="basis">{basis}</ul>
    <a class="more" href="{href('records?cat=' + quote(cat), lang)}">{more}</a>
  </div>
</section>'''
    flow = ''.join(f'<li><span class="step">Step {i+1}</span><h4>{h}</h4><p>{p}</p></li>' for i, (h, p) in enumerate(L['steps']))
    body = sub_top(L, lang, 1, L['nav'][1][3][0][0], 'business', 13) + f'''
<div class="page wrap">
  <p class="statement">{L['statement']}</p>
  <nav class="tabs" aria-label="{L['tabs_aria']}">{tabs}</nav>
  {area_html}
  <section class="block" id="process">
    <div class="block-title"><h3>{L['b_process']}</h3><span class="en">Process</span></div>
    <ol class="flow">{flow}</ol>
  </section>
</div>'''
    page(L, lang, 'business', L['business_title'], L['business_desc'], body, 1)


def build_history(L, lang):
    H = L['hist']

    def year_block(y):
        lis = ''
        for m, t, s, sub in H[y]:
            t = t or L['major']
            sm = f'<small>{s}</small>' if s else ''
            ul = '<ul>' + ''.join(f'<li>{x}</li>' for x in sub) + '</ul>' if sub else ''
            lis += f'<li><span class="m">{m}</span><div class="ev">{t}{sm}{ul}</div></li>'
        return f'<div class="year"><p class="year-num">{y}</p><ol>{lis}</ol></div>'
    eras = [('era-2', '2023 — 2025', L['eras'][0], ['2025', '2024', '2023']),
            ('era-1', '2018 — 2022', L['eras'][1], ['2022', '2021', '2020', '2018'])]
    era_nav = ''.join(f'<a href="#{i}">{r}</a>' for i, r, _, _ in eras)
    era_html = ''.join(f'<section class="era" id="{i}"><div class="era-head"><p class="range">{r}</p><p>{d}</p></div>{"".join(year_block(y) for y in ys)}</section>' for i, r, d, ys in eras)
    body = sub_top(L, lang, 2, L['nav'][2][3][0][0], 'history', 17) + f'''
<div class="page wrap">
  <nav class="era-nav" aria-label="{L['era_aria']}">{era_nav}</nav>
  {era_html}
</div>'''
    page(L, lang, 'history', L['history_title'], L['history_desc'], body, 2)


def build_records(L, lang):
    rows = ''.join(f'<tr data-cat="{esc(r[1])}" data-year="{r[0]}"><td class="y">{r[0]}</td><td class="c"><span class="tag">{esc(L["cats"][r[1]])}</span></td>'
                   f'<td class="t">{esc(rec_title(r, lang))}</td><td class="o">{esc(rec_org(r, lang))}</td></tr>' for r in reversed(RECORDS))
    chips = f'<button type="button" data-cat="all" aria-pressed="true">{L["all"]}</button>' + ''.join(
        f'<button type="button" data-cat="{esc(c)}" aria-pressed="false">{esc(L["cats"][c])} <span class="en">{len(recs_by(c))}</span></button>' for c in CATS)
    years = ''.join(f'<option value="{y}">{L["year_fmt"].format(y)}</option>' for y in ['2025', '2024', '2023', '2022', '2021'])
    vals = [len(RECORDS), n_orgs(), len(recs_by('국가 R&D')), len(recs_by('수소도시'))]
    facts = ''.join(f'<div><dt>{a}</dt><dd>{v}' + (f'<small>{u}</small>' if u else '') + '</dd></div>' for (a, u), v in zip(L['rf'], vals))
    th = ''.join(f'<th scope="col">{h}</th>' for h in L['th'])
    body = sub_top(L, lang, 3, L['nav'][3][3][0][0], 'records', 19) + f'''
<div class="page wrap">
  <div class="page-head"><h2>{L['records_h2']}</h2><p>{L['records_p']}</p></div>
  <dl class="facts">{facts}</dl>
  <div class="filters">
    <div class="chips" role="group" aria-label="{L['cat_aria']}">{chips}</div>
    <div class="search">
      <label class="sr-only" for="f-year">{L['year_label']}</label>
      <select id="f-year"><option value="all">{L['all_years']}</option>{years}</select>
      <label class="sr-only" for="f-q">{L['search_label']}</label>
      <input id="f-q" type="search" placeholder="{L['search_label']}">
    </div>
  </div>
  <p class="result-count" aria-live="polite">{L['count_fmt'].format(n=len(RECORDS))}</p>
  <table class="rec-table">
    <thead><tr>{th}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="empty" hidden>{L['empty']}</p>
</div>'''
    page(L, lang, 'records', L['records_title'], L['records_desc'], body, 3)


def build_contact(L, lang):
    C = L['company']
    q = quote(T['ko']['company']['addr'])
    maps = (f'<a class="btn" href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">{L["map_naver"]}</a>'
            f'<a class="btn" href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">{L["map_kakao"]}</a>')
    if lang != 'ko':
        maps = f'<a class="btn" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">{L["map_google"]}</a>' + maps
    body = sub_top(L, lang, 4, L['nav'][4][3][0][0], 'contact', 23) + f'''
<div class="page wrap">
  <div class="contact-grid">
    <div>
      <dl class="contact-list">
        <div><dt>{L['c_addr']}</dt><dd>{C['addr']}</dd></div>
        <div><dt>{L['c_tel']}</dt><dd><a href="tel:+82314270937">{C['tel']}</a></dd></div>
        <div><dt>{L['c_hours']}</dt><dd>{L['hours']}</dd></div>
      </dl>
      <div class="map-links">{maps}</div>
    </div>
    <div class="map"><iframe title="{L['map_title']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={q}&amp;hl={lang}&amp;output=embed"></iframe></div>
  </div>
  <section class="inquiry" id="inquiry">
    <div><h4>{L['inq_h']}</h4><p>{L['inq_p']}</p></div>
    <a class="btn fill" href="tel:+82314270937">{L['inq_btn']}</a>
  </section>
</div>'''
    page(L, lang, 'contact', L['contact_title'], L['contact_desc'], body, 4)


def build_404(L, lang):
    body = f'''<section class="sub-visual">{sub_art(29)}<div class="wrap"><p class="en-title">404</p><h1>{L['nf_h1']}</h1><p>{L['nf_p']}</p></div></section>
<div class="page wrap" style="text-align:center"><a class="btn fill" href="{href('index', lang)}">{L['nf_btn']}</a></div>'''
    page(L, lang, '404', L['nf_title'], L['brand'], body)


if __name__ == '__main__':
    missing = [r[2] for r in RECORDS if r[2] not in TITLES] + [r[3] for r in RECORDS if r[3] not in ORGS]
    if missing:
        raise SystemExit('content.py에 번역이 없는 실적 항목: ' + ', '.join(missing))
    for lang in LANGS:
        L = T[lang]
        for f in [build_home, build_about, build_greeting, build_vision, build_partners, build_business,
                  build_history, build_records, build_contact, build_404]:
            f(L, lang)
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    print('done:', len(LANGS) * len(PAGES), 'pages')
