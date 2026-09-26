# -*- coding: utf-8 -*-
"""넥서스도시랩 정적 사이트 빌더 — site/*.html 생성"""
import json, random, html, os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)  # 저장소 최상위 폴더
RECORDS = json.load(open(os.path.join(HERE, 'records.json'), encoding='utf-8'))
esc = html.escape

COMPANY = {
    'name': '주식회사 넥서스도시랩', 'en': 'NEXUS CITY LAB Co., Ltd.', 'ceo': '노경식',
    'addr': '경기도 안양시 동안구 엘에스로116번길 91, 1019호', 'tel': '031-427-0937',
}

CATS = ['수소도시', '탄소중립', '도시·지역개발', '국가 R&D', '국제협력']

NAV = [
    ('회사소개', 'About', '미래형 탄소중립 도시와 수소경제를 연구하는 연구개발 컨설팅 기업입니다.', [
        ('개요', 'about.html'), ('인사말', 'greeting.html'), ('비전·강점', 'vision.html'), ('협력기관', 'partners.html')]),
    ('사업소개', 'Business', '정책 수립부터 타당성조사, 사업 실행 지원까지 하나의 흐름으로 수행합니다.', [
        ('사업영역', 'business.html'), ('수소도시·탄소중립도시', 'business.html#area-1'),
        ('에너지전환·온실가스 감축', 'business.html#area-2'), ('도시·지역개발 기획', 'business.html#area-3'),
        ('국가·지방정부 R&D', 'business.html#area-4'), ('국제개발협력(ODA)', 'business.html#area-5'),
        ('수행 프로세스', 'business.html#process')]),
    ('연혁', 'History', '2018년 설립 이후의 주요 발자취입니다.', [
        ('연혁', 'history.html')]),
    ('실적', 'Projects', '2021년 이후 수행한 용역과 국가 R&D 실적입니다.', [
        ('수행실적', 'records.html')] + [(c, 'records.html?cat=' + quote(c)) for c in CATS]),
    ('문의', 'Contact', '과업 문의와 찾아오시는 길을 안내합니다.', [
        ('오시는 길', 'contact.html'), ('과업 문의', 'contact.html#inquiry')]),
]

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
    'flag': '<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 56V8"/><path d="M14 10h34l-7 10 7 10H14"/></svg>',
}
ARROW = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
HOME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 11l9-7 9 7M5 9.5V20h5v-6h4v6h5V9.5"/></svg>'

AREAS = [
    dict(id='area-1', icon='h2', en='Hydrogen & Carbon-Neutral City', title='수소도시·탄소중립도시 연구', cat='수소도시',
         short='수소 시범도시 마스터플랜부터 탄소중립 선도도시 사업화 모델까지',
         desc='수소 생산·저장·활용의 전 주기를 도시 공간에 통합하는 수소도시와, 온실가스 감축을 수치로 입증하는 탄소중립도시의 계획을 수립합니다.',
         tasks=['수소 시범도시 마스터플랜 및 수소도시 조성사업 기획·종합계획', '탄소중립 선도도시 기본계획 및 사업화 모델 개발',
                '수소특화단지·수소생산기지 타당성조사 및 지방재정 투자심사 대응', '수소도시 운영제도·지원 네트워크 및 통합 안전관리 방안'],
         basis=['수소경제 육성 및 수소 안전관리에 관한 법률', '탄소중립·녹색성장 기본법', '수소도시종합계획']),
    dict(id='area-2', icon='leaf', en='Energy Transition & GHG Reduction', title='에너지전환·온실가스 감축 정책 연구', cat='탄소중립',
         short='RE100 커뮤니티, 온실가스 저감 시뮬레이션, 신재생에너지 사업추진',
         desc='중앙정부와 지자체의 탄소중립 목표를 실행 가능한 정책과 사업으로 옮기기 위한 추진방안과 타당성을 연구합니다.',
         tasks=['탄소중립도시 추진방안 및 그린도시 공모사업 기획', 'RE100 커뮤니티 조성 타당성 검토',
                '온실가스 저감 국제표준 및 시뮬레이션 도구', '신재생에너지 사업추진방안 및 탄소저감 타당성'],
         basis=['기후위기 대응을 위한 탄소중립·녹색성장 기본법', '에너지법']),
    dict(id='area-3', icon='city', en='Urban & Regional Development', title='도시 및 지역개발 기획', cat='도시·지역개발',
         short='도시개발 타당성조사, 역세권 개발구상, 농촌공간계획',
         desc='상위계획과 정합성을 갖춘 도시·지역개발 구상과 타당성조사로 사업의 추진 근거를 만듭니다.',
         tasks=['도시개발사업 타당성조사 및 역세권 종합개발구상', '자유무역지역 지정 타당성 사전조사',
                '스마트그린 산업단지 기본계획', '농촌특화지구 지침 및 농촌공간계획·메가시티 상생발전 전략'],
         basis=['국토의 계획 및 이용에 관한 법률', '도시개발법', '농촌공간 재구조화 및 재생지원에 관한 법률']),
    dict(id='area-4', icon='rnd', en='National & Local R&D', title='국가·지방정부 R&D 과제 수행', cat='국가 R&D',
         short='플랜트 안전도시, 수소전기트램, 탄소중립도시 시범모델 기획',
         desc='기업부설연구소를 기반으로 국토교통·산업 분야 국가 R&D 과제에 참여하여 제도와 모델을 개발합니다.',
         tasks=['국토공간 기반 플랜트 안전도시 제도 및 모델 개발(3개년)', '수소전기트램용 시스템 통합 및 검증 기술개발(3개년)',
                '2050 탄소중립도시 시범모델 구축사업 기획', '미활용 자원·에너지 지능형 순환 시스템 기술개발 기획'],
         basis=['국토교통과학기술진흥원', '한국산업기술진흥원', '한국산업기술평가원']),
    dict(id='area-5', icon='globe', en='International Development Cooperation', title='국제개발협력(ODA)·해외진출 지원', cat='국제협력',
         short='ODA 협력국 기후변화 정책조사, 해외 인프라 타당성조사(F/S)',
         desc='개발도상국의 기후변화 대응과 인프라 사업에 대한 정책조사와 타당성조사로 국내 기관의 해외 진출을 지원합니다.',
         tasks=['ODA 중점협력국 기후변화 대응 물관리 정책 동향 조사', '해외 국제공항 현대화사업 타당성조사(F/S)',
                '한국형 스마트시티·녹색도시 해외진출 전략'],
         basis=['한국수출입은행(EDCF)', 'KOICA', 'World Bank']),
]

