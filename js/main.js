/* TSP Statyba. Vanilla. No JS means everything is visible. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;

  /* The hidden state only exists once JS has confirmed it can undo it. */
  if (canObserve && !reduce) root.classList.add('js');

  /* ---------- reveal ---------- */
  var items = [].slice.call(document.querySelectorAll('[data-reveal]'));
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
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });

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
    setTimeout(showAll, 2500);
  }

  /* ---------- sklandus slinkimas (Lenis) ---------- */
  /* iframe'e nepaleidžiam: qa harnesui reikia tikro programinio scrollTo */
  var inFrame = window.self !== window.top;
  var lenis = null;
  if (window.Lenis && !reduce && !inFrame) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true, syncTouch: false, autoRaf: false });
    var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      var t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      lenis.scrollTo(t, { offset: -78 });
    });
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
      targets.forEach(function (t, i) { if (t && t.offsetTop <= mid) best = i; });
      links.forEach(function (a, i) { a.classList.toggle('is-active', i === best); });
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = document.getElementById('burger');
  var panel = document.getElementById('navlinks');
  if (burger && panel) {
    var setOpen = function (open) {
      panel.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Uždaryti meniu' : 'Atidaryti meniu');
    };
    burger.addEventListener('click', function () {
      setOpen(burger.getAttribute('aria-expanded') !== 'true');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* ---------- mobile call bar hides over the contact section ---------- */
  var bar = document.getElementById('callbar');
  var contact = document.getElementById('kontaktai');
  if (bar && contact && canObserve) {
    new IntersectionObserver(function (es) {
      bar.classList.toggle('is-hidden', es[0].isIntersecting);
    }, { threshold: 0.06 }).observe(contact);
  }

  /* ---------- naujienų vaizdo įrašai: groja, kai matomi ---------- */
  var vids = [].slice.call(document.querySelectorAll('[data-video]'));
  vids.forEach(function (box) {
    var v = box.querySelector('video');
    if (!v) return;
    if (reduce) { box.classList.add('is-paused'); return; }
    var play = function () {
      var pr = v.play();
      if (pr && pr.catch) pr.catch(function () { box.classList.add('is-paused'); });
    };
    if (canObserve) {
      new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { v.preload = 'auto'; play(); }
        else { v.pause(); }
      }, { threshold: 0.25 }).observe(box);
    } else {
      v.preload = 'auto'; play();
    }
    v.addEventListener('playing', function () { box.classList.remove('is-paused'); });
    v.addEventListener('pause', function () {
      if (!document.hidden) box.classList.add('is-paused');
    });
  });

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
        msg.textContent = 'Nepavyko išsiųsti. Paskambinkite +370 639 94290 arba parašykite el. paštu.';
      }).then(function () {
        btn.disabled = false; btn.textContent = label;
      });
    });
  }
})();
