"""Buduje 5 podstron dema. python _src/build.py"""
import os, re, json, math, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
URL = 'https://impulseo-pl.github.io/serwis-hulajnog-kutno/'
TEL, TEL_H, MAIL = '+48889503420', '889 503 420', 'Revoltec@vp.pl'
HOME = (52.2236904, 19.3550328)
GMAPS = 'https://www.google.com/maps/place/Naprawa+serwis+hulajnogi/@52.2236904,19.3550328,17z'

SVG = open(os.path.join(SRC, 'hulajnoga.svg.html'), encoding='utf-8').read()
FORM = open(os.path.join(SRC, 'formularz.html'), encoding='utf-8').read()
MIEJSCA = json.load(open(os.path.join(ROOT, 'assets', 'miejscowosci.json'), encoding='utf-8'))

def km(lat, lon):
    r = math.radians
    h = math.sin(r(lat - HOME[0]) / 2) ** 2 + math.cos(r(HOME[0])) * math.cos(r(lat)) * math.sin(r(lon - HOME[1]) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))
for m in MIEJSCA: m['d'] = km(m['lat'], m['lon'])
KM = {m['n']: round(m['d']) for m in MIEJSCA}

NAV = [('', 'Strona główna'), ('naprawy/', 'Naprawy'), ('zgloszenie/', 'Zgłoś naprawę'), ('odbior/', 'Odbiór z domu'), ('kontakt/', 'Kontakt')]

LOGO = '<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="6" fill="#1c3fd1"/><path d="M10 28h16l4-16h4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="11" cy="28" r="3.6" fill="#1c3fd1" stroke="#fff" stroke-width="2.4"/><circle cx="28" cy="28" r="3.6" fill="#ff6a2b" stroke="#fff" stroke-width="2.4"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'

BIZ = {
    "@type": "AutoRepair", "@id": URL + "#serwis",
    "name": "Serwis hulajnóg elektrycznych Kutno",
    "description": "Naprawa i serwis hulajnóg elektrycznych, rowerów elektrycznych, skuterów i wózków inwalidzkich elektrycznych w Kutnie. Wymiana dętek i opon, hamulce, naprawa sterowników i wyświetlaczy, regeneracja baterii, modernizacje. Odbiór sprzętu z Kutna i okolic do 30 km.",
    "url": URL, "telephone": TEL, "email": MAIL, "image": URL + "img/skuter-1200.webp",
    "address": {"@type": "PostalAddress", "streetAddress": "ul. Księdza Piotra Ściegiennego 25", "postalCode": "99-300", "addressLocality": "Kutno", "addressRegion": "łódzkie", "addressCountry": "PL"},
    "geo": {"@type": "GeoCoordinates", "latitude": HOME[0], "longitude": HOME[1]},
    "areaServed": [{"@type": "City", "name": n} for n in ("Kutno", "Krośniewice", "Żychlin", "Łęczyca", "Gostynin", "Dąbrowice", "Piątek", "Strzelce", "Oporów", "Bedlno")],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "15:00"}],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.4", "reviewCount": "10", "bestRating": "5"},
    "sameAs": [GMAPS],
}