PARTNERS = [('국토교통과학기술진흥원', 'partner1.png', True), ('한국건설기술연구원', 'partner2.png', False),
            ('한국에너지기술연구원', 'partner3.png', False), ('한국청정수소진흥연구원', 'partner4.png', False),
            ('한전KDN', 'partner5.png', False), ('한국지역난방공사', 'partner6.png', False),
            ('LH 토지주택연구원', 'partner7.png', True), ('글로벌에너지', 'partner8.png', True)]

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
    """logo-like continuous N loop: up, arc over, down, arc under, up, arc over, down"""
    d = f'M-40 {base}H{x}'
    d += f'V{top}a{r} {r} 0 0 1 {2*r} 0V{base-60}a{r} {r} 0 0 0 {2*r} 0V{top}a{r} {r} 0 0 1 {2*r} 0V{base}'
    return d, x + 6 * r

def hero_art():
    base = 700
    parts = [f'<svg class="art" viewBox="0 0 1440 800" preserveAspectRatio="xMaxYMax slice" aria-hidden="true">', GRAD,
             '<rect width="1440" height="800" fill="url(#glow)"/>',
             skyline(7, 1480, base, 40, 250, x0=700, op=.13) + skyline(3, 700, base, 20, 90, x0=-20, windows=False, op=.08)]
    parts += [turbine(1360, base - 190, .9), turbine(1420, base - 230, 1.1), turbine(760, base - 120, .7)]
    parts += [tank(560, base, 34), tank(640, base, 26)]
    d, end = n_pipe(980, base - 40, base - 250, 56)
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

# ───────── layout ─────────
def header(current):
    lis = []
    for i, (k, en, intro, items) in enumerate(NAV):
        cur = ' class="is-current"' if i == current else ''
        lis.append(f'<li{cur}><a href="{items[0][1]}">{k}</a></li>')
    cols = ''.join(f'<div><h3>{k}</h3>' + ''.join(f'<a href="{u}">{esc(t)}</a>' for t, u in items) + '</div>' for k, en, intro, items in NAV)
    drawer = ''.join(f'<details{" open" if i == current else ""}><summary>{k}</summary><ul>' +
                     ''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in items) + '</ul></details>'
                     for i, (k, en, intro, items) in enumerate(NAV))
    return f'''<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="넥서스도시랩 홈">
      <img class="mark mark-light" src="assets/img/mark-light.svg" alt="" width="38" height="38">
      <img class="mark mark-dark" src="assets/img/mark-dark.svg" alt="" width="38" height="38">
      <img class="word word-light" src="assets/img/wordmark-light.svg" alt="넥서스도시랩 NEXUS CITY LAB" width="176" height="30">
      <img class="word word-dark" src="assets/img/wordmark-dark.svg" alt="넥서스도시랩 NEXUS CITY LAB" width="176" height="30">
    </a>
    <nav class="gnb" aria-label="주 메뉴"><ul>{''.join(lis)}</ul></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" aria-label="메뉴 열기"><span></span></button>
  </div>
  <div class="mega"><div class="wrap">
    <div class="mega-intro"><strong>도시와 에너지가 만나는 곳의 연구개발 컨설팅</strong><p>수소도시·탄소중립도시 계획부터 국가 R&amp;D와 국제개발협력까지 수행합니다.</p></div>
    <div class="mega-cols">{cols}</div>
  </div></div>
</header>
<nav class="drawer" id="drawer" aria-label="모바일 메뉴">{drawer}</nav>'''

