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

// "Ask Finvry AI": answers questions about Finvry only. Anyone who wants a person is pointed to support@finvry.com.
(function () {
  var API = 'https://app.finvry.com/api/public/ask', SUPPORT = 'support@finvry.com', KEY = 'fv_ask';
  var HUMAN = /\b(human|agent|person|people|someone|somebody|representative|rep|sales|talk to|speak (to|with)|call me|phone|live chat|customer service|contact (you|support|someone))\b/i;
  var HUMAN_REPLY = 'To talk to someone on the Finvry team, email ' + SUPPORT + ' and we will get back to you.';
  var CHIPS = ['How much does Finvry cost?', 'Is there a free trial?', 'Which tools does it connect to?', 'Talk to a person'];
  var msgs = [];
  try { msgs = JSON.parse(sessionStorage.getItem(KEY) || '[]') || []; } catch (e) { msgs = []; }
  var save = function () { try { sessionStorage.setItem(KEY, JSON.stringify(msgs.slice(-12))); } catch (e) {} };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmt = function (s) {
    return esc(s)
      .replace(/support@finvry\.com/g, '<a href="mailto:support@finvry.com">support@finvry.com</a>')
      .replace(/(^|[\s(])((?:https?:\/\/)?(?:www\.|app\.)?finvry\.com(?:\/[\w\-./#?=&]*)?)/g, function (m, pre, u) {
        var trail = /[.,)]$/.test(u) ? u.slice(-1) : ''; if (trail) u = u.slice(0, -1);
        return pre + '<a href="' + (/^https?:/.test(u) ? u : 'https://' + u) + '">' + u + '</a>' + trail;
      })
      .replace(/\n/g, '<br>');
  };
  var ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8zM18.5 14.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z" fill="currentColor"/></svg>';

  function build() {
    var root = document.createElement('div');
    root.className = 'f-ask';
    root.innerHTML =
      '<button type="button" class="f-askb" aria-expanded="false" aria-controls="f-askp">' + ICON + '<span>Ask Finvry AI</span></button>' +
      '<section class="f-askp" id="f-askp" role="dialog" aria-label="Ask Finvry AI" hidden>' +
        '<header><span class="ic">' + ICON + '</span><span class="tt"><b>Finvry AI</b><em>Answers questions about Finvry</em></span><button type="button" class="x" aria-label="Close">×</button></header>' +
        '<div class="log" aria-live="polite"></div>' +
        '<div class="chips"></div>' +
        '<form><label class="sr" for="f-askq">Your question</label><textarea id="f-askq" rows="1" maxlength="1000" placeholder="Ask about plans, pricing, features…"></textarea><button type="submit" aria-label="Send"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button></form>' +
        '<p class="ft">AI answers can be wrong. To reach a person, email <a href="mailto:' + SUPPORT + '">' + SUPPORT + '</a></p>' +
      '</section>';
    document.body.appendChild(root);
    return root;
  }

  function init() {
    var root = build(), btn = root.querySelector('.f-askb'), panel = root.querySelector('.f-askp'), log = root.querySelector('.log'),
      chips = root.querySelector('.chips'), form = root.querySelector('form'), q = root.querySelector('textarea'), busy = false;

    var bubble = function (role, html) { var d = document.createElement('div'); d.className = 'm ' + role; d.innerHTML = html; log.appendChild(d); log.scrollTop = log.scrollHeight; return d; };
    var render = function () {
      log.innerHTML = '';
      bubble('ai', 'Hi, I\'m Finvry AI. Ask me anything about Finvry: what it does, plans and pricing, the free trial, integrations or company services.');
      msgs.forEach(function (m) { bubble(m.role === 'user' ? 'me' : 'ai', m.role === 'user' ? esc(m.text) : fmt(m.text)); });
      chips.hidden = msgs.length > 0;
    };
    chips.innerHTML = CHIPS.map(function (c) { return '<button type="button">' + c + '</button>'; }).join('');
    var open = function (on) {
      panel.hidden = !on; btn.setAttribute('aria-expanded', on ? 'true' : 'false'); root.classList.toggle('on', on);
      if (on) { render(); setTimeout(function () { q.focus(); }, 30); }
    };
    btn.addEventListener('click', function () { open(panel.hidden); });
    root.querySelector('.x').addEventListener('click', function () { open(false); btn.focus(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { open(false); btn.focus(); } });

    var ask = function (text) {
      text = String(text || '').trim(); if (!text || busy) return;
      chips.hidden = true;
      msgs.push({ role: 'user', text: text.slice(0, 1000) }); save(); bubble('me', esc(text));
      if (HUMAN.test(text)) { msgs.push({ role: 'assistant', text: HUMAN_REPLY }); save(); bubble('ai', fmt(HUMAN_REPLY)); return; }
      busy = true; form.classList.add('busy');
      var wait = bubble('ai wait', '<i></i><i></i><i></i>');
      fetch(API, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ messages: msgs.slice(-8) }) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }, function () { return { ok: false, j: null }; }); })
        .then(function (x) {
          var t = x.ok && x.j && x.j.answer ? x.j.answer : (x.j && x.j.data && x.j.data.error && x.j.data.error.message) || ('Finvry AI could not answer just now. Try again, or email ' + SUPPORT + '.');
          wait.remove();
          if (x.ok) { msgs.push({ role: 'assistant', text: t }); save(); }
          bubble('ai', fmt(t));
        })
        .catch(function () { wait.remove(); bubble('ai', fmt('Finvry AI could not be reached. Try again, or email ' + SUPPORT + '.')); })
        .then(function () { busy = false; form.classList.remove('busy'); q.focus(); });
    };
    chips.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) ask(b.textContent); });
    form.addEventListener('submit', function (e) { e.preventDefault(); var t = q.value; q.value = ''; q.style.height = ''; ask(t); });
    q.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); } });
    q.addEventListener('input', function () { q.style.height = ''; q.style.height = Math.min(q.scrollHeight, 120) + 'px'; });
  }
  document.readyState !== 'loading' ? init() : document.addEventListener('DOMContentLoaded', init);
})();