def page(path, title, desc, body, extra_ld=None, scripts=''):
    B = '../' * path.count('/')
    nav = ''.join('<a href="%s%s"%s>%s</a>' % (B, p, ' aria-current="page"' if p == path else '', t) for p, t in NAV[1:])
    mnav = ''.join('<a href="%s%s"%s>%s</a>' % (B, p, ' aria-current="page"' if p == path else '', t) for p, t in NAV)
    crumbs = []
    if path:
        name = dict(NAV)[path]
        crumbs = [{"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Serwis hulajnóg Kutno", "item": URL},
            {"@type": "ListItem", "position": 2, "name": name, "item": URL + path}]}]
    graph = [BIZ] + crumbs + (extra_ld or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    foot_nav = ''.join('<li><a href="%s%s">%s</a></li>' % (B, p, t) for p, t in NAV)
    out = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="Serwis hulajnóg elektrycznych Kutno">
<meta property="og:title" content="{H.escape(title)}"><meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{URL}{path}"><meta property="og:image" content="{URL}img/skuter-1200.webp">
<meta name="theme-color" content="#1c3fd1">
<link rel="icon" href="{B}favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{'<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">' if 'mapa' in body else ''}
<link rel="stylesheet" href="{B}assets/styles.css">
<script type="application/ld+json">{ld}</script>
</head>
<body data-base="{B}">
<a class="skip" href="#tresc">Przejdź do&nbsp;treści</a>
<header class="top"><div class="wrap top-in">
  <a class="brand" href="{B or './'}" aria-label="Serwis hulajnóg Kutno – strona główna">{LOGO}<span class="brand-t"><b>Serwis hulajnóg</b><span>elektrycznych · Kutno</span></span></a>
  <nav class="nav" aria-label="Menu główne">{nav}</nav>
  <a class="top-tel" href="tel:{TEL}">{PHONE_SVG}{TEL_H}</a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><i></i><i></i></button>
</div>
<nav class="menu" id="menu" aria-label="Menu">{mnav}<a class="menu-tel" href="tel:{TEL}">{TEL_H}</a></nav>
</header>
<main id="tresc">
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div><p class="foot-b">Serwis hulajnóg elektrycznych Kutno</p><p>ul. Księdza Piotra Ściegiennego 25<br>99-300 Kutno, woj. łódzkie</p><p><a href="tel:{TEL}">{TEL_H}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
  <div><p class="foot-b">Godziny</p><p>pon–pt 9:00–18:00<br>sobota 10:00–15:00<br>niedziela nieczynne</p></div>
  <div><p class="foot-b">Strony</p><ul>{foot_nav}</ul></div>
  <div><p class="foot-b">Naprawiamy</p><p>hulajnogi, rowery, skutery i&nbsp;wózki inwalidzkie elektryczne. Kutno, Krośniewice, Żychlin, Łęczyca, Gostynin i&nbsp;okolice do&nbsp;30&nbsp;km.</p></div>
</div><div class="wrap foot-s"><p>© 2026 Serwis hulajnóg elektrycznych Kutno</p><p><a href="#">Polityka prywatności</a></p></div></footer>
<div class="mbar"><a href="tel:{TEL}">Zadzwoń</a><a href="sms:{TEL}">SMS</a><a href="{B}zgloszenie/" class="m-sig">Zgłoś naprawę</a></div>
{scripts}<script src="{B}assets/app.js" defer></script>
<script src="{B}assets/licznik.js" defer></script>
</body>
</html>
'''
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)

def band(kicker, h1, lead):
    return f'''<section class="band"><div class="wrap band-in">
  <p class="kicker">{kicker}</p>
  <h1>{h1}</h1>
  <p class="band-lead">{lead}</p>
</div></section>'''

def mini(parts, n):
    s = SVG.replace('class="scooter"', 'class="scooter mini" aria-hidden="true" focusable="false"').replace('role="group" aria-label="Rysunek hulajnogi – wybierz część"', '')
    s = re.sub(r'<g class="callouts">.*?</g>\s*</svg>', '</svg>', s, flags=re.S)
    s = s.replace('id="hatch"', 'id="hatch%d"' % n).replace('url(#hatch)', 'url(#hatch%d)' % n)
    s = s.replace(' tabindex="-1"', '')
    for p in parts:
        s = s.replace('class="part" data-part="%s"' % p, 'class="part on" data-part="%s"' % p)
    if parts == ['*']:
        s = s.replace('class="part"', 'class="part on"')
    return s

def calc_style_css(): pass

# ------------------------------------------------------------------ STRONA GŁÓWNA
REVS = [
    ('Bardzo dobry serwis hulajnóg elektrycznych. Naprawa wykonana szybko i&nbsp;profesjonalnie, a&nbsp;obsługa bardzo miła i&nbsp;pomocna. Hulajnoga działa teraz bez zarzutu. Zdecydowanie polecam!', 'Maciej W.'),
    ('Super serwis, naprawa zrobiona idealnie, mycie – wygląda jak nowa. Daję opinię 5/5, super obsługa i&nbsp;przede wszystkim miła.', 'Julek O.'),
    ('Super serwis, mega miła i&nbsp;profesjonalna obsługa z&nbsp;szybką realizacją.', 'Klaudia B.'),
    ('Wszystko git, tanio, bardzo dobra jakość. Hulajnoga jest teraz jak nowa, bardzo szybko naprawili. Wszystkim polecam!', 'Sasza'),
]
revs = ''.join(f'<blockquote><p>{t}</p><footer>{a} · opinia w&nbsp;Google, 5/5</footer></blockquote>' for t, a in REVS)

ZAKRES = [
    ('jezdny', 'Opony, dętki i&nbsp;mechanika', 'wymiana dętek i&nbsp;opon, kasowanie luzów na&nbsp;kierownicy, naprawa zawieszenia'),
    ('hamulce', 'Hamulce', 'regulacja i&nbsp;naprawa hamulców, wymiana klocków i&nbsp;tarcz'),
    ('elektronika', 'Elektronika', 'naprawa sterowników, płyt i&nbsp;wyświetlaczy, usterki elektryczne'),
    ('baterie', 'Baterie', 'diagnostyka, renowacja i&nbsp;regeneracja baterii, kalibracja ogniw'),
    ('tuning', 'Modernizacje', 'poprawa osiągów, zmiana blokad prędkości'),
    ('przeglad', 'Przegląd', 'przegląd przed sezonem, czyszczenie i&nbsp;smarowanie'),
    ('rowery', 'Rowery elektryczne', 'wspomaganie, sterownik, bateria, ładowarka'),
    ('wozki', 'Wózki inwalidzkie elektryczne', 'elektryka, akumulatory, sterowanie, mechanika'),
    ('skutery', 'Skutery elektryczne', 'także skutery inwalidzkie dla seniorów'),
]
zak = ''.join(f'<li><a href="naprawy/#{k}"><b>{t}</b><span>{d}</span></a></li>' for k, t, d in ZAKRES)
blisko = ['Krośniewice', 'Piątek', 'Żychlin', 'Łęczyca', 'Dąbrowice', 'Gostynin']
blisko.sort(key=lambda n: KM[n])
bl = ''.join(f'<tr><th>{n}</th><td>ok. {KM[n]}&nbsp;km</td></tr>' for n in blisko)

home = f'''<section class="hero"><div class="wrap hero-in">
  <div class="hero-txt">
    <p class="kicker light">Kutno, ul.&nbsp;Ściegiennego 25 · <span data-status>pon–pt 9–18, sob 10–15</span></p>
    <h1>Serwis hulajnóg elektrycznych w&nbsp;Kutnie</h1>
    <p class="lead">Hulajnoga przestała działać, coś stuka, hamulec nie trzyma albo bateria szybko pada? Naprawiamy hulajnogi elektryczne na&nbsp;miejscu w&nbsp;Kutnie, a&nbsp;z&nbsp;okolic do&nbsp;30&nbsp;km możemy odebrać sprzęt spod domu.</p>
    <div class="actions">
      <a class="btn hot" href="tel:{TEL}">Zadzwoń: {TEL_H}</a>
      <a class="btn ghost" href="zgloszenie/">Opisz usterkę</a>
    </div>
    <p class="hero-g"><a href="{GMAPS}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">★★★★<i>★</i></span> 4,4 w&nbsp;Google, 10 opinii</a></p>
  </div>
  <div class="scooter-box">
    <p class="scooter-hint">Co się zepsuło? Kliknij część na&nbsp;rysunku.</p>
    {SVG}
    <div class="parts-list" role="tablist" aria-label="Część hulajnogi">
      <button role="tab" data-part="opony">Opony i dętki</button><button role="tab" data-part="hamulce">Hamulce</button><button role="tab" data-part="bateria">Bateria</button><button role="tab" data-part="sterownik">Sterownik</button><button role="tab" data-part="wyswietlacz">Wyświetlacz</button><button role="tab" data-part="luzy">Kierownica, luzy</button><button role="tab" data-part="silnik">Silnik, osiągi</button>
    </div>
    <div class="part-card" aria-live="polite">
      <h2 class="pc-t">Wybierz część</h2>
      <p class="pc-o" hidden><b>Typowe objawy:</b> <span></span></p>
      <p class="pc-r"><span>Pokażemy typowe objawy usterki i&nbsp;to, co z&nbsp;nią robimy w&nbsp;serwisie.</span></p>
      <a class="pc-btn" href="zgloszenie/" hidden>Zgłoś tę usterkę</a>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap split">
  <div class="split-l">
    <h2>Naprawa hulajnogi elektrycznej od&nbsp;dętki po&nbsp;sterownik</h2>
    <p>Serwisujemy hulajnogi elektryczne różnych marek, m.in. Xiaomi, Segway-Ninebot, Motus, Kugoo i&nbsp;Blaupunkt. Robimy wymianę dętek i&nbsp;opon, naprawy hamulców, sterowników i&nbsp;wyświetlaczy, regenerację baterii oraz przeglądy przed sezonem.</p>
    <p>Koszt naprawy podajemy po&nbsp;sprawdzeniu sprzętu, zanim zaczniemy pracę.</p>
    <p><a class="btn outline" href="naprawy/">Pełny zakres napraw</a></p>
  </div>
  <ul class="zakres">{zak}</ul>
</div></section>

<section class="sec white"><div class="wrap split">
  <div class="split-l">
    <h2>Odbiór hulajnogi z&nbsp;domu w&nbsp;promieniu 30&nbsp;km</h2>
    <p>Rozładowana hulajnoga waży swoje, a&nbsp;nie każdy ma ją czym przywieźć. Z&nbsp;Kutna i&nbsp;okolicznych miejscowości możemy odebrać sprzęt, naprawić go i&nbsp;odwieźć z&nbsp;powrotem.</p>
    <p><a class="btn outline" href="odbior/">Sprawdź swoją miejscowość na&nbsp;mapie</a></p>
  </div>
  <div class="split-r">
    <table class="dist"><caption>Odległość od&nbsp;serwisu w&nbsp;linii prostej</caption>{bl}</table>
  </div>
</div></section>

<section class="sec"><div class="wrap pair">
  <figure class="pair-img"><img src="img/skuter-1200.webp" srcset="img/skuter-700.webp 700w, img/skuter-1200.webp 1200w" sizes="(max-width:860px) 100vw, 50vw" width="1200" height="900" alt="Naprawa skutera elektrycznego w Kutnie – otwarta komora akumulatorów" loading="lazy" decoding="async"><figcaption>Skuter elektryczny w&nbsp;trakcie naprawy</figcaption></figure>
  <div class="pair-txt">
    <h2>Serwis rowerów, skuterów i&nbsp;wózków elektrycznych</h2>
    <p>Do&nbsp;serwisu trafiają nie tylko hulajnogi. Naprawiamy rowery elektryczne, skutery elektryczne, także inwalidzkie dla seniorów, oraz elektryczne wózki inwalidzkie: elektrykę, akumulatory, sterowanie, hamulce i&nbsp;mechanikę.</p>
    <p><a class="btn outline" href="naprawy/#rowery">Rowery</a><a class="btn outline" href="naprawy/#wozki">Wózki</a><a class="btn outline" href="naprawy/#skutery">Skutery</a></p>
    <p>Masz nietypowy sprzęt? Zadzwoń pod&nbsp;<a class="u" href="tel:{TEL}">{TEL_H}</a> i&nbsp;opisz, co się dzieje.</p>
  </div>
</div></section>

<section class="sec white"><div class="wrap">
  <div class="head-row"><h2>Opinie z&nbsp;Google</h2><p><a class="u" href="{GMAPS}" target="_blank" rel="noopener">Średnia 4,4 z&nbsp;10 opinii</a></p></div>
  <div class="revs">{revs}</div>
</div></section>

<section class="cta"><div class="wrap cta-in">
  <p class="cta-t">Hulajnoga nie jedzie? Zadzwoń, powiemy, co dalej.</p>
  <div class="actions"><a class="btn hot" href="tel:{TEL}">{TEL_H}</a><a class="btn ghost" href="zgloszenie/">Formularz zgłoszenia</a></div>
</div></section>'''
page('', 'Serwis hulajnóg elektrycznych Kutno – naprawa hulajnogi | tel. 889 503 420',
     'Serwis i naprawa hulajnóg elektrycznych w Kutnie: dętki i opony, hamulce, sterowniki, regeneracja baterii. Naprawiamy też rowery, skutery i wózki elektryczne. Odbiór z okolic do 30 km.', home)

# ------------------------------------------------------------------ NAPRAWY
SEK = [
    ('jezdny', ['opony', 'luzy'], 'Wymiana dętki i&nbsp;opony, luzy, zawieszenie',
     'Przebita dętka to najczęstszy powód wizyty w&nbsp;serwisie hulajnóg. Wymieniamy dętki i&nbsp;opony w&nbsp;hulajnogach elektrycznych, także w&nbsp;popularnych modelach Xiaomi i&nbsp;Motus, kasujemy luzy na&nbsp;kierownicy i&nbsp;mechanizmie składania oraz naprawiamy zawieszenie.',
     ['kapeć albo powietrze schodzi po&nbsp;kilku dniach', 'starty bieżnik, hulajnoga ślizga się na&nbsp;mokrym', 'luz na&nbsp;kierownicy, stukanie przy jeździe po&nbsp;nierównościach', 'drgania i&nbsp;skrzypienie zawieszenia'],
     ['wymiana dętek i&nbsp;opon (przód i&nbsp;tył)', 'kasowanie luzów kolumny kierownicy i&nbsp;mechanizmu składania', 'naprawa zawieszenia'], 'opony'),
    ('hamulce', ['hamulce'], 'Naprawa i&nbsp;regulacja hamulców',
     'Hamulec to element, którego nie warto odkładać na&nbsp;później. Regulujemy i&nbsp;naprawiamy hamulce w&nbsp;hulajnogach elektrycznych, wymieniamy klocki i&nbsp;tarcze hamulcowe.',
     ['hamulec słabo trzyma albo trzeba mocno ściskać dźwignię', 'piszczenie i&nbsp;ocieranie tarczy', 'luźna lub zbyt twarda dźwignia hamulca'],
     ['regulacja hamulców', 'naprawa hamulców', 'wymiana klocków hamulcowych', 'wymiana tarcz'], 'hamulce'),
    ('elektronika', ['sterownik', 'wyswietlacz'], 'Naprawa sterownika, płyty i&nbsp;wyświetlacza',
     'Gdy hulajnoga elektryczna nie włącza się, wyłącza się podczas jazdy albo szarpie przy ruszaniu, przyczyna często leży w&nbsp;elektronice. Naprawiamy sterowniki i&nbsp;płyty główne, wyświetlacze i&nbsp;manetki gazu, szukamy przetartych przewodów i&nbsp;luźnych złączy.',
     ['hulajnoga nie włącza się mimo naładowanej baterii', 'wyłącza się podczas jazdy', 'szarpie przy ruszaniu albo nie reaguje na&nbsp;gaz', 'kod błędu na&nbsp;wyświetlaczu (np. 14, 15, 18 lub 21 w&nbsp;hulajnogach Xiaomi)'],
     ['naprawa sterowników i&nbsp;płyt', 'naprawa i&nbsp;wymiana wyświetlaczy', 'diagnoza i&nbsp;usuwanie kodów błędów', 'naprawa instalacji elektrycznej'], 'sterownik'),
    ('baterie', ['bateria'], 'Regeneracja baterii hulajnogi',
     'Bateria to najdroższa część hulajnogi elektrycznej, dlatego zanim wymienisz ją na&nbsp;nową, warto sprawdzić, czy da się ją uratować. Diagnozujemy baterie, robimy renowację, regenerację i&nbsp;kalibrację ogniw.',
     ['zasięg wyraźnie spadł', 'hulajnoga gaśnie pod obciążeniem, np. pod górę', 'bateria nie ładuje się albo ładowarka nie kończy ładowania'],
     ['diagnostyka baterii', 'renowacja i&nbsp;regeneracja', 'kalibracja ogniw'], 'bateria'),
    ('tuning', ['silnik'], 'Modernizacje i&nbsp;odblokowanie prędkości',
     'Na&nbsp;życzenie modernizujemy hulajnogi elektryczne: poprawiamy osiągi i&nbsp;zmieniamy blokady prędkości. Pamiętaj, że po&nbsp;drogach publicznych hulajnoga elektryczna może jechać najwyżej 20&nbsp;km/h, szybciej wolno jeździć tylko po&nbsp;terenie prywatnym.',
     ['hulajnoga słabo przyspiesza', 'nie daje rady pod górę', 'chcesz zmienić ustawienia fabryczne'],
     ['poprawa osiągów', 'zmiana blokad prędkości', 'modyfikacje na&nbsp;życzenie'], 'silnik'),
    ('przeglad', ['*'], 'Przegląd hulajnogi elektrycznej',
     'Przegląd przed sezonem albo po&nbsp;zimie wyłapuje usterki, zanim zatrzymają cię w&nbsp;trasie. Sprawdzamy hamulce, luzy, opony, elektrykę i&nbsp;baterię, a&nbsp;przy okazji czyścimy i&nbsp;smarujemy sprzęt.',
     ['hulajnoga stała całą zimę', 'od dawna nikt jej nie sprawdzał', 'jeździsz codziennie do&nbsp;pracy lub szkoły'],
     ['sprawdzenie hamulców, luzów i&nbsp;opon', 'kontrola elektryki i&nbsp;baterii', 'czyszczenie i&nbsp;smarowanie'], 'przeglad'),
]
secs = ''
for i, (k, parts, h, txt, obj, rob, pick) in enumerate(SEK):
    secs += f'''<section class="srv" id="{k}"><div class="wrap srv-in">
  <div class="srv-pic">{mini(parts, i)}</div>
  <div class="srv-txt">
    <h2>{h}</h2>
    <p>{txt}</p>
    <div class="srv-cols">
      <div><h3>Typowe objawy</h3><ul>{''.join('<li>%s</li>' % x for x in obj)}</ul></div>
      <div><h3>Co robimy</h3><ul>{''.join('<li>%s</li>' % x for x in rob)}</ul></div>
    </div>
    <p class="srv-a"><a class="btn outline" href="../zgloszenie/?czesc={pick}">Zgłoś tę naprawę</a></p>
  </div>
</div></section>'''
ROWER = '''<svg class="ill" viewBox="0 0 400 270" aria-hidden="true" focusable="false">
  <line class="g" x1="10" y1="250" x2="390" y2="250"/>
  <circle class="w" cx="90" cy="185" r="60"/><circle class="w" cx="312" cy="185" r="60"/>
  <circle class="hub on" cx="90" cy="185" r="18"/><circle class="ax" cx="312" cy="185" r="5"/>
  <path class="s" d="M90 185 L192 190 L168 92 Z M168 92 L272 86 L192 190 M272 86 L312 185 M262 66 L272 86"/>
  <rect class="bat on" x="206" y="98" width="22" height="78" rx="5" transform="rotate(38 217 137)"/>
  <rect class="ctl on" x="176" y="182" width="30" height="18" rx="3"/>
  <path class="s" d="M146 82 H192 M250 62 L284 56"/><rect class="disp on" x="258" y="50" width="16" height="11" rx="2"/>
  <circle class="s" cx="192" cy="190" r="12"/>
</svg>'''
WOZEK = '''<svg class="ill" viewBox="0 0 400 270" aria-hidden="true" focusable="false">
  <line class="g" x1="10" y1="250" x2="390" y2="250"/>
  <path class="s" d="M100 219 V192 H322 V219"/>
  <circle class="w" cx="205" cy="198" r="46"/><circle class="ax" cx="205" cy="198" r="7"/>
  <circle class="w sm" cx="100" cy="234" r="15"/><circle class="w sm" cx="322" cy="234" r="15"/>
  <rect class="bat on" x="138" y="150" width="134" height="32" rx="4"/>
  <path class="s" d="M282 146 L318 205 H348"/>
  <rect class="seat" x="118" y="122" width="172" height="22" rx="6"/>
  <rect class="seat" x="110" y="38" width="24" height="92" rx="7" transform="rotate(-8 122 84)"/>
  <path class="s" d="M146 98 H268 M260 98 V122 M268 98 L282 84"/><circle class="joy on" cx="286" cy="80" r="8"/>
</svg>'''
EXTRA = [
    ('rowery', ROWER, 'Serwis rowerów elektrycznych',
     'Rower elektryczny ma tę samą elektrykę co hulajnoga: baterię, sterownik, silnik i&nbsp;wyświetlacz, więc w&nbsp;serwisie trafia na&nbsp;ten sam stół. Naprawiamy rowery elektryczne z&nbsp;silnikiem w&nbsp;piaście i&nbsp;centralnym, szukamy przyczyny, gdy nie działa wspomaganie, i&nbsp;zajmujemy się baterią, sterownikiem i&nbsp;ładowarką.',
     ['nie działa wspomaganie albo działa raz tak, raz nie', 'nie działa wyświetlacz lub manetka', 'zasięg na&nbsp;baterii wyraźnie spadł', 'ładowarka nie ładuje baterii'],
     ['naprawa sterownika roweru elektrycznego', 'diagnostyka i&nbsp;regeneracja baterii', 'naprawa instalacji, wyświetlacza i&nbsp;manetki', 'hamulce i&nbsp;mechanika'], 'Rower elektryczny'),
    ('wozki', WOZEK, 'Naprawa wózków inwalidzkich elektrycznych',
     'Elektryczny wózek inwalidzki to dla wielu osób jedyny sposób, żeby wyjść z&nbsp;domu, więc każda awaria jest pilna. Naprawiamy elektrykę, akumulatory, sterowanie i&nbsp;mechanikę wózków elektrycznych dla seniorów i&nbsp;osób z&nbsp;niepełnosprawnością. Z&nbsp;Kutna i&nbsp;okolic do&nbsp;30&nbsp;km możemy odebrać wózek spod domu.',
     ['wózek nie rusza albo nie reaguje na&nbsp;joystick', 'akumulatory szybko się rozładowują', 'wózek zatrzymuje się w&nbsp;trakcie jazdy', 'stuki, luzy albo zużyte kółka'],
     ['diagnostyka i&nbsp;naprawa elektryki', 'akumulatory', 'naprawa sterowania', 'mechanika i&nbsp;kółka'], 'Wózek elektryczny'),
    ('skutery', None, 'Naprawa skuterów elektrycznych',
     'Naprawiamy skutery elektryczne, także trzykołowe i&nbsp;czterokołowe skutery inwalidzkie dla seniorów. Zajmujemy się akumulatorami, elektryką, hamulcami i&nbsp;mechaniką. Na&nbsp;zdjęciu skuter z&nbsp;otwartą komorą akumulatorów w&nbsp;trakcie naprawy.',
     ['skuter nie rusza albo gaśnie w&nbsp;trakcie jazdy', 'akumulatory nie trzymają ładunku', 'słabo hamuje', 'nie działa licznik, światła lub kierunkowskazy'],
     ['akumulatory i&nbsp;ładowanie', 'elektryka i&nbsp;sterownik', 'hamulce', 'mechanika'], 'Skuter elektryczny'),
]
for k, pic, h, txt, obj, rob, typ in EXTRA:
    picd = f'<div class="srv-pic">{pic}</div>' if pic else '<div class="srv-pic photo"><img src="../img/skuter-700.webp" width="700" height="525" alt="Naprawa skutera inwalidzkiego elektrycznego w Kutnie – otwarta komora akumulatorów" loading="lazy" decoding="async"></div>'
    secs += f'''<section class="srv" id="{k}"><div class="wrap srv-in">
  {picd}
  <div class="srv-txt">
    <h2>{h}</h2>
    <p>{txt}</p>
    <div class="srv-cols">
      <div><h3>Typowe objawy</h3><ul>{''.join('<li>%s</li>' % x for x in obj)}</ul></div>
      <div><h3>Co robimy</h3><ul>{''.join('<li>%s</li>' % x for x in rob)}</ul></div>
    </div>
    <p class="srv-a"><a class="btn outline" href="../zgloszenie/?typ={typ.replace(' ', '+')}">Zgłoś naprawę</a></p>
  </div>
</div></section>'''

FAQ = [
    ('Ile kosztuje naprawa hulajnogi elektrycznej?', 'Zależy od&nbsp;usterki i&nbsp;modelu. Wymiana dętki to inna praca niż naprawa sterownika czy regeneracja baterii. Najpierw sprawdzamy, co jest przyczyną, i&nbsp;mówimy, ile będzie kosztować naprawa, a&nbsp;dopiero potem ją robimy.'),
    ('Dlaczego hulajnoga elektryczna nie włącza się?', 'Najczęstsze przyczyny to rozładowana lub uszkodzona bateria, zabezpieczenie baterii (BMS), które odcięło zasilanie, przetarty przewód w&nbsp;kolumnie kierownicy albo uszkodzony sterownik lub wyświetlacz. Bez pomiarów trudno wskazać jedną z&nbsp;nich, dlatego zaczynamy od&nbsp;diagnozy.'),
    ('Dlaczego hulajnoga wyłącza się podczas jazdy?', 'Zwykle winne jest napięcie baterii, które spada pod obciążeniem, luźne złącze albo przegrzewający się sterownik. Jeśli hulajnoga gaśnie np. pod górę albo przy mocnym przyspieszaniu, warto sprawdzić baterię.'),
    ('Hulajnoga szarpie przy ruszaniu. Co to może być?', 'Często to manetka gazu, czujniki w&nbsp;silniku albo luźne połączenie między silnikiem a&nbsp;sterownikiem. Takiej usterki nie warto rozjeżdżać, bo może się pogłębić.'),
    ('Co oznacza kod błędu na wyświetlaczu?', 'Kod błędu wskazuje, który układ hulajnogi zgłasza problem, np. silnik, sterownik, hamulec czy baterię. Zapisz go albo zrób zdjęcie wyświetlacza i&nbsp;podaj w&nbsp;zgłoszeniu, to przyspiesza diagnozę.'),
    ('Czy regenerujecie baterie do hulajnóg Xiaomi?', 'Tak. Robimy diagnostykę, renowację i&nbsp;regenerację baterii hulajnóg elektrycznych, w&nbsp;tym Xiaomi, oraz kalibrację ogniw.'),
    ('Czy można odblokować prędkość w hulajnodze?', 'Tak, zajmujemy się modernizacjami i&nbsp;zmianą blokad prędkości. Na&nbsp;drogach publicznych hulajnoga elektryczna może jechać najwyżej 20&nbsp;km/h, szybsza jazda jest dozwolona tylko na&nbsp;terenie prywatnym.'),
    ('Rower elektryczny – nie działa wspomaganie. Co może być przyczyną?', 'Najczęściej czujnik prędkości i&nbsp;magnes na&nbsp;szprysze, uszkodzony przewód albo złącze, czujnik pedałowania, sterownik lub bateria. Sprawdzamy układ po&nbsp;kolei i&nbsp;mówimy, co trzeba wymienić.'),
    ('Czy naprawiacie elektryczne wózki inwalidzkie i skutery dla seniorów?', 'Tak. Naprawiamy elektrykę, akumulatory, sterowanie, hamulce i&nbsp;mechanikę wózków i&nbsp;skuterów elektrycznych. Jeśli wózek nie jedzie, z&nbsp;Kutna i&nbsp;okolic do&nbsp;30&nbsp;km możemy go odebrać spod domu.'),
    ('Czy trzeba się umawiać?', f'Najlepiej zadzwoń przed przyjazdem pod&nbsp;{TEL_H}. Upewnimy się, że ktoś jest na&nbsp;miejscu, i&nbsp;od&nbsp;razu wstępnie opowiesz, co się dzieje.'),
]
faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', H.unescape(a))}} for q, a in FAQ]}
srv_ld = {"@type": "OfferCatalog", "name": "Naprawy pojazdów elektrycznych", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": H.unescape(re.sub('<[^>]+>', '', x)), "provider": {"@id": URL + "#serwis"}, "areaServed": "Kutno"}} for x in [e[2] for e in SEK] + [e[2] for e in EXTRA]]}

skok = ''.join(f'<a href="#{k}">{H.unescape(t).replace(chr(160), " ")}</a>' for k, t in [(s[0], re.sub('<[^>]+>', '', s[2])) for s in SEK] + [('rowery', 'Rowery elektryczne'), ('wozki', 'Wózki elektryczne'), ('skutery', 'Skutery elektryczne'), ('pytania', 'Pytania')])
napr = band('Naprawy', 'Naprawa hulajnóg, rowerów, skuterów i&nbsp;wózków elektrycznych w&nbsp;Kutnie',
            'Dętki i&nbsp;opony, hamulce, sterowniki, wyświetlacze, baterie i&nbsp;modernizacje hulajnóg, a&nbsp;także serwis rowerów elektrycznych, skuterów i&nbsp;elektrycznych wózków inwalidzkich. Poniżej typowe objawy usterek i&nbsp;to, co z&nbsp;nimi robimy.') + \
    f'<nav class="jump" aria-label="Na tej stronie"><div class="wrap">{skok}</div></nav>' + secs + f'''
<section class="sec white" id="pytania"><div class="wrap faq-wrap">
  <h2>Pytania o&nbsp;naprawy</h2>
  <div class="faq">{faq}</div>
</div></section>'''
page('naprawy/', 'Naprawa hulajnogi elektrycznej, roweru, skutera i wózka elektrycznego – Kutno',
     'Naprawa hulajnóg elektrycznych w Kutnie: dętki i opony, hamulce, sterowniki, wyświetlacze, regeneracja baterii. Serwis rowerów elektrycznych, skuterów i wózków inwalidzkich elektrycznych.', napr, [faq_ld, srv_ld])

# ------------------------------------------------------------------ ZGŁOSZENIE
zg = band('Zgłoś naprawę', 'Zgłoś naprawę hulajnogi elektrycznej',
          'Opisz usterkę w&nbsp;czterech krokach. Na&nbsp;końcu wyślesz gotową wiadomość SMS-em albo mailem, a&nbsp;my oddzwonimy.') + f'''
<section class="sec dark"><div class="wrap form-wrap">
  {FORM}
  <aside class="form-side">
    <h2>Jak wygląda naprawa</h2>
    <ol class="flow">
      <li><b>Zgłoszenie.</b> Telefonicznie albo przez formularz obok.</li>
      <li><b>Dostarczenie.</b> Przywozisz sprzęt na&nbsp;ul.&nbsp;Ściegiennego 25 w&nbsp;Kutnie albo odbieramy go od&nbsp;ciebie (do&nbsp;30&nbsp;km).</li>
      <li><b>Diagnoza.</b> Sprawdzamy, co jest przyczyną, i&nbsp;mówimy, ile będzie kosztować naprawa.</li>
      <li><b>Naprawa i&nbsp;odbiór.</b> Oddajemy sprawny sprzęt albo go odwozimy.</li>
    </ol>
    <p class="form-tel">Wolisz porozmawiać?<br><a href="tel:{TEL}">{TEL_H}</a></p>
    <p class="form-h">pon–pt 9:00–18:00<br>sob 10:00–15:00</p>
  </aside>
</div></section>'''
page('zgloszenie/', 'Zgłoś naprawę hulajnogi elektrycznej – serwis Kutno',
     'Formularz zgłoszenia naprawy hulajnogi, skutera lub roweru elektrycznego w Kutnie. Opisz usterkę, wybierz dostarczenie lub odbiór z domu i wyślij SMS albo mail.', zg)

# ------------------------------------------------------------------ ODBIÓR
rows = ''
for m in sorted([m for m in MIEJSCA if m['n'] != 'Kutno'], key=lambda m: m['d']):
    d = m['d']
    st = '<span class="ok">w zasięgu</span>' if d <= 30 else ('zadzwoń, ustalimy' if d <= 35 else 'poza strefą')
    rows += f'<tr><th>{m["n"]}</th><td>ok. {round(d)}&nbsp;km</td><td>{st}</td></tr>'
od = band('Odbiór z domu', 'Odbiór hulajnogi do&nbsp;serwisu – Kutno i&nbsp;okolice',
          'W&nbsp;promieniu 30&nbsp;km od&nbsp;serwisu możemy przyjechać po&nbsp;hulajnogę, rower, skuter albo wózek elektryczny, naprawić sprzęt i&nbsp;odwieźć z&nbsp;powrotem.') + f'''
<section class="sec"><div class="wrap odb-wrap">
  <div class="odb-txt">
    <h2>Sprawdź, czy przyjedziemy</h2>
    <p>Wpisz miejscowość albo użyj lokalizacji telefonu. Pokażemy odległość od&nbsp;serwisu przy ul.&nbsp;Ściegiennego 25 w&nbsp;Kutnie.</p>
    <label class="field chk"><span>Twoja miejscowość</span><input id="miasto" list="miejsca" placeholder="np. Krośniewice" autocomplete="off"></label>
    <datalist id="miejsca"></datalist>
    <button class="geo" type="button" id="geo">Użyj mojej lokalizacji</button>
    <p class="chk-out" id="chk-out" aria-live="polite"></p>
    <p class="note">Odległość liczymy w&nbsp;linii prostej. Przy samej granicy zadzwoń, ustalimy.</p>
  </div>
  <figure class="zmap"><div id="mapa" role="img" aria-label="Mapa: strefa odbioru 30 km wokół serwisu w Kutnie"></div>
    <figcaption><span class="lg lg-z"></span>strefa odbioru do&nbsp;30&nbsp;km<span class="lg lg-s"></span>serwis, ul.&nbsp;Ściegiennego 25</figcaption></figure>
</div></section>
<section class="sec white"><div class="wrap split">
  <div class="split-l">
    <h2>Serwis hulajnóg dla Krośniewic, Żychlina, Łęczycy i&nbsp;Gostynina</h2>
    <p>Najbliższy serwis hulajnóg elektrycznych nie musi być w&nbsp;Łodzi czy Płocku. Z&nbsp;miejscowości w&nbsp;strefie odbieramy sprzęt i&nbsp;odwozimy go po&nbsp;naprawie. Z&nbsp;dalszych możesz przywieźć hulajnogę sam albo zadzwonić i&nbsp;ustalić, czy dojedziemy.</p>
    <p><a class="btn outline" href="../zgloszenie/">Zamów odbiór</a></p>
  </div>
  <div class="split-r"><table class="dist full"><caption>Odległości od&nbsp;serwisu w&nbsp;linii prostej</caption><thead><tr><th>Miejscowość</th><td>Odległość</td><td>Odbiór</td></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''
page('odbior/', 'Odbiór hulajnogi do serwisu – Kutno, Krośniewice, Żychlin, Łęczyca, Gostynin',
     'Serwis hulajnóg elektrycznych z odbiorem z domu w promieniu 30 km od Kutna: Krośniewice, Żychlin, Łęczyca, Gostynin, Dąbrowice, Piątek. Sprawdź swoją miejscowość na mapie.', od,
     scripts='<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin="" defer></script>\n')

# ------------------------------------------------------------------ KONTAKT
DNI = [('1', 'Poniedziałek', '9:00–18:00'), ('2', 'Wtorek', '9:00–18:00'), ('3', 'Środa', '9:00–18:00'), ('4', 'Czwartek', '9:00–18:00'), ('5', 'Piątek', '9:00–18:00'), ('6', 'Sobota', '10:00–15:00'), ('0', 'Niedziela', 'nieczynne')]
hrs = ''.join(f'<tr data-d="{d}"><th>{n}</th><td>{g}</td></tr>' for d, n, g in DNI)
ko = band('Kontakt', 'Kontakt z&nbsp;serwisem hulajnóg w&nbsp;Kutnie',
          'Zadzwoń, napisz SMS albo przyjedź na&nbsp;ul.&nbsp;Księdza Piotra Ściegiennego 25. Przed przyjazdem najlepiej zadzwoń.') + f'''
<section class="sec"><div class="wrap kontakt">
  <div class="k-txt">
    <p class="k-l">Telefon</p>
    <p class="k-tel"><a href="tel:{TEL}">{TEL_H}</a></p>
    <p class="k-l">E-mail</p>
    <p><a class="u" href="mailto:{MAIL}">{MAIL}</a></p>
    <p class="k-l">Adres serwisu</p>
    <p>ul. Księdza Piotra Ściegiennego 25<br>99-300 Kutno</p>
    <p class="k-l">Godziny otwarcia</p>
    <table class="hours">{hrs}</table>
    <p class="actions"><a class="btn hot" href="https://www.google.com/maps/dir/?api=1&amp;destination=52.2236904,19.3550328" target="_blank" rel="noopener">Wyznacz trasę</a><a class="btn outline" href="../zgloszenie/">Zgłoś naprawę</a></p>
  </div>
  <div class="k-map"><iframe title="Mapa dojazdu do serwisu hulajnóg w Kutnie" src="https://maps.google.com/maps?q=52.2236904,19.3550328&amp;z=15&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''
page('kontakt/', 'Kontakt – serwis hulajnóg elektrycznych Kutno, ul. Ściegiennego 25',
     'Serwis hulajnóg elektrycznych w Kutnie, ul. Księdza Piotra Ściegiennego 25. Tel. 889 503 420. Czynne pon–pt 9–18, sob 10–15. Mapa dojazdu.', ko)

# ------------------------------------------------------------------ sitemap, robots
sm = ''.join(f'<url><loc>{URL}{p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if not p else "0.8"}</priority></url>' for p, _ in NAV)
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sm + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n')
print('ok')