def footer():
    links = ''.join(f'<a href="{u}">{k}</a>' for k, u in [('회사소개', 'about.html'), ('사업소개', 'business.html'), ('연혁', 'history.html'),
                                                          ('수행실적', 'records.html'), ('협력기관', 'partners.html'), ('오시는 길', 'contact.html')])
    return f'''<footer class="site-footer">
  <div class="top"><div class="wrap">{links}</div></div>
  <div class="main"><div class="wrap">
    <img class="logo" src="assets/img/wordmark-dark.svg" alt="넥서스도시랩 NEXUS CITY LAB" width="200" height="34">
    <div>
      <address>
        <span><b>법인명</b>{COMPANY['name']}</span><span><b>대표</b>{COMPANY['ceo']}</span><br>
        <span><b>주소</b>{COMPANY['addr']}</span><span><b>TEL</b><a href="tel:{COMPANY['tel'].replace('-', '')}">{COMPANY['tel']}</a></span>
      </address>
      <p class="copy">© 2026 NEXUS CITY LAB Co., Ltd. All rights reserved.</p>
    </div>
  </div></div>
</footer>
<button class="to-top" type="button" aria-label="맨 위로"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>
<script src="assets/js/main.js"></script>'''

def page(fname, title, desc, body, current=None, home=False):
    full_title = f'{title} | 넥서스도시랩' if title else '넥서스도시랩 | 수소도시·탄소중립도시 연구개발 컨설팅'
    doc = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="넥서스도시랩">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#0E1C1F">
<link rel="icon" type="image/svg+xml" href="assets/img/mark-light.svg">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body{' class="is-home"' if home else ''}>
{header(current if current is not None else -1)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(doc)

def sub_top(ci, sub_label, sub_url, lead, seed):
    k, en, intro, items = NAV[ci]
    d1 = ''.join(f'<li><a href="{it[3][0][1]}"{" aria-current=\"page\"" if i == ci else ""}>{it[0]}</a></li>' for i, it in enumerate(NAV))
    sibs = [it for it in items if '#' not in it[1] and '?' not in it[1]]
    d2 = ''.join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == sub_url else ""}>{esc(t)}</a></li>' for t, u in sibs)
    return f'''<section class="sub-visual">
  {sub_art(seed)}
  <div class="wrap">
    <p class="en-title">{en}</p>
    <h1>{k}</h1>
    <p>{lead}</p>
  </div>
</section>
<nav class="location" aria-label="현재 위치"><div class="wrap">
  <a class="loc-home" href="index.html" aria-label="홈">{HOME}</a>
  <div class="loc-drop"><button type="button" aria-expanded="false">{k}</button><ul>{d1}</ul></div>
  <div class="loc-drop"><button type="button" aria-expanded="false">{esc(sub_label)}</button><ul>{d2}</ul></div>
</div></nav>'''

def recs_by(cat):
    return [r for r in RECORDS if r[1] == cat]

