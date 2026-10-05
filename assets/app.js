(function () {
  'use strict';
  var TEL = '+48889503420', MAIL = 'Revoltec@vp.pl';
  var HOME = { lat: 52.2236904, lon: 19.3550328 }, ZASIEG = 30;
  var BASE = document.body.getAttribute('data-base') || '';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- menu ---------- */
  var burger = $('.burger'), menu = $('#menu');
  burger.addEventListener('click', function () {
    var o = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', o); menu.classList.toggle('open', o);
  });

  /* ---------- godziny (czas w Polsce) ---------- */
  var GODZ = { 1: [9, 18], 2: [9, 18], 3: [9, 18], 4: [9, 18], 5: [9, 18], 6: [10, 15], 0: null };
  var DNI = ['w niedzielę', 'w poniedziałek', 'we wtorek', 'w środę', 'w czwartek', 'w piątek', 'w sobotę'];
  var t = (function () {
    var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Warsaw', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date());
    var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
    return { d: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(o.weekday), h: +o.hour + (+o.minute) / 60 };
  })();
  var row = $('.hours tr[data-d="' + t.d + '"]'); if (row) row.classList.add('today');
  var st = $('[data-status]');
  if (st) {
    var g = GODZ[t.d];
    if (g && t.h >= g[0] && t.h < g[1]) st.textContent = 'dziś czynne do ' + g[1] + ':00';
    else if (g && t.h < g[0]) st.textContent = 'dziś czynne od ' + g[0] + ':00';
    else for (var i = 1; i <= 7; i++) { var d = (t.d + i) % 7; if (GODZ[d]) { st.textContent = 'teraz zamknięte, otwieramy ' + (i === 1 ? 'jutro' : DNI[d]) + ' o ' + GODZ[d][0] + ':00'; break; } }
  }

  /* ---------- rysunek hulajnogi (strona główna) ---------- */
  var CZESCI = {
    opony: { t: 'Opony i dętki', o: 'kapeć, powietrze schodzi po kilku dniach, starty bieżnik.', r: 'wymiana dętek i opon, przód i tył.' },
    hamulce: { t: 'Hamulce', o: 'hamulec słabo trzyma, piszczy albo ociera, dźwignia chodzi za lekko lub za ciężko.', r: 'regulacja i naprawa hamulców, wymiana klocków i tarcz.' },
    bateria: { t: 'Bateria', o: 'zasięg wyraźnie spadł, hulajnoga gaśnie pod obciążeniem albo nie chce się ładować.', r: 'diagnostyka, renowacja i regeneracja baterii, kalibracja ogniw.' },
    sterownik: { t: 'Sterownik', o: 'hulajnoga nie włącza się, wyłącza się podczas jazdy albo szarpie przy ruszaniu.', r: 'naprawa sterowników i płyt, usuwanie usterek elektrycznych.' },
    wyswietlacz: { t: 'Wyświetlacz', o: 'ekran nie świeci, pokazuje kod błędu, nie działają przyciski albo manetka gazu.', r: 'naprawa lub wymiana wyświetlacza, diagnoza kodów błędów.' },
    luzy: { t: 'Kierownica, luzy, zawieszenie', o: 'luz na kierownicy, stukanie przy jeździe, drgania na nierównościach.', r: 'kasowanie luzów na kierownicy i mechanizmie składania, naprawa zawieszenia.' },
    silnik: { t: 'Silnik i osiągi', o: 'hulajnoga słabo przyspiesza, nie daje rady pod górę.', r: 'modernizacje: poprawa osiągów, zmiana blokad prędkości.' }
  };
  var svg = $('.scooter:not(.mini)'), card = $('.part-card');
  if (svg && card) {
    var pokaz = function (k, przewin) {
      var c = CZESCI[k]; if (!c) return;
      $$('.part, .co', svg).forEach(function (el) { el.classList.toggle('on', el.getAttribute('data-part') === k); });
      $$('.parts-list button').forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-part') === k); });
      $('.pc-t', card).textContent = c.t;
      $('.pc-o span', card).textContent = c.o.charAt(0).toUpperCase() + c.o.slice(1);
      $('.pc-o', card).hidden = false;
      $('.pc-r', card).innerHTML = '<b>Co robimy:</b> ' + c.r.charAt(0).toUpperCase() + c.r.slice(1);
      var a = $('.pc-btn', card); a.hidden = false; a.href = BASE + 'zgloszenie/?czesc=' + k;
      if (przewin && card.getBoundingClientRect().bottom > innerHeight) card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    };
    svg.addEventListener('click', function (e) { var el = e.target.closest('[data-part]'); if (el) pokaz(el.getAttribute('data-part'), true); });
    $$('.parts-list button').forEach(function (b) { b.addEventListener('click', function () { pokaz(b.getAttribute('data-part'), true); }); });
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) svg.classList.add('draw');
  }

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
  function werdykt(d) { return d <= ZASIEG ? 'ok' : d <= ZASIEG + 5 ? 'granica' : 'poza'; }
  function fmt(d) { return d < 1.5 ? 'na miejscu' : 'ok. ' + Math.round(d) + ' km'; }
  var potrzebaMiejsc = $('#form') || $('#mapa');
  var miejscaGotowe = potrzebaMiejsc ? fetch(BASE + 'assets/miejscowosci.json').then(function (r) { return r.json(); }).then(function (d) {
    MIEJSCA = d.map(function (m) { m.km = km(HOME, m); return m; });
    var dl = $('#miejsca');
    if (dl) MIEJSCA.forEach(function (m) { var o = document.createElement('option'); o.value = m.n; dl.appendChild(o); });
  }).catch(function () {}) : null;

  /* ---------- formularz zgłoszenia ---------- */
  var form = $('#form');
  if (form) {
    var qs = new URLSearchParams(location.search), q = qs.get('czesc'), typ = qs.get('typ');
    if (typ) $$('input[name=typ]', form).forEach(function (i) { i.checked = i.value === typ; });
    if (q) $$('input[name=obj]', form).forEach(function (i) { if (i.getAttribute('data-g') === q) i.checked = true; });
    var odb = $('.odb', form), odbInfo = $('.odb-info', form);
    var dl2 = $('#miejsca'); if (!dl2) { dl2 = document.createElement('datalist'); dl2.id = 'miejsca'; form.appendChild(dl2); }
    form.addEventListener('change', function (e) {
      if (e.target.name === 'dost') {
        var on = e.target.value === 'Proszę o odbiór';
        odb.hidden = !on; odbInfo.hidden = !on;
        if (on) $('input', odb).focus();
      }
    });
    $('input', odb).addEventListener('input', function () {
      var m = znajdz(this.value);
      if (!m) { odbInfo.textContent = ''; return; }
      var w = werdykt(m.km);
      odbInfo.innerHTML = w === 'ok' ? m.n + ': ' + fmt(m.km) + ' od serwisu. <b>W zasięgu odbioru</b>'
        : w === 'granica' ? m.n + ': ' + fmt(m.km) + ' od serwisu, tuż za granicą 30 km. Zadzwoń, ustalimy.'
        : m.n + ': ' + fmt(m.km) + ' od serwisu, poza strefą odbioru. Możesz przywieźć sprzęt na Ściegiennego 25.';
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), err = $('.form-err', form);
      var tel = (f.get('tel') || '').replace(/[^\d+]/g, '');
      if (tel.length < 9) { err.hidden = false; $('[name=tel]', form).focus(); return; }
      err.hidden = true;
      var obj = f.getAll('obj'), L = [];
      L.push('Dzień dobry, zgłaszam usterkę.');
      L.push('Sprzęt: ' + f.get('typ') + (f.get('model') ? ' – ' + f.get('model') : ''));
      if (obj.length) L.push('Co się dzieje: ' + obj.join(', '));
      if (f.get('opis')) L.push('Opis: ' + f.get('opis'));
      L.push('Dostarczenie: ' + f.get('dost') + (f.get('dost') === 'Proszę o odbiór' && f.get('adres') ? ' – ' + f.get('adres') : ''));
      L.push((f.get('imie') ? f.get('imie') + ', ' : '') + 'tel. ' + f.get('tel'));
      var txt = L.join('\n'), box = $('.msg', form);
      $('.msg-t', box).textContent = txt;
      var sep = /iPhone|iPad|Mac/.test(navigator.userAgent) ? '&' : '?';
      $('[data-sms]', box).href = 'sms:' + TEL + sep + 'body=' + encodeURIComponent(txt);
      $('[data-mail]', box).href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Zgłoszenie usterki – ' + f.get('typ')) + '&body=' + encodeURIComponent(txt);
      box.hidden = false;
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  }

  /* ---------- mapa strefy odbioru (Leaflet) ---------- */
  var box = $('#mapa');
  if (box) {
    var out = $('#chk-out'), inp = $('#miasto');
    var mapa = null, linia = null, cel = null, dom = null;
    var start = function () {
      if (!window.L || mapa) return;
      var mob = matchMedia('(max-width: 900px)').matches;
      mapa = L.map(box, { scrollWheelZoom: false, dragging: !mob, tap: false, zoomControl: !mob }).setView([HOME.lat, HOME.lon], mob ? 9 : 10);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, className: 'kafle', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(mapa);
      L.circle([HOME.lat, HOME.lon], { radius: ZASIEG * 1000, color: '#1c3fd1', weight: 2.5, fillColor: '#1c3fd1', fillOpacity: .09 }).addTo(mapa);
      dom = L.marker([HOME.lat, HOME.lon], { icon: L.divIcon({ className: 'pin', iconSize: [20, 20] }), keyboard: false, zIndexOffset: 1000 })
        .bindTooltip('Serwis · Kutno', { permanent: true, direction: 'top', offset: [0, -12], className: 'km' }).addTo(mapa);
    };
    var zaznacz = function (m, d) {
      if (!mapa) return;
      if (linia) { mapa.removeLayer(linia); linia = null; }
      if (cel) { mapa.removeLayer(cel); cel = null; }
      if (!m) { dom.openTooltip(); return; }
      dom.closeTooltip();
      linia = L.polyline([[HOME.lat, HOME.lon], [m.lat, m.lon]], { color: '#ff6a2b', weight: 3, dashArray: '8 7' }).addTo(mapa);
      cel = L.circleMarker([m.lat, m.lon], { radius: 9, color: '#fff', weight: 3, fillColor: '#ff6a2b', fillOpacity: 1 }).addTo(mapa);
      cel.bindTooltip((m.n !== 'Twoja lokalizacja' ? m.n + ' · ' : '') + Math.round(d) + ' km', { permanent: true, direction: 'top', offset: [0, -10], className: 'km' }).openTooltip();
      mapa.flyToBounds(L.latLngBounds([[HOME.lat, HOME.lon], [m.lat, m.lon]]).pad(.5), { maxZoom: 11, duration: .6 });
    };
    var sprawdz = function (m, nazwa, d) {
      if (d == null) d = m.km;
      var w = werdykt(d);
      zaznacz(m, d);
      out.innerHTML = w === 'ok'
        ? '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu. <span class="ok">W zasięgu odbioru</span>'
        : w === 'granica'
          ? '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu, tuż za granicą 30 km. Zadzwoń pod <a class="u" href="tel:' + TEL + '">889 503 420</a>, ustalimy.'
          : '<b>' + nazwa + '</b><br>' + fmt(d) + ' od serwisu, poza strefą odbioru. Sprzęt możesz przywieźć na ul. Ściegiennego 25 w Kutnie.';
    };
    inp.addEventListener('input', function () {
      var m = znajdz(inp.value);
      if (m) sprawdz(m, m.n); else { out.textContent = ''; zaznacz(null); }
    });
    $('#geo').addEventListener('click', function () {
      if (!navigator.geolocation) { out.textContent = 'Twoja przeglądarka nie udostępnia lokalizacji.'; return; }
      out.textContent = 'Sprawdzam lokalizację…';
      navigator.geolocation.getCurrentPosition(function (pos) {
        var me = { n: 'Twoja lokalizacja', lat: pos.coords.latitude, lon: pos.coords.longitude };
        sprawdz(me, 'Twoja lokalizacja', km(HOME, me));
      }, function () { out.textContent = 'Nie udało się pobrać lokalizacji. Wpisz miejscowość.'; }, { timeout: 8000 });
    });
    var go = function () { if (window.L) start(); else window.addEventListener('load', start); };
    if (miejscaGotowe) miejscaGotowe.then(go); else go();
  }
})();
