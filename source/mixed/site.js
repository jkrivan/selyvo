/* selyvo.com — the mixed design (sections in turn dark and light): the bar following the section under it, things that come in as you reach them, screens that rise into place, the market's
   processes played as you scroll, the Good to know cards, the tour's chapters, the menu and the contact form. No libraries. */
(function () {
  'use strict';
  var root = document.documentElement, lm = document.querySelector('meta[name="selyvo-lang"]');
  if (lm && !root.lang) root.lang = lm.content;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };

  // light or dark: the system decides until the visitor chooses; the choice is remembered
  var sysDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function dark() { var t = root.getAttribute('data-theme'); return t ? t === 'dark' : !!(sysDark && sysDark.matches); }
  function label() { $$('[data-theme-toggle]').forEach(function (b) { b.setAttribute('aria-label', b.getAttribute(dark() ? 'data-l-light' : 'data-l-dark')); }); }
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var next = dark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('selyvo-theme', next); } catch (x) {}
      label();
    });
  });
  if (sysDark && sysDark.addEventListener) sysDark.addEventListener('change', label);
  label();

  // the phone menu: closes on a link, on Escape
  $$('details.mm').forEach(function (d) {
    d.addEventListener('toggle', function () {
      document.documentElement.style.overflow = d.open ? 'hidden' : '';
      var bar = d.closest('.gn');      // the bar without its glass while the menu is open (site.css: .gn--open), light under the light menu
      if (bar) { bar.classList.toggle('gn--open', d.open); if (d.open) bar.classList.remove('gn--dark'); else bars(); }
      if (d.open) $$('details.lsel[open]').forEach(function (x) { x.open = false; });
    });
    d.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a[href]')) d.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.open) { d.open = false; d.querySelector('summary').focus(); } });
  });

  // the language: the 15 languages under the bar, each the same page in that language; closes on a click outside it and on Escape
  $$('details.lsel').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) $$('details.mm[open]').forEach(function (x) { x.open = false; }); });
    document.addEventListener('click', function (e) { if (d.open && !d.contains(e.target)) d.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.open) { d.open = false; d.querySelector('summary').focus(); } });
  });

  // things come in as you reach them; numbers count up; the trust steps light up one after another
  function countUp(el) {
    var to = +el.getAttribute('data-count'), t0 = null;
    if (reduce || !to) return;
    el.textContent = '0';
    function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / 1100); el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  var seen = function (el) { el.classList.add('in'); $$('[data-count]', el).forEach(countUp); if (el.hasAttribute('data-count')) countUp(el); };
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { seen(en.target); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    $$('[data-rv], .vsteps').forEach(function (el) { io.observe(el); });
  } else { $$('[data-rv], .vsteps').forEach(function (el) { el.classList.add('in'); }); }

  // screens that rise into place: flat once their top passes the lower part of the screen
  var risers = reduce ? [] : $$('[data-rise]');

  // a jump the visitor should not see as a scroll
  function jumpTo(y) { var b = root.style.scrollBehavior; root.style.scrollBehavior = 'auto'; window.scrollTo(0, y); root.style.scrollBehavior = b; }
  // a page opened from the menu starts at its top (its links carry #top)
  if (location.hash === '#top') { jumpTo(0); window.addEventListener('pageshow', function () { if (location.hash === '#top' && window.scrollY < 2 * window.innerHeight) jumpTo(0); }); }

  // the stories: the process played as you scroll — the first time through, to its end: the last step held like the others, then the
  // page goes on to what follows. Once every step has been seen (the first and the last with the visitor in it, so all those between),
  // the story is set still for the rest of the visit — but only when it is out of sight and the scrolling has stopped, so that nothing
  // in view moves: then no more scrolling through it, a step chosen shows it again
  var stories = $$('[data-story]').map(function (s, i) {
    var data = JSON.parse(s.getAttribute('data-story'));
    return { el: s, data: data, n: data.length, k: -1, lis: $$('.sstp li', s), scs: $$('.sc', s), sss: $$('.ss', s),
             fill: s.querySelector('.sstp'), url: s.querySelector('.story__frame .dframe__url'), stage: s.querySelector('.story__stage'),
             key: 'selyvo-seen:' + location.pathname + ':' + i, lo: Infinity, hi: -1, seen: false };
  });
  function pinned(st) { return getComputedStyle(st.stage).position === 'sticky'; }
  function show(st, k) {
    if (st.k === k) return; st.k = k;
    var d = st.data[k];
    st.lis.forEach(function (li, i) { li.classList.toggle('done', st.seen ? i !== k : i < k); li.classList.toggle('now', i === k); });
    st.scs.forEach(function (sc, i) { sc.classList.toggle('on', i === k); });
    st.sss.forEach(function (ss, i) {
      var on = i === d.s; ss.classList.toggle('on', on);
      var hls = ss.querySelectorAll('.hl');
      Array.prototype.forEach.call(hls, function (h, j) {
        var b = on ? d.b[j] : null;
        if (b) { h.style.left = b[0] + '%'; h.style.top = b[1] + '%'; h.style.width = b[2] + '%'; h.style.height = b[3] + '%'; }
        h.classList.remove('on');
        if (b) { void h.offsetWidth; h.classList.add('on'); }
      });
    });
    if (st.url) st.url.textContent = d.u;
  }
  function markSeen(st) {                              // seen and out of sight: a still section of the stage's height
    if (st.seen) return;
    var b0 = st.el.getBoundingClientRect().bottom;      // what follows the story is where the visitor's eyes are: it must not move
    st.seen = true; st.el.classList.add('story--seen');
    var intro = st.el.previousElementSibling, h = intro && intro.querySelector('.hint [data-seen]');
    if (intro && intro.classList.contains('story-intro')) intro.classList.add('story-intro--seen');
    if (h) h.textContent = h.getAttribute('data-seen');
    st.fill.style.setProperty('--p', '1');
    var k = st.k; st.k = -1; show(st, k < 0 ? st.n - 1 : k);
    if (b0 <= 0) jumpTo(window.scrollY + st.el.getBoundingClientRect().bottom - b0);     // it was above the screen: the page stays exactly where the visitor is
  }
  function settle() {
    stories.forEach(function (st) {
      if (!st.done || st.seen) return;
      var r = st.el.getBoundingClientRect();
      if (r.bottom <= 0 || r.top >= window.innerHeight) markSeen(st);
    });
  }
  var idle = 0;                                          // the scrolling has stopped (a flick's glide included)
  window.addEventListener('scroll', function () { clearTimeout(idle); idle = setTimeout(settle, 450); }, { passive: true });
  stories.forEach(function (st) {
    show(st, 0);
    try { st.done = sessionStorage.getItem(st.key) === '1'; } catch (x) {}
    st.lis.forEach(function (li, i) {
      var b = li.querySelector('button'); if (!b) return;
      b.addEventListener('click', function () {         // a step chosen: the page scrolls to where that step is played; once seen, it shows it
        if (st.seen) { show(st, i); return; }
        if (!pinned(st)) return;
        var r = st.el.getBoundingClientRect(), total = st.el.offsetHeight - st.stage.offsetHeight;
        var y = window.scrollY + r.top + total * (i + 0.5) / st.n;
        window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  });

  // the page bar: its first link right under the main bar's first one (Overview under Sell); where the main bar has no links, at the right
  var gl = document.querySelector('.gn__links'), lnav = document.querySelector('.ln__links');
  function alignLn() {
    if (!gl || !lnav) return;
    lnav.style.marginLeft = '';
    var a = gl.querySelector('a');
    if (!a || getComputedStyle(gl).display === 'none' || getComputedStyle(lnav).display === 'none') return;
    lnav.style.marginLeft = '0px';
    lnav.style.marginLeft = Math.max(0, Math.round(a.getBoundingClientRect().left - lnav.getBoundingClientRect().left)) + 'px';
  }
  alignLn(); window.addEventListener('resize', alignLn); window.addEventListener('load', alignLn);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(alignLn);

  // the main bar stays on one line beside the logo (some languages' words are long). On a tablet or a phone (the menu shown, holding
  // the links, Get invited and the languages as well) the first to leave the bar is the language, then Get invited — and the language
  // comes back where Get invited has gone and it fits. On a desktop the language stays: first the bar draws closer together (snug),
  // then Get invited goes, and where the links still do not fit, they go into the menu as on a tablet.
  var gin = document.querySelector('.gn__in'), gtools = document.querySelector('.gn__tools'), gmm = document.querySelector('details.mm');
  var FIT = ['nolang', 'tight', 'menu', 'snug'];
  function fitBar() {
    if (!gin || !gtools) return;
    var set = function (t) { FIT.forEach(function (c) { gin.classList.toggle('gn__in--' + c, t.indexOf(c) >= 0); }); };
    set([]);
    var phone = !!gmm && getComputedStyle(gmm).display !== 'none';
    var tries = phone ? [[], ['nolang'], ['tight'], ['nolang', 'tight']]
                      : [[], ['snug'], ['snug', 'tight'], ['menu'], ['menu', 'nolang'], ['menu', 'tight'], ['menu', 'nolang', 'tight']];
    for (var i = 0; i < tries.length; i++) {
      set(tries[i]);
      var lim = gin.getBoundingClientRect().right - parseFloat(getComputedStyle(gin).paddingRight);
      if (gtools.getBoundingClientRect().right <= lim + 1) break;
    }
    alignLn();      // the main bar's links may have moved: the page bar follows them
  }
  fitBar(); window.addEventListener('resize', fitBar); window.addEventListener('load', fitBar);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitBar);

  // the bar follows the section under it
  var gn = document.querySelector('.gn'), ln = document.querySelector('.ln');
  function toneAt(y) { var el = document.elementFromPoint(Math.round(window.innerWidth / 2), Math.min(window.innerHeight - 1, y)); var s = el && el.closest('[data-tone]'); return s ? s.getAttribute('data-tone') : 'light'; }
  function bars() {
    if (!gn || (document.querySelector('details.mm[open]'))) return;
    var y = (ln || gn).getBoundingClientRect().bottom + 2, dk = toneAt(y) === 'dark';
    gn.classList.toggle('gn--dark', dk); if (ln) ln.classList.toggle('ln--dark', dk); document.body.classList.toggle('bar-light', !dk);
  }
  function frame() {
    var vh = window.innerHeight;
    bars();
    risers.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.85)));
      el.style.setProperty('--rp', (0.15 + p * 0.85).toFixed(3));
    });
    stories.forEach(function (st) {
      if (st.seen || !pinned(st)) return;
      var r = st.el.getBoundingClientRect(), sh = st.stage.offsetHeight, total = st.el.offsetHeight - sh;
      var p = Math.max(0, Math.min(1, -r.top / Math.max(1, total)));
      var k = Math.min(st.n - 1, Math.floor(p * st.n));
      var f = Math.max(0, Math.min(1, (p * st.n - 0.5) / Math.max(1, st.n - 1)));     // the line fills from the first step's middle to the last's
      st.fill.style.setProperty('--p', f.toFixed(4));
      show(st, k);
      var T = parseFloat(getComputedStyle(st.stage).top) || 0;
      if (r.top <= T + 1 && r.bottom >= T + sh - 1) {                                  // the visitor is in it: the steps seen so far
        st.lo = Math.min(st.lo, k); st.hi = Math.max(st.hi, k);
        if (st.lo === 0 && st.hi === st.n - 1 && !st.done) { st.done = true; try { sessionStorage.setItem(st.key, '1'); } catch (x) {} }
      }
    });
  }
  var ticking = false;
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; frame(); }); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  frame();
  var navType = ((performance.getEntriesByType && performance.getEntriesByType('navigation')[0]) || {}).type;
  if (navType === 'reload' || navType === 'back_forward') window.addEventListener('load', function () { setTimeout(settle, 300); }); else settle();

  // Good to know: the arrows move the cards
  $$('[data-gal]').forEach(function (b) {
    b.addEventListener('click', function () {
      var sec = b.closest('section'), g = sec && sec.querySelector('.gal'); if (!g) return;
      var card = g.querySelector('.gcard'), w = card ? card.getBoundingClientRect().width + 18 : 300;
      g.scrollBy({ left: +b.getAttribute('data-gal') * w, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  // the tour: one video at a time; a chapter chosen plays from its start; the chapter playing is marked
  var vids = $$('video');
  vids.forEach(function (v) { v.addEventListener('play', function () { vids.forEach(function (o) { if (o !== v && !o.paused) o.pause(); }); }); });
  function seek(v, t) {
    var go = function () { try { v.currentTime = t; } catch (x) {} var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    if (v.readyState >= 1) go(); else { v.preload = 'metadata'; v.addEventListener('loadedmetadata', function once() { v.removeEventListener('loadedmetadata', once); go(); }); v.load(); }
    var r = v.getBoundingClientRect(); if (r.top < 0 || r.bottom > window.innerHeight) v.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
  }
  $$('button[data-player][data-t]').forEach(function (b) {
    b.addEventListener('click', function () { var v = document.getElementById(b.getAttribute('data-player')); if (v) seek(v, +b.getAttribute('data-t')); });
  });
  vids.forEach(function (v) {
    var bs = $$('button[data-player="' + v.id + '"][data-t]');
    if (!bs.length) return;
    v.addEventListener('timeupdate', function () {
      var cur = 0; bs.forEach(function (b) { if (+b.getAttribute('data-t') <= v.currentTime + .25) cur = +b.getAttribute('data-t'); });
      bs.forEach(function (b) { if (+b.getAttribute('data-t') === cur) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); b.classList.remove('here'); });
    });
  });

  // the films: one player for the page; a card chosen plays its film there; the film's timeline fills as it plays, a part of it or a
  // chapter chosen plays from there, the chapter playing is marked; "Watch the video" plays the page's film
  $$('.fplayer').forEach(function (box) {
    var v = box.querySelector('video'), sec = box.closest('section'), films, cur = 0, lastK = -1, raf = 0;
    try { films = JSON.parse(box.getAttribute('data-films')); } catch (x) { return; }
    if (!v || !films || !films.length) return;
    var srcEl = v.querySelector('source'), cards = $$('.fcard', sec), chs = $$('.fchap', box);
    var nl = box.querySelector('.fnow__label'), nt = box.querySelector('.fnow__t'), nx = box.querySelector('.fnow__x');
    function partsOf(i) { return chs[i] ? $$('.ftl button', chs[i]) : []; }
    function chipsOf(i) { return chs[i] ? $$('.dchap button', chs[i]) : []; }
    function paint() {
      var f = films[cur], cs = f.c, started = v.currentTime > 0.05, t = started ? v.currentTime : (f.st || 0), end = v.duration || f.d, k = 0;
      for (var j = 0; j < cs.length; j++) if (cs[j] <= t + 0.25) k = j;
      partsOf(cur).forEach(function (b, j) {
        var a = cs[j], z = j + 1 < cs.length ? cs[j + 1] : end;
        var p = !started ? 0 : t >= z ? 1 : t <= a ? 0 : (t - a) / Math.max(0.1, z - a);
        b.style.setProperty('--f', p.toFixed(4));
      });
      var chips = chipsOf(cur);
      chips.forEach(function (b, j) { if (j === k) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
      if (k !== lastK) {                       // the chapter playing slides into view in its row (the row only, never the page)
        lastK = k;
        var row = chs[cur] && chs[cur].querySelector('.dchap'), c = chips[k];
        if (row && c && started) row.scrollTo({ left: Math.max(0, c.offsetLeft - row.offsetLeft - (row.clientWidth - c.offsetWidth) / 2), behavior: reduce ? 'auto' : 'smooth' });
      }
    }
    function loop() { paint(); if (!v.paused && !v.ended) raf = requestAnimationFrame(loop); }
    v.addEventListener('play', function () { sec.classList.add('playing'); cancelAnimationFrame(raf); loop(); });
    ['pause', 'ended'].forEach(function (ev) { v.addEventListener(ev, function () { sec.classList.remove('playing'); cancelAnimationFrame(raf); paint(); }); });
    ['seeked', 'loadedmetadata', 'timeupdate'].forEach(function (ev) { v.addEventListener(ev, function () { if (v.paused) paint(); }); });
    function playFrom(t) {                     // play() first, inside the click, so that phones let it play with its sound
      var p = v.play(); if (p && p.catch) p.catch(function () {});
      var at = function () { try { if (Math.abs(v.currentTime - t) > 0.3) v.currentTime = t; } catch (x) {} };
      if (v.readyState >= 1) at(); else v.addEventListener('loadedmetadata', function once() { v.removeEventListener('loadedmetadata', once); at(); });
      var r = v.getBoundingClientRect();
      if (r.top < 0 || r.bottom > window.innerHeight) v.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
    }
    function choose(i) {
      if (i === cur) return;
      var f = films[i]; cur = i; lastK = -1;
      v.pause(); v.poster = f.p; v.setAttribute('aria-label', f.t);
      srcEl.setAttribute('src', f.s); v.preload = 'none'; v.load();
      nl.textContent = f.l; nt.textContent = f.t; nx.textContent = f.x;
      var fn = box.querySelector('.fnote'); if (fn) { fn.textContent = f.n || ''; fn.hidden = !f.n; }      // an English film on another language's page says so
      chs.forEach(function (c, j) { c.hidden = j !== i; });
      cards.forEach(function (c, j) { c.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      paint();
    }
    cards.forEach(function (c, i) {
      c.addEventListener('click', function () {
        if (i === cur && !v.paused) { v.pause(); return; }                       // the film playing: its card pauses it
        if (i === cur && v.currentTime > 0.05) { var p = v.play(); if (p && p.catch) p.catch(function () {}); return; }
        choose(i); playFrom(films[i].st || 0);
      });
    });
    chs.forEach(function (ch, i) {
      $$('button[data-t]', ch).forEach(function (b) { b.addEventListener('click', function () { if (i !== cur) choose(i); playFrom(+b.getAttribute('data-t')); }); });
    });
    // a row of chapters wider than the page fades out where more of it is
    var rows = $$('.dchap', box);
    function edges() { rows.forEach(function (r) { r.classList.toggle('fl', r.scrollLeft > 4); r.classList.toggle('fr', r.scrollLeft + r.clientWidth < r.scrollWidth - 4); }); }
    rows.forEach(function (r) { r.addEventListener('scroll', edges, { passive: true }); });
    window.addEventListener('resize', edges); cards.forEach(function (c) { c.addEventListener('click', function () { setTimeout(edges, 0); }); });
    edges();
    $$('a[data-play]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        if (!v.paused) { v.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' }); return; }
        playFrom(v.currentTime > 0.05 ? v.currentTime : (films[cur].st || 0));
      });
    });
    paint();
  });

  // the contact form: the required fields filled, the e-mail an e-mail — then the thank-you page
  var form = document.querySelector('form.dform');
  if (form) {
    var err = form.querySelector('.form__err');
    form.addEventListener('submit', function (e) {
      var bad = [];
      $$('[required]', form).forEach(function (f) {
        var ok = f.value.trim() !== '' && (f.type !== 'email' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim()));
        f.setAttribute('aria-invalid', ok ? 'false' : 'true'); if (!ok) bad.push(f);
      });
      if (bad.length) { e.preventDefault(); if (err) err.hidden = false; bad[0].focus(); return; }
      if (err) err.hidden = true;
      if (document.querySelector('meta[name="selyvo-demo"]')) { e.preventDefault(); window.location.href = form.getAttribute('data-thanks') || 'thank-you.html'; }
    });
  }
})();
