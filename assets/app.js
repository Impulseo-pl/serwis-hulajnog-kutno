(function () {
  'use strict';
  var TEL = '+48889503420', MAIL = 'Revoltec@vp.pl';
  var HOME = { lat: 52.2236904, lon: 19.3550328 }, ZASIEG = 30;

  /* ---------- menu ---------- */
  var burger = document.querySelector('.burger'), menu = document.getElementById('menu');
  burger.addEventListener('click', function () {
    var o = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', o); menu.classList.toggle('open', o);
  });
  menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') { burger.setAttribute('aria-expanded', 'false'); menu.classList.remove('open'); } });

  /* ---------- otwarte / zamknięte (czas w Polsce) ---------- */
  var GODZ = { 1: [9, 18], 2: [9, 18], 3: [9, 18], 4: [9, 18], 5: [9, 18], 6: [10, 15], 0: null };
  var DNI = ['w niedzielę', 'w poniedziałek', 'we wtorek', 'w środę', 'w czwartek', 'w piątek', 'w sobotę'];
  function teraz() {
    var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Warsaw', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date());
    var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
    return { d: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(o.weekday), h: +o.hour + (+o.minute) / 60 };
  }
  (function () {
    var el = document.querySelector('[data-status]'); if (!el) return;
    var t = teraz(), g = GODZ[t.d];
    var row = document.querySelector('.hours tr[data-d="' + t.d + '"]'); if (row) row.classList.add('today');
    if (g && t.h >= g[0] && t.h < g[1]) { el.textContent = 'Otwarte dziś do ' + g[1] + ':00'; el.classList.add('open'); return; }
    if (g && t.h < g[0]) { el.textContent = 'Dziś otwieramy o ' + g[0] + ':00'; el.classList.add('closed'); return; }
    for (var i = 1; i <= 7; i++) {
      var d = (t.d + i) % 7;
      if (GODZ[d]) { el.textContent = 'Teraz zamknięte · otwieramy ' + (i === 1 ? 'jutro' : DNI[d]) + ' o ' + GODZ[d][0] + ':00'; el.classList.add('closed'); return; }
    }
  })();

  /* ---------- rysunek hulajnogi ---------- */
  var CZESCI = {
    opony: { t: 'Opony i dętki', o: 'kapeć, powietrze ucieka po kilku dniach, starty bieżnik, hulajnoga ślizga się na zakrętach.', r: 'wymieniamy opony i dętki, sprawdzamy przy okazji obręcz i wentyl.' },
    hamulce: { t: 'Hamulce', o: 'hamulec słabo trzyma, piszczy albo ociera, dźwignia chodzi za lekko lub za ciężko.', r: 'naprawiamy i regulujemy hamulce, wymieniamy klocki i tarcze.' },
    bateria: { t: 'Bateria', o: 'zasięg wyraźnie spadł, hulajnoga gaśnie pod obciążeniem albo nie chce się ładować.', r: 'diagnostyka baterii, renowacja i regeneracja, kalibracja ogniw.' },
    sterownik: { t: 'Sterownik i elektryka', o: 'hulajnoga się nie włącza, wyłącza się w trakcie jazdy, silnik szarpie albo nie reaguje na gaz.', r: 'naprawiamy sterowniki i płyty, szukamy i usuwamy usterki elektryczne.' },
    wyswietlacz: { t: 'Wyświetlacz', o: 'ekran nie świeci, pokazuje kod błędu, nie działają przyciski albo manetka gazu.', r: 'naprawiamy lub wymieniamy wyświetlacz, odczytujemy i usuwamy błędy.' },
    luzy: { t: 'Kierownica, luzy i zawieszenie', o: 'coś stuka przy jeździe, kolumna kierownicy ma luz, hulajnoga drga na nierównościach.', r: 'kasujemy luzy na kierownicy i mechanizmie składania, naprawiamy zawieszenie.' },
    silnik: { t: 'Silnik i osiągi', o: 'chcesz mocniej przyspieszać, lepiej podjeżdżać pod górę albo zmienić ustawienia.', r: 'modernizacje i tuning: poprawa osiągów, zmiana blokad prędkości.' }
  };
  var svg = document.querySelector('.scooter'), card = document.querySelector('.part-card');
  var wybrana = null;
  function pokaz(k, przewin) {
    var c = CZESCI[k]; if (!c) return;
    wybrana = k;
    svg.querySelectorAll('.part, .co').forEach(function (el) { el.classList.toggle('on', el.getAttribute('data-part') === k); });
    document.querySelectorAll('.parts-list button').forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-part') === k); });
    card.querySelector('.pc-t').textContent = c.t;
    card.querySelector('.pc-o span').textContent = c.o.charAt(0).toUpperCase() + c.o.slice(1);
    card.querySelector('.pc-r span').textContent = c.r.charAt(0).toUpperCase() + c.r.slice(1);
    card.querySelector('.pc-o').hidden = false;
    card.querySelector('.pc-btn').hidden = false;
    if (!card.querySelector('.pc-r b')) card.querySelector('.pc-r').insertAdjacentHTML('afterbegin', '<b>Co robimy:</b> ');
    if (przewin && card.getBoundingClientRect().bottom > innerHeight) card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
  svg.addEventListener('click', function (e) {
    var el = e.target.closest('[data-part]'); if (el) pokaz(el.getAttribute('data-part'), true);
  });
  document.querySelectorAll('.parts-list button').forEach(function (b) {
    b.addEventListener('click', function () { pokaz(b.getAttribute('data-part'), true); });
  });
  card.querySelector('.pc-btn').addEventListener('click', function () { if (wybrana) zaznacz(wybrana); });
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) svg.classList.add('draw');

  /* ---------- formularz ---------- */
  var form = document.getElementById('form');
  function zaznacz(g) {
    form.querySelectorAll('input[name=obj]').forEach(function (i) { if (i.getAttribute('data-g') === g) i.checked = true; });
  }
  document.querySelectorAll('[data-pick]').forEach(function (a) {
    a.addEventListener('click', function () { zaznacz(a.getAttribute('data-pick')); });
  });
  var odb = form.querySelector('.odb'), odbInfo = form.querySelector('.odb-info');
  form.addEventListener('change', function (e) {
    if (e.target.name === 'dost') {
      var on = e.target.value === 'Proszę o odbiór';
      odb.hidden = !on; odbInfo.hidden = !on;
      if (on) odb.querySelector('input').focus();
    }
  });

  /* ---------- odległości ---------- */
  function km(a, b) {
    var r = Math.PI / 180, dLa = (b.lat - a.lat) * r, dLo = (b.lon - a.lon) * r;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2);
    return 2 * 6371 * Math.asin(Math.sqrt(h));
  }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ł/g, 'l').trim(); }
  var MIEJSCA = [];
  function znajdz(txt) {
    var n = norm(txt.split(',')[0]); if (n.length < 3) return null;
    var hit = null;
    MIEJSCA.forEach(function (m) { var mn = norm(m.n); if (mn === n || (!hit && mn.indexOf(n) === 0)) hit = m; });
    return hit;
  }
  function werdykt(d) {
    if (d <= ZASIEG) return 'ok';
    if (d <= ZASIEG + 5) return 'granica';
    return 'poza';
  }
  function fmt(d) { return d < 1.5 ? 'na miejscu' : 'ok. ' + Math.round(d) + ' km'; }

  odb.querySelector('input').addEventListener('input', function () {
    var m = znajdz(this.value);
    if (!m) { odbInfo.textContent = ''; return; }
    var w = werdykt(m.km);
    odbInfo.innerHTML = w === 'ok' ? m.n + ': ' + fmt(m.km) + ' od serwisu. <b>W zasięgu odbioru.</b>'
      : w === 'granica' ? m.n + ': ' + fmt(m.km) + ' od serwisu, tuż za granicą 30 km. Zadzwoń, ustalimy.'
      : m.n + ': ' + fmt(m.km) + ' od serwisu, poza strefą odbioru. Możesz przywieźć sprzęt na Ściegiennego 25.';
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form), err = form.querySelector('.form-err');
    var tel = (f.get('tel') || '').replace(/[^\d+]/g, '');
    if (tel.length < 9) { err.hidden = false; form.querySelector('[name=tel]').focus(); return; }
    err.hidden = true;
    var obj = f.getAll('obj');
    var L = [];
    L.push('Dzień dobry, zgłaszam usterkę.');
    L.push('Sprzęt: ' + f.get('typ') + (f.get('model') ? ' – ' + f.get('model') : ''));
    if (obj.length) L.push('Co się dzieje: ' + obj.join(', '));
    if (f.get('opis')) L.push('Opis: ' + f.get('opis'));
    L.push('Dostarczenie: ' + f.get('dost') + (f.get('dost') === 'Proszę o odbiór' && f.get('adres') ? ' – ' + f.get('adres') : ''));
    L.push((f.get('imie') ? f.get('imie') + ', ' : '') + 'tel. ' + f.get('tel'));
    var txt = L.join('\n');
    var box = form.querySelector('.msg');
    box.querySelector('.msg-t').textContent = txt;
    var sep = /iPhone|iPad|Mac/.test(navigator.userAgent) ? '&' : '?';
    box.querySelector('[data-sms]').href = 'sms:' + TEL + sep + 'body=' + encodeURIComponent(txt);
    box.querySelector('[data-mail]').href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Zgłoszenie usterki – ' + f.get('typ')) + '&body=' + encodeURIComponent(txt);
    box.hidden = false;
    box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });

  /* ---------- mapa strefy odbioru ---------- */
  var radar = document.getElementById('radar'), out = document.getElementById('chk-out'), inp = document.getElementById('miasto');
  var NS = 'http://www.w3.org/2000/svg', SKALA = 200 / ZASIEG; // 30 km = 200 px
  var ETYK = ['Żychlin', 'Krośniewice', 'Łęczyca', 'Gostynin', 'Kłodawa', 'Łowicz', 'Płock', 'Piątek', 'Ozorków', 'Gąbin', 'Dąbrowice', 'Strzelce', 'Witonia', 'Sanniki', 'Oporów'];
  var DUZE = ['Żychlin', 'Krośniewice', 'Łęczyca', 'Gostynin', 'Kłodawa', 'Łowicz', 'Płock', 'Piątek', 'Ozorków', 'Gąbin', 'Dąbrowice', 'Sanniki', 'Kiernozia', 'Oporów', 'Strzelce', 'Bedlno', 'Witonia', 'Daszyna', 'Nowe Ostrowy', 'Grabów', 'Chodów', 'Pacyna', 'Szczawin Kościelny', 'Dobrzelin', 'Łanięta', 'Krzyżanów', 'Góra Świętej Małgorzaty'];
  function xy(m) {
    var x = (m.lon - HOME.lon) * Math.cos(HOME.lat * Math.PI / 180) * 111.32 * SKALA;
    var y = -(m.lat - HOME.lat) * 110.57 * SKALA;
    return [x, y];
  }
  function el(n, a, p) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); (p || radar).appendChild(e); return e; }
  var linia = null, etykieta = null, punkty = {};
  function rysuj() {
    el('circle', { 'class': 'ring', cx: 0, cy: 0, r: 15 * SKALA });
    el('circle', { 'class': 'zone', cx: 0, cy: 0, r: ZASIEG * SKALA });
    el('circle', { 'class': 'ring', cx: 0, cy: 0, r: 40 * SKALA });
    el('text', { 'class': 'ring-l', x: 6, y: -ZASIEG * SKALA - 8 }).textContent = '30 km';
    el('text', { 'class': 'ring-l', x: 6, y: -15 * SKALA - 8 }).textContent = '15 km';
    MIEJSCA.forEach(function (m) {
      if (m.n === 'Kutno' || DUZE.indexOf(m.n) < 0) return;
      var p = xy(m); if (Math.abs(p[0]) > 290 || Math.abs(p[1]) > 290) return;
      var g = el('g', { 'class': 't' + (m.km > ZASIEG ? ' out' : '') + (['Żychlin', 'Krośniewice', 'Łęczyca', 'Gostynin', 'Kłodawa', 'Łowicz', 'Płock', 'Ozorków', 'Gąbin'].indexOf(m.n) > -1 ? ' big' : ''), transform: 'translate(' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + ')' });
      el('circle', { r: 4.5 }, g);
      var lewa = p[0] > 150;
      var t = el('text', { x: lewa ? -9 : 9, y: 5, 'text-anchor': lewa ? 'end' : 'start' }, g); t.textContent = m.n;
      if (ETYK.indexOf(m.n) < 0) g.classList.add('small');
      punkty[m.n] = g;
    });
    linia = el('line', { 'class': 'line', x1: 0, y1: 0, x2: 0, y2: 0, visibility: 'hidden' });
    etykieta = el('text', { 'class': 'km', 'text-anchor': 'middle', visibility: 'hidden' });
    var h = el('g', { 'class': 'home' });
    el('rect', { x: -9, y: -9, width: 18, height: 18 }, h);
    el('text', { x: 0, y: 30, 'text-anchor': 'middle' }, h).textContent = 'Kutno – serwis';
  }
  function zaznaczNaMapie(m, d) {
    Object.keys(punkty).forEach(function (k) { punkty[k].classList.toggle('sel', m && k === m.n); });
    if (!m) { linia.setAttribute('visibility', 'hidden'); etykieta.setAttribute('visibility', 'hidden'); return; }
    var p = xy(m), r = Math.hypot(p[0], p[1]), maks = 285;
    if (r > maks) { p = [p[0] * maks / r, p[1] * maks / r]; }
    linia.setAttribute('x2', p[0]); linia.setAttribute('y2', p[1]); linia.setAttribute('visibility', 'visible');
    etykieta.setAttribute('x', p[0] / 2); etykieta.setAttribute('y', p[1] / 2 - 8); etykieta.textContent = Math.round(d) + ' km';
    etykieta.setAttribute('visibility', d < 1.5 ? 'hidden' : 'visible');
  }
  function sprawdz(m, nazwa, d) {
    if (d == null) d = m.km;
    var w = werdykt(d);
    zaznaczNaMapie(m, d);
    out.innerHTML = w === 'ok'
      ? '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu. <span class="ok">W zasięgu odbioru.</span>'
      : w === 'granica'
        ? '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu, tuż za granicą 30 km. Zadzwoń pod <a class="u" href="tel:' + TEL + '">889 503 420</a>, ustalimy.'
        : '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu, poza strefą odbioru. Sprzęt możesz przywieźć na ul. Ściegiennego 25 w Kutnie.';
  }
  inp.addEventListener('input', function () {
    var m = znajdz(inp.value);
    if (m) sprawdz(m, m.n); else { out.textContent = ''; if (linia) zaznaczNaMapie(null); }
  });
  document.getElementById('geo').addEventListener('click', function () {
    if (!navigator.geolocation) { out.textContent = 'Twoja przeglądarka nie udostępnia lokalizacji.'; return; }
    out.textContent = 'Sprawdzam lokalizację…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      var me = { n: 'Twoja lokalizacja', lat: pos.coords.latitude, lon: pos.coords.longitude };
      var d = km(HOME, me);
      punkty[me.n] = punkty[me.n] || null;
      sprawdz(me, 'Twoja lokalizacja', d);
    }, function () { out.textContent = 'Nie udało się pobrać lokalizacji. Wpisz miejscowość.'; }, { timeout: 8000 });
  });

  fetch('assets/miejscowosci.json').then(function (r) { return r.json(); }).then(function (d) {
    MIEJSCA = d.map(function (m) { m.km = km(HOME, m); return m; });
    var dl = document.getElementById('miejsca');
    MIEJSCA.forEach(function (m) { var o = document.createElement('option'); o.value = m.n; dl.appendChild(o); });
    rysuj();
  }).catch(function () {});
})();