# ───────── pages ─────────
def build_home():
    recent = [r for r in RECORDS if r[0] == '2025']
    area_links = ''.join(f'''<li><a href="business.html#{a['id']}">{ICONS[a['icon']]}<h3>{a['title']}</h3><p>{a['short']}</p>{ARROW}</a></li>''' for a in AREAS)
    partners = ''.join(f'<li class="{"tall" if t else ""}"><img src="assets/img/partners/{f}" alt="{n}" loading="lazy"></li>' for n, f, t in PARTNERS)
    recent_li = ''.join(f'<li><span class="tag">{esc(r[1])}</span><span class="t">{esc(r[2])}</span><span class="o">{esc(r[3])}</span></li>' for r in recent)
    body = f'''<section class="hero">
  {hero_art()}
  <div class="wrap">
    <p class="kicker">Nexus City Lab · Hydrogen &amp; Carbon-Neutral City</p>
    <h1><span>정책이 실행 가능한 계획이 되고,</span><span>계획이 도시의 변화가 되도록.</span></h1>
    <p>넥서스도시랩은 수소도시와 탄소중립도시, 그리고 이를 실현하는 도시계획과 정책연구를 전문으로 하는 연구개발 컨설팅 기업입니다.</p>
    <div class="actions"><a class="btn fill" href="business.html">사업소개 보기</a><a class="btn ghost-light" href="records.html">수행실적 보기</a></div>
  </div>
  <span class="scroll">Scroll</span>
</section>

<section class="home-sec">
  <div class="wrap">
    <div class="about-intro">
      <div>
        <p class="en" style="color:var(--teal)">About</p>
        <p class="lead">2018년 설립 이후 중앙정부와 지방자치단체, 공기업과 함께 도시와 에너지가 만나는 현장에서 연구와 계획을 수행해 왔습니다.</p>
      </div>
      <div class="txt">
        <p>수소 시범도시 마스터플랜, 탄소중립 선도도시 기본계획, 국가 R&amp;D 과제까지. 법령·지침·통계에 근거한 분석으로 발주기관이 바로 활용할 수 있는 계획과 문서를 만듭니다.</p>
        <p>기업부설연구소와 연구개발서비스업 등록을 바탕으로, 정책 수립 단계부터 타당성조사와 투자심사 대응, 실시설계 발주 지원까지 하나의 흐름으로 지원합니다.</p>
        <a class="btn" href="about.html">회사 개요</a>
      </div>
    </div>
    <dl class="fact-row">
      <div><dt>설립</dt><dd>2018년 11월</dd></div>
      <div><dt>기업부설연구소</dt><dd>2020년 인정</dd></div>
      <div><dt>수행 실적 (2021–2025)</dt><dd>41건</dd></div>
      <div><dt>국가 R&amp;D 과제</dt><dd>7건</dd></div>
    </dl>
  </div>
</section>

<section class="home-sec alt">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Business</p><h2>사업영역</h2></div><a href="business.html">사업소개 전체</a></div>
    <ul class="area-list">{area_links}</ul>
  </div>
</section>

<section class="home-sec">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Recent Projects</p><h2>2025년 수행 과업</h2></div><a href="records.html">실적 전체 41건</a></div>
    <ul class="recent">{recent_li}</ul>
  </div>
</section>

<section class="home-sec alt">
  <div class="wrap">
    <div class="sec-head"><div><p class="en">Partners</p><h2>함께하는 기관</h2></div><a href="partners.html">협력기관</a></div>
    <ul class="partners">{partners}</ul>
  </div>
</section>

<section class="cta-band">
  {sub_art(21)}
  <div class="wrap">
    <div><h2>과업을 준비하고 계신가요?</h2><p>제안요청서(RFP)나 과업지시서를 보내주시면 수행 가능 여부와 일정을 회신드립니다.</p></div>
    <div class="actions"><a class="btn fill" href="tel:0314270937">031-427-0937</a><a class="btn ghost-light" href="contact.html">오시는 길</a></div>
  </div>
</section>'''
    page('index.html', None, '넥서스도시랩은 수소도시·탄소중립도시, 에너지전환 정책, 도시·지역개발, 국가 R&D, 국제개발협력을 수행하는 연구개발 컨설팅 기업입니다.', body, home=True)

