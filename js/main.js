/* TSP Statyba — vanilla. PHYSICAL motion personality. No JS => everything visible. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  // The hidden state only exists once JS has confirmed it can undo it.
  if (canObserve && !reduce) root.classList.add('js');

  /* ---------- hero settle ---------- */
  var hero = document.getElementById('hero');
  if (hero) requestAnimationFrame(function () {
    requestAnimationFrame(function () { hero.classList.add('is-in'); });
  });

  /* ---------- reveal (text/UI) + settle (photos: transform only, never hidden) ---------- */
  var items = [].slice.call(document.querySelectorAll('[data-reveal],[data-line],[data-settle]'));
  function show(el) {
    var d = parseInt(el.getAttribute('data-delay') || '0', 10);
    if (d) el.style.transitionDelay = d + 'ms';
    el.classList.add('is-in');
  }
  function showAll() { items.forEach(show); }

  if (!canObserve || reduce) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });

    // Safety net: reveal whatever is already on screen (no blanket show-all).
    var sweep = function () {
      items.forEach(function (el) {
        if (el.classList.contains('is-in')) return;
        var r = el.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0) show(el);
      });
    };
    window.addEventListener('load', sweep);
    document.addEventListener('visibilitychange', sweep);
    window.addEventListener('pageshow', sweep);
  }

  /* ---------- nav state + active link ---------- */
  var nav = document.getElementById('nav');
  var links = [].slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));
  var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 8);
      var mid = window.scrollY + innerHeight * 0.34, best = -1;
      targets.forEach(function (t, i) {
        if (t && t.offsetTop <= mid) best = i;
      });
      links.forEach(function (a, i) { a.classList.toggle('is-active', i === best); });
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- services: hovering a panel opens it ---------- */
  var panels = [].slice.call(document.querySelectorAll('[data-panel]'));
  panels.forEach(function (p, i) {
    p.setAttribute('tabindex', '0');
    function open() {
      panels.forEach(function (q, k) { q.classList.toggle('is-open', k === i); });
    }
    p.addEventListener('mouseenter', open);
    p.addEventListener('focus', open);
    p.addEventListener('click', open);
  });

  /* ---------- mobile call bar hides over the contact section ---------- */
  var bar = document.getElementById('callbar');
  var contact = document.getElementById('kontaktai');
  if (bar && contact && canObserve) {
    new IntersectionObserver(function (es) {
      bar.classList.toggle('is-hidden', es[0].isIntersecting);
    }, { threshold: 0.06 }).observe(contact);
  }

  /* ---------- form ---------- */
  var form = document.getElementById('form');
  if (form && window.fetch) {
    var msg = document.getElementById('formMsg');
    var btn = document.getElementById('submit');
    var label = btn.textContent;
    form.addEventListener('submit', function (ev) {
      var need = [form.querySelector('#tipas'), form.querySelector('#objektas'), form.querySelector('#kontaktas')];
      var bad = need.filter(function (f) { return !f.value.trim(); });
      if (bad.length) {
        ev.preventDefault();
        msg.setAttribute('data-state', 'err');
        msg.textContent = 'Užpildykite darbo tipą, objekto aprašymą ir kontaktą.';
        bad[0].focus();
        return;
      }
      ev.preventDefault();
      btn.disabled = true; btn.textContent = 'Siunčiama…';
      msg.removeAttribute('data-state'); msg.textContent = '';
      fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
        method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' }
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      }).then(function () {
        form.reset();
        msg.setAttribute('data-state', 'ok');
        msg.textContent = 'Užklausa išsiųsta. Susisieksime artimiausiu metu.';
      }).catch(function () {
        msg.setAttribute('data-state', 'err');
        msg.textContent = 'Nepavyko išsiųsti — paskambinkite +370 639 94290 arba parašykite el. paštu.';
      }).then(function () {
        btn.disabled = false; btn.textContent = label;
      });
    });
  }
})();
