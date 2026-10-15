(function () {
  var header = document.querySelector('.site-header');
  var body = document.body;

  // header state on scroll
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 10);
    var top = document.querySelector('.to-top');
    if (top) top.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // mega menu: open on hover / keyboard focus over the GNB
  var gnb = document.querySelector('.gnb');
  var mega = document.querySelector('.mega');
  var closeTimer;
  function openMega() { clearTimeout(closeTimer); header.classList.add('mega-open'); }
  function closeMega() { closeTimer = setTimeout(function () { header.classList.remove('mega-open'); }, 120); }
  if (gnb && mega) {
    [gnb, mega].forEach(function (el) {
      el.addEventListener('mouseenter', openMega);
      el.addEventListener('mouseleave', closeMega);
      el.addEventListener('focusin', openMega);
      el.addEventListener('focusout', function (e) {
        if (!header.contains(e.relatedTarget)) closeMega();
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') header.classList.remove('mega-open');
    });
  }

  // mobile drawer
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = body.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? (menuBtn.dataset.labelClose || '메뉴 닫기') : (menuBtn.dataset.labelOpen || '메뉴 열기'));
    });
    document.querySelectorAll('.drawer a').forEach(function (a) {
      a.addEventListener('click', function () { body.classList.remove('nav-open'); });
    });
  }

  // location bar dropdowns
  document.querySelectorAll('.loc-drop').forEach(function (d) {
    var b = d.querySelector('button');
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = !d.classList.contains('open');
      document.querySelectorAll('.loc-drop.open').forEach(function (o) { o.classList.remove('open'); o.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if (willOpen) { d.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.loc-drop.open').forEach(function (o) { o.classList.remove('open'); o.querySelector('button').setAttribute('aria-expanded', 'false'); });
  });

  // in-page tabs: highlight the section in view
  var tabs = document.querySelectorAll('.tabs a[href^="#"]');
  if (tabs.length && 'IntersectionObserver' in window) {
    var map = {};
    tabs.forEach(function (t) { var s = document.querySelector(t.getAttribute('href')); if (s) map[s.id] = t; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tabs.forEach(function (t) { t.classList.remove('on'); });
          map[en.target.id].classList.add('on');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  // back to top
  var top = document.querySelector('.to-top');
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  // records filter
  var table = document.querySelector('.rec-table');
  if (table) {
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var chips = document.querySelectorAll('.chips button');
    var yearSel = document.getElementById('f-year');
    var q = document.getElementById('f-q');
    var count = document.getElementById('f-count');
    var empty = document.querySelector('.empty');
    var cat = 'all';
    var params = new URLSearchParams(location.search);
    if (params.get('cat')) cat = params.get('cat');

    function apply() {
      var y = yearSel.value, term = q.value.trim().toLowerCase(), n = 0;
      rows.forEach(function (r) {
        var ok = (cat === 'all' || r.dataset.cat === cat) &&
                 (y === 'all' || r.dataset.year === y) &&
                 (!term || r.textContent.toLowerCase().indexOf(term) > -1);
        r.hidden = !ok; if (ok) n++;
      });
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.cat === cat ? 'true' : 'false'); });
      count.textContent = n;
      empty.hidden = n > 0;
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { cat = c.dataset.cat; apply(); }); });
    yearSel.addEventListener('change', apply);
    q.addEventListener('input', apply);
    apply();
  }
})();