def build_about():
    certs = f'''<div class="cert">{ICONS['badge']}<div><h4>기업부설연구소 인정</h4><p>한국산업기술진흥협회 · 2020년 11월</p></div></div>
<div class="cert">{ICONS['doc']}<div><h4>연구개발서비스업 등록<br>(연구개발컨설팅전문업)</h4><p>과학기술정보통신부 · 2020년 12월</p></div></div>'''
    areas = ''.join(f'<li>{a["title"]}</li>' for a in AREAS)
    body = sub_top(0, '개요', 'about.html', NAV[0][2], 3) + f'''
<div class="page wrap">
  <div class="page-head"><h2>도시와 에너지를 잇는<br>연구개발 컨설팅 기업</h2>
  <p>주식회사 넥서스도시랩은 수소도시·탄소중립도시 연구와 에너지 관련 컨설팅을 수행하는 전문·과학·기술서비스 기업입니다.</p></div>

  <section class="block">
    <div class="block-title"><h3>일반 현황</h3><span class="en">General</span></div>
    <table class="info-table"><tbody>
      <tr><th scope="row">법인명</th><td>{COMPANY['name']}<small>{COMPANY['en']}</small></td></tr>
      <tr><th scope="row">설립</th><td>2018년 11월 26일<small>2025년 2월 현 상호로 변경 (구 코비즈 주식회사)</small></td></tr>
      <tr><th scope="row">대표자</th><td>{COMPANY['ceo']}</td></tr>
      <tr><th scope="row">업종</th><td>전문, 과학 및 기술서비스업<small>학술연구, 연구개발컨설팅</small></td></tr>
      <tr><th scope="row">기업 구분</th><td>소기업</td></tr>
      <tr><th scope="row">주요 고객</th><td>중앙정부(국토교통부·산업통상자원부), 지방자치단체, LH·지방공사, 공공기관</td></tr>
      <tr><th scope="row">본사</th><td>{COMPANY['addr']}</td></tr>
      <tr><th scope="row">전화</th><td><a href="tel:0314270937">{COMPANY['tel']}</a></td></tr>
    </tbody></table>
  </section>

  <section class="block">
    <div class="block-title"><h3>인증·등록</h3><span class="en">Certification</span></div>
    <div class="cert-list">{certs}</div>
  </section>

  <section class="block">
    <div class="block-title"><h3>사업영역</h3><span class="en">Business Areas</span></div>
    <ul class="area-list">{''.join(f'<li><a href="business.html#{a["id"]}">{ICONS[a["icon"]]}<h3>{a["title"]}</h3><p>{a["short"]}</p>{ARROW}</a></li>' for a in AREAS)}</ul>
  </section>
</div>'''
    page('about.html', '회사 개요', '주식회사 넥서스도시랩 일반 현황, 인증·등록, 사업영역', body, 0)

def build_greeting():
    body = sub_top(0, '인사말', 'greeting.html', NAV[0][2], 5) + '''
<div class="page wrap">
  <div class="greeting">
    <p class="lead"><span>정책이 실행 가능한 계획이 되고,</span><span>계획이 도시의 변화가 되도록.</span></p>
    <div class="body">
      <p>주식회사 넥서스도시랩은 수소도시와 탄소중립도시, 그리고 이를 실현하는 도시계획과 정책연구를 전문으로 하는 연구개발 컨설팅 기업입니다. 2018년 설립 이후 국토교통부·산업통상자원부 등 중앙정부, 지방자치단체, LH와 지방공사, 공공연구기관과 함께 수소 시범도시 마스터플랜, 탄소중립 선도도시 기본계획, 국가 R&amp;D 과제 등 도시와 에너지가 만나는 현장에서 연구와 계획을 수행해 왔습니다.</p>
      <p>기후위기 대응과 탄소중립은 이제 선언이 아니라 실행의 단계에 있습니다. 좋은 정책이 실제 도시의 변화로 이어지기 위해서는 상위계획과 정합성을 갖춘 계획, 재원 확보가 가능한 사업구조, 그리고 발주기관이 바로 활용할 수 있는 근거 있는 문서가 필요합니다. 저희는 법령·지침·통계에 기반한 정확한 분석과 20년간 축적한 정책연구 경험으로 그 간극을 메우는 일에 집중하고 있습니다.</p>
      <p>수소 생산·저장·활용의 전 주기를 도시 공간에 통합하는 수소도시, 온실가스 감축을 수치로 입증하는 탄소중립도시, 도시와 농촌이 함께 성장하는 지역개발, 그리고 국제개발협력을 통한 해외 진출까지, 넥서스도시랩은 정책 수립 단계부터 타당성조사와 투자심사 대응, 실시설계 발주 지원에 이르는 전 과정을 하나의 흐름으로 지원합니다.</p>
      <p>앞으로도 발주기관의 정책 목표가 실행 가능한 계획과 사업으로 이어지도록, 신뢰할 수 있는 연구와 성실한 자문으로 함께하겠습니다. 저희 회사에 보내주시는 관심과 기대에 깊이 감사드립니다.</p>
      <div class="sign"><span>주식회사 넥서스도시랩 임직원 일동</span></div>
    </div>
  </div>
</div>'''
    page('greeting.html', '인사말', '넥서스도시랩 인사말', body, 0)

