// Shared behaviour for finvry.com: mobile menu, hero AI demo, "See it work" tabs, API code tabs, year.
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ready(fn) { document.readyState !== 'loading' ? fn() : document.addEventListener('DOMContentLoaded', fn); }

  ready(function () {
    $$('.yr').forEach(function (e) { e.textContent = new Date().getFullYear(); });

    // Mobile menu
    var mb = $('.f-mb'), mm = $('#f-mm');
    if (mb && mm) mb.addEventListener('click', function () {
      var open = mm.hasAttribute('hidden');
      open ? mm.removeAttribute('hidden') : mm.setAttribute('hidden', '');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // Product menu: hover on desktop, tap to open on touch screens
    $$('.f-dd').forEach(function (d) {
      var b = $('.f-ddb', d);
      var set = function (o) { d.classList.toggle('open', o); b.setAttribute('aria-expanded', o ? 'true' : 'false'); };
      b.addEventListener('click', function (e) { e.stopPropagation(); set(!d.classList.contains('open')); });
      document.addEventListener('click', function (e) { if (!d.contains(e.target)) set(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { set(false); b.blur(); } });
    });

    // Header shadow on scroll
    var hd = $('.f-hd');
    if (hd) { var on = function () { hd.classList.toggle('sc', scrollY > 8); }; on(); addEventListener('scroll', on, { passive: true }); }

    // Hero AI demo (sample company)
    var ai = $('[data-ai]');
    if (ai) {
      var ASK = [
        { ask: 'How long is our runway?', src: 'QuickBooks · last 6 months', answer: 'At your average burn, cash lasts about 21 months.', kpis: [['Cash', '$1.4M'], ['Burn / mo', '$66k'], ['Runway', '21 months']] },
        { ask: 'Draft the September update.', src: 'Books · last update', answer: 'Drafted: strong quarter, two key hires, raising next. Ready for your edit.', kpis: [['Q3 revenue', '$84,210'], ['New hires', '2'], ['Recipients', '42']] },
        { ask: 'Where is the seed round?', src: 'Pipeline · SAFEs', answer: '$1.9M committed of $2.5M. Three investors opened the data room this week.', kpis: [['Committed', '$1.9M'], ['Target', '$2.5M'], ['Progress', '76%']] },
        { ask: 'What do we owe this quarter?', src: 'Compliance calendar', answer: 'Delaware franchise tax and the Q4 investor report are next. Reminders are set.', kpis: [['Due soon', '2'], ['Overdue', 'None'], ['Filed', '5']] }
      ];
      var cur = 0, timer, btns = $$('.tabs button', ai), box = $('[data-cur]', ai);
      var show = function (i) {
        var p = ASK[cur]; cur = i; var a = ASK[i];
        $('[data-pq]', ai).textContent = p.ask; $('[data-pa]', ai).textContent = p.answer;
        $('[data-q]', ai).textContent = a.ask; $('[data-src]', ai).textContent = a.src; $('[data-a]', ai).textContent = a.answer;
        $('[data-kp]', ai).innerHTML = a.kpis.map(function (k) { return '<span>' + k[0] + ' <b>' + k[1] + '</b></span>'; }).join('');
        btns.forEach(function (b, j) { b.classList.toggle('on', j === i); });
        if (box) { box.classList.remove('f-fade'); void box.offsetWidth; box.classList.add('f-fade'); }
      };
      var loop = function () { clearInterval(timer); if (!still) timer = setInterval(function () { show((cur + 1) % ASK.length); }, 4200); };
      btns.forEach(function (b, j) { b.addEventListener('click', function () { if (j !== cur) show(j); loop(); }); });
      loop();
    }

    // "See it work": one video at a time
    $$('[data-show]').forEach(function (wrap) {
      var sec = wrap.closest('section'), vid = $('[data-sv]', sec), tabs = $$('.f-tab', wrap);
      tabs.forEach(function (t) {
        $('button', t).addEventListener('click', function () {
          if (t.classList.contains('on')) return;
          tabs.forEach(function (x) { x.classList.remove('on'); $('button', x).setAttribute('aria-expanded', 'false'); });
          t.classList.add('on'); $('button', t).setAttribute('aria-expanded', 'true');
          $('[data-sk]', sec).textContent = t.dataset.k; $('[data-sl]', sec).textContent = t.dataset.l; $('[data-sc]', sec).textContent = t.dataset.v;
          if (vid) { vid.innerHTML = '<source src="' + t.dataset.video + '" type="video/mp4">'; vid.load(); var pr = vid.play(); if (pr && pr.catch) pr.catch(function () {}); }
        });
      });
    });

    // API code sample
    var code = $('[data-code]');
    if (code) {
      var K = 'Authorization: Bearer $FINVRY_KEY';
      var S = [
        'curl https://app.finvry.com/api/v1/metrics \\\n  -H "' + K + '"',
        "const res = await fetch('https://app.finvry.com/api/v1/metrics', {\n  headers: { Authorization: `Bearer ${process.env.FINVRY_KEY}` }\n});\nconst { runway_months, burn, cash } = await res.json();",
        "import os, requests\n\nr = requests.get('https://app.finvry.com/api/v1/metrics',\n    headers={'Authorization': f\"Bearer {os.environ['FINVRY_KEY']}\"})\nprint(r.json()['runway_months'])"
      ];
      var pre = $('[data-pre]', code), cb = $$('.bar button', code);
      var set = function (i) { pre.textContent = S[i]; cb.forEach(function (b, j) { b.classList.toggle('on', j === i); }); };
      cb.forEach(function (b, j) { b.addEventListener('click', function () { set(j); }); });
      set(0);
    }

    // Only play videos while they are on screen
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var v = e.target;
          if (e.isIntersecting) { if (v.preload === 'none') v.preload = 'auto'; if (!still) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
          else v.pause();
        });
      }, { rootMargin: '200px' });
      $$('video.f-vid').forEach(function (v) { io.observe(v); });
    }
  });
})();
