(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');

  function onScroll() { header && header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

/* ==== home extras: question demo ==== */
(function () {
  var demo = document.querySelector('.demo');
  if (!demo) return;
  var qt = demo.querySelector('.demo-qt'), chips = demo.querySelectorAll('.chip'),
      res = demo.querySelector('.demo-res'), type = demo.querySelector('.demo-type'), find = demo.querySelector('.demo-find');
  var EX = [
    ['Which plasma proteins change after treatment?', 'Discovery proteomics', '38 proteins changed · 4 pathways enriched'],
    ['Is this compound rewiring kinase signalling in our cells?', 'Phosphoproteomics', '112 phosphosites regulated · 3 kinases implicated'],
    ['Which metabolites separate responders from non-responders?', 'Untargeted metabolomics', '17 discriminating metabolites · clear group separation']
  ];
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function done() { chips.forEach(function (c) { c.className = 'chip done'; }); res.classList.add('show'); }
  if (reduce) { done(); return; }
  var visible = false, running = false, n = 0;
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  async function cycle() {
    running = true;
    while (visible) {
      var ex = EX[n++ % EX.length];
      chips.forEach(function (c) { c.className = 'chip'; });
      res.classList.remove('show');
      qt.textContent = '';
      await wait(500);
      for (var i = 1; i <= ex[0].length; i++) { qt.textContent = ex[0].slice(0, i); await wait(32); }
      type.textContent = ex[1]; find.textContent = ex[2];
      await wait(600);
      for (var k = 0; k < chips.length; k++) {
        chips[k].className = 'chip on'; await wait(k === 3 || k === 4 ? 1100 : 750);
        chips[k].className = 'chip done';
      }
      res.classList.add('show');
      await wait(4800);
    }
    running = false;
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible && !running) cycle();
    }, { threshold: 0.35 }).observe(demo);
  } else { done(); }
})();
/* ==== end home extras ==== */