def build_vision():
    goals = [('h2', '미래 수소 기반<br>수소경제 및 수소도시 컨설팅'), ('leaf', '탄소중립도시<br>선도 모델 구축 컨설팅'), ('city', '지속가능한<br>도시·농촌 상생발전 컨설팅')]
    goals_li = ''.join(f'<li>{ICONS[i]}<strong>{t}</strong></li>' for i, t in goals)
    strengths = [('h2', '수소·탄소중립 특화 전문성', '국내외 수소도시 및 탄소중립 연구를 다수 수행했습니다.'),
                 ('badge', '국가 R&D 및 공공사업', '국토교통부, 산업통상자원부, LH, 지자체, 공공기관 과업을 다수 수주했습니다.'),
                 ('link', '통합 솔루션 제공', '도시·에너지·환경을 아우르는 융합형 계획 수립과 컨설팅을 전문으로 합니다.'),
                 ('globe', '국제협력 및 해외시장 경험', 'ODA 및 해외 기후변화 대응, 인프라 타당성조사를 수행했습니다.')]
    st = ''.join(f'<li>{ICONS[i].replace("class=\"ico\"", "class=\"ico\"")}<div><h4>{h}</h4><p>{p}</p></div></li>' for i, h, p in strengths)
    body = sub_top(0, '비전·강점', 'vision.html', NAV[0][2], 9) + f'''
<div class="page wrap">
  <section class="block">
    <div class="block-title"><h3>비전과 목표</h3><span class="en">Vision</span></div>
    <div class="vision-core"><p class="en">Vision</p><p class="big">미래형 탄소중립 도시와 수소경제를 선도하는<br>최고의 연구개발 컨설팅 기업</p></div>
    <ul class="goals">{goals_li}</ul>
  </section>
  <section class="block">
    <div class="block-title"><h3>차별화된 강점</h3><span class="en">Strengths</span></div>
    <ul class="strengths">{st}</ul>
  </section>
</div>'''
    page('vision.html', '비전·강점', '넥서스도시랩 비전과 목표, 차별화된 강점', body, 0)

def build_partners():
    lis = ''.join(f'<li class="{"tall" if t else ""}"><img src="assets/img/partners/{f}" alt="{n}" loading="lazy"><span>{n}</span></li>' for n, f, t in PARTNERS)
    body = sub_top(0, '협력기관', 'partners.html', NAV[0][2], 11) + f'''
<div class="page wrap">
  <div class="page-head"><h2>함께 연구하는 기관</h2><p>공공연구기관과 에너지 공기업, 산업계와 협력하여 연구와 사업을 수행하고 있습니다.</p></div>
  <ul class="partners">{lis}</ul>
</div>'''
    page('partners.html', '협력기관', '넥서스도시랩 협력기관', body, 0)

def build_business():
    tabs = ''.join(f'<a href="#{a["id"]}">{a["title"].split("·")[0] if len(a["title"])>12 else a["title"]}</a>' for a in AREAS)
    tabs = ''.join(f'<a href="#{a["id"]}">{t}</a>' for a, t in zip(AREAS, ['수소·탄소중립도시', '에너지전환', '도시·지역개발', '국가 R&D', '국제개발협력'])) + '<a href="#process">수행 프로세스</a>'
    area_html = ''
    for a in AREAS:
        recs = recs_by(a['cat'])
        tasks = ''.join(f'<li>{esc(t)}</li>' for t in a['tasks'])
        basis = ''.join(f'<li>{esc(b)}</li>' for b in a['basis'])
        label = '관련 법령·계획' if a['id'] in ('area-1', 'area-2', 'area-3') else '주요 발주·협력 기관'
        area_html += f'''<section class="area" id="{a['id']}">
  <div class="area-head">{ICONS[a['icon']]}<p class="en">{a['en']}</p><h3>{a['title']}</h3></div>
  <div class="area-body">
    <p>{a['desc']}</p>
    <h4>주요 수행 업무</h4><ul class="bullets">{tasks}</ul>
    <h4>{label}</h4><ul class="basis">{basis}</ul>
    <a class="more" href="records.html?cat={quote(a['cat'])}">{a['cat']} 분야 실적 {len(recs)}건 보기</a>
  </div>
</section>'''
    steps = [('정책 수립', '상위계획과 법령·지침을 검토하고 발주기관의 정책 목표를 구체적인 추진 전략으로 정리합니다.'),
             ('계획·타당성조사', '마스터플랜과 기본계획을 수립하고 사업의 기술적·경제적 타당성을 분석합니다.'),
             ('투자심사 대응', '지방재정 투자심사와 공모사업 평가에 필요한 근거 자료와 사업계획서를 작성합니다.'),
             ('실행 지원', '실시설계 발주와 운영제도 마련 등 계획이 실제 사업으로 이어지도록 지원합니다.')]
    flow = ''.join(f'<li><span class="step">Step {i+1}</span><h4>{h}</h4><p>{p}</p></li>' for i, (h, p) in enumerate(steps))
    body = sub_top(1, '사업영역', 'business.html', NAV[1][2], 13) + f'''
<div class="page wrap">
  <p class="statement">수소도시·탄소중립도시 연구에서 국가 R&amp;D와 국제개발협력까지, 도시와 에너지가 만나는 다섯 개 영역에서 연구와 컨설팅을 수행합니다.</p>
  <nav class="tabs" aria-label="사업영역">{tabs}</nav>
  {area_html}
  <section class="block" id="process">
    <div class="block-title"><h3>수행 프로세스</h3><span class="en">Process</span></div>
    <ol class="flow">{flow}</ol>
  </section>
</div>'''
    page('business.html', '사업소개', '수소도시·탄소중립도시, 에너지전환, 도시·지역개발, 국가 R&D, 국제개발협력 사업영역', body, 1)

def build_history():
    def proj(y):
        return [r[2] for r in RECORDS if r[0] == y]
    # curated highlight lines per year (from company profile)
    H = {
        '2025': [('02', '주식회사 넥서스도시랩으로 상호 변경', '구 코비즈 주식회사', None),
                 ('', '주요 수행 과업', None, ['울진·울산(3기) 수소도시 조성사업 마스터플랜 수립', '탄소중립 선도도시(당진·제주·노원·보령) 사업화 모델 개발', '태안군 수소도시 조성사업 계획서 작성', '모잠비크 베이라·펨바 국제공항 현대화사업 타당성조사(F/S)'])],
        '2024': [('', '주요 수행 과업', None, ['울진 수소도시 조성사업 기획연구, 양주 수소도시 마스터플랜 수립', '평택 예비 수소특화단지 기획, 수소생산기지 지방재정 타당성 조사 지원', '농촌특화지구 지침 연구, 농촌공간계획·메가시티 상생발전 전략 연구'])],
        '2023': [('03', '노경식 대표이사 취임', None, None),
                 ('', '주요 수행 과업', None, ['평택 수소도시 종합계획 수립', '새만금 스마트 수변도시 RE100 커뮤니티 조성 타당성 검토', '송산그린시티 스마트그린 산업단지 및 탄소중립도시 기본계획', '동해항 자유무역지역 타당성, 원주 문막지구 도시개발 타당성조사'])],
        '2022': [('', '주요 수행 과업', None, ['국토교통부 탄소중립도시 추진방안 연구', '수소 시범도시 운영제도 및 지원 네트워크 구축 방안 연구', '광명시 탄소중립 그린도시 공모사업', '2050 탄소중립도시 시범모델 구축사업 기획(국가 R&D)'])],
        '2021': [('', '주요 수행 과업', None, ['울산광역시 수소 시범도시 마스터플랜', 'LH 수소인프라 활성화를 위한 수소도시 조성 기본 연구', '플랜트 안전도시·수소전기트램 국가 R&D 착수'])],
        '2020': [('12', '연구개발서비스업(연구개발컨설팅전문업) 등록', '과학기술정보통신부', None),
                 ('11', '기업부설연구소 인정', '한국산업기술진흥협회', None)],
        '2018': [('11', '코비즈 주식회사 설립', '경기도 안양시', None)],
    }
    def year_block(y):
        lis = ''
        for m, t, s, sub in H[y]:
            sm = f'<small>{s}</small>' if s else ''
            ul = '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in sub) + '</ul>' if sub else ''
            lis += f'<li><span class="m">{m}</span><div class="ev">{t}{sm}{ul}</div></li>'
        return f'<div class="year"><p class="year-num">{y}</p><ol>{lis}</ol></div>'
    eras = [('era-2', '2023 — 2025', '넥서스도시랩으로 새 이름을 걸고, 수소도시·탄소중립도시 계획을 전국 지자체로 넓혔습니다.', ['2025', '2024', '2023']),
            ('era-1', '2018 — 2022', '기업부설연구소를 세우고, 울산 수소 시범도시와 국가 R&D로 수소도시 연구의 기반을 다졌습니다.', ['2022', '2021', '2020', '2018'])]
    era_nav = ''.join(f'<a href="#{i}">{r}</a>' for i, r, _, _ in eras)
    era_html = ''.join(f'<section class="era" id="{i}"><div class="era-head"><p class="range">{r}</p><p>{d}</p></div>{"".join(year_block(y) for y in ys)}</section>' for i, r, d, ys in eras)
    body = sub_top(2, '연혁', 'history.html', NAV[2][2], 17) + f'''
<div class="page wrap">
  <nav class="era-nav" aria-label="연대 선택">{era_nav}</nav>
  {era_html}
</div>'''
    page('history.html', '연혁', '넥서스도시랩 연혁 2018–2025', body, 2)

def build_records():
    orgs = set()
    for r in RECORDS:
        for o in r[3].replace('，', ',').split(','):
            orgs.add(o.strip())
    print('distinct orgs', len(orgs))
    rows = ''.join(f'<tr data-cat="{esc(r[1])}" data-year="{r[0]}"><td class="y">{r[0]}</td><td class="c"><span class="tag">{esc(r[1])}</span></td><td class="t">{esc(r[2])}</td><td class="o">{esc(r[3])}</td></tr>' for r in reversed(RECORDS))
    chips = '<button type="button" data-cat="all" aria-pressed="true">전체</button>' + ''.join(f'<button type="button" data-cat="{c}" aria-pressed="false">{c} <span class="en">{len(recs_by(c))}</span></button>' for c in CATS)
    years = ''.join(f'<option value="{y}">{y}년</option>' for y in ['2025', '2024', '2023', '2022', '2021'])
    body = sub_top(3, '수행실적', 'records.html', NAV[3][2], 19) + f'''
<div class="page wrap">
  <div class="page-head"><h2>수행실적</h2><p>2021년 이후 중앙부처·지방자치단체·공기업·공공기관을 대상으로 수행한 용역 및 국가 R&amp;D 실적입니다.</p></div>
  <dl class="facts">
    <div><dt>수행 실적 (2021–2025)</dt><dd>41<small>건</small></dd></div>
    <div><dt>발주기관</dt><dd>{len(orgs)}<small>개</small></dd></div>
    <div><dt>국가 R&amp;D 과제</dt><dd>7<small>건</small></dd></div>
    <div><dt>수소도시 분야</dt><dd>{len(recs_by('수소도시'))}<small>건</small></dd></div>
  </dl>
  <div class="filters">
    <div class="chips" role="group" aria-label="분야">{chips}</div>
    <div class="search">
      <label class="sr-only" for="f-year">연도</label>
      <select id="f-year"><option value="all">전체 연도</option>{years}</select>
      <label class="sr-only" for="f-q">사업명·발주처 검색</label>
      <input id="f-q" type="search" placeholder="사업명·발주처 검색">
    </div>
  </div>
  <p class="result-count" aria-live="polite">총 <b id="f-count">41</b>건</p>
  <table class="rec-table">
    <thead><tr><th scope="col">연도</th><th scope="col">분야</th><th scope="col">사업명</th><th scope="col">발주처</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="empty" hidden>조건에 맞는 실적이 없습니다. 분야나 검색어를 바꿔 보세요.</p>
</div>'''
    page('records.html', '수행실적', '넥서스도시랩 2021–2025 수행실적 41건: 수소도시, 탄소중립, 도시·지역개발, 국가 R&D, 국제협력', body, 3)

def build_contact():
    q = quote(COMPANY['addr'])
    body = sub_top(4, '오시는 길', 'contact.html', NAV[4][2], 23) + f'''
<div class="page wrap">
  <div class="contact-grid">
    <div>
      <dl class="contact-list">
        <div><dt>주소</dt><dd>{COMPANY['addr']}</dd></div>
        <div><dt>전화</dt><dd><a href="tel:0314270937">{COMPANY['tel']}</a></dd></div>
        <div><dt>업무시간</dt><dd>평일 09:00–18:00</dd></div>
      </dl>
      <div class="map-links">
        <a class="btn" href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">네이버 지도</a>
        <a class="btn" href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">카카오맵</a>
      </div>
    </div>
    <div class="map"><iframe title="넥서스도시랩 위치 지도" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={q}&amp;output=embed"></iframe></div>
  </div>
  <section class="inquiry" id="inquiry">
    <div><h4>과업 문의</h4><p>제안요청서(RFP)나 과업지시서를 보내주시면 수행 가능 여부와 일정을 회신드립니다.</p></div>
    <a class="btn fill" href="tel:0314270937">전화 문의 031-427-0937</a>
  </section>
</div>'''
    page('contact.html', '오시는 길', '넥서스도시랩 오시는 길과 과업 문의', body, 4)

def build_404():
    body = f'''<section class="sub-visual">{sub_art(29)}<div class="wrap"><p class="en-title">404</p><h1>페이지를 찾을 수 없습니다</h1><p>주소가 바뀌었거나 삭제된 페이지입니다. 홈에서 다시 찾아보세요.</p></div></section>
<div class="page wrap" style="text-align:center"><a class="btn fill" href="index.html">홈으로 가기</a></div>'''
    page('404.html', '페이지를 찾을 수 없음', '넥서스도시랩', body)

for f in [build_home, build_about, build_greeting, build_vision, build_partners, build_business, build_history, build_records, build_contact, build_404]:
    f()
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('done')
