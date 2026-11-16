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

// "Ask Finvry AI": a messenger in the corner of every page (home, conversations, help). Finvry AI answers questions
// about Finvry only; anyone who wants a person is pointed to support@finvry.com. Conversations stay in this browser.
(function () {
  var API = 'https://app.finvry.com/api/public/ask', SUPPORT = 'support@finvry.com', KEY = 'fv_chats', SEEN = 'fv_ask_seen';
  var HUMAN = /\b(human|agent|person|people|someone|somebody|representative|sales|talk to|speak (to|with)|call me|phone|live chat|customer service|contact (you|support|someone|the team))\b/i;
  var HUMAN_REPLY = 'To talk to someone on the Finvry team, email ' + SUPPORT + ' and we will get back to you.';
  var HELLO = 'Hi there. You are speaking with Finvry AI. Ask me anything about Finvry: plans and pricing, the free trial, features, integrations or company services.';
  var HELP = [
    ['Plans and pricing', 'How much does Finvry cost?'], ['Free trial', 'How does the 14-day free trial work?'], ['Paying in naira', 'Can I pay in naira?'],
    ['Integrations', 'Which tools does Finvry connect to?'], ['Getting access', 'Why do I need to request access?'], ['Partner discounts', 'How do partner codes work?'],
    ['Company services', 'What company services do you offer?'], ['Moving from Pulley', 'Can I move my cap table from Pulley?']
  ];
  var LINKS = [['Pricing', '/pricing/'], ['Finvry vs others', '/compare/'], ['Partner discounts', '/partners/'], ['API documentation', 'https://app.finvry.com/developers'], ['System status', 'https://app.finvry.com/status']];
  var I = {
    spark: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8zM18.5 14.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z" fill="currentColor"/></svg>',
    chat: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v12H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 10.5c1.9 1.6 5.1 1.6 7 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    home: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10.5 12 4l8 6.5V20H4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    msgs: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 9h8M8 12h5" stroke="currentColor" stroke-width="1.8"/></svg>',
    help: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1 .8-1 1.5v.4M12 16.8v.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    send: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M12 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    back: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    go: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    mail: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v12H3z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 7 8.5 6.5L20.5 7" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
    x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2"/></svg>',
    down: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg>'
  };
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
  var ago = function (t) {
    var s = Math.max(0, (Date.now() - t) / 1000);
    if (s < 60) return 'Just now'; if (s < 3600) return Math.floor(s / 60) + 'm ago'; if (s < 86400) return Math.floor(s / 3600) + 'h ago';
    return new Date(t).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var chats = store.get(KEY, []);
  if (!Array.isArray(chats)) chats = [];
  var saveChats = function () { chats = chats.filter(function (c) { return c.msgs && c.msgs.length; }).slice(0, 20); store.set(KEY, chats); };

  function init() {
    var root = document.createElement('div');
    root.className = 'fa';
    root.innerHTML =
      '<div class="fa-tease" hidden><button type="button" class="fa-tx" aria-label="Dismiss">' + I.x + '</button><span class="fa-av">' + I.spark + '</span><span class="fa-tb"><b>Hi there 👋</b><span>You are speaking with Finvry AI. How can I help?</span><em>Finvry AI · Just now</em></span></div>' +
      '<section class="fa-p" role="dialog" aria-label="Finvry AI" hidden><div class="fa-v"></div></section>' +
      '<button type="button" class="fa-l" aria-label="Open Finvry AI" aria-expanded="false"><span class="o">' + I.chat + '</span><span class="c">' + I.down + '</span><i class="fa-badge" hidden>1</i></button>';
    document.body.appendChild(root);
    var panel = root.querySelector('.fa-p'), view = root.querySelector('.fa-v'), launcher = root.querySelector('.fa-l'), tease = root.querySelector('.fa-tease'), badge = root.querySelector('.fa-badge');
    var tab = 'home', cur = null, busy = false;

    var open = function (on) {
      panel.hidden = !on; root.classList.toggle('on', on); launcher.setAttribute('aria-expanded', on ? 'true' : 'false');
      launcher.setAttribute('aria-label', on ? 'Close Finvry AI' : 'Open Finvry AI');
      if (on) { tease.hidden = true; badge.hidden = true; store.set(SEEN, 1); cur ? showChat(cur) : showTab(tab); }
      else if (!dismissed()) tease.hidden = false;
    };
    launcher.addEventListener('click', function () { open(panel.hidden); });
    // The greeting sits above the button on every page until the visitor closes it (for this visit) or opens the chat.
    var dismissed = function () { try { return sessionStorage.getItem('fv_tease_off') === '1'; } catch (e) { return false; } };
    tease.addEventListener('click', function (e) {
      if (e.target.closest('.fa-tx')) { tease.hidden = true; badge.hidden = true; store.set(SEEN, 1); try { sessionStorage.setItem('fv_tease_off', '1'); } catch (x) {} return; }
      open(true); newChat();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { open(false); launcher.focus(); } });
    if (!dismissed()) setTimeout(function () { if (panel.hidden) { tease.hidden = false; badge.hidden = !!store.get(SEEN, 0); } }, 1800);

    var nav = function () {
      return '<nav class="fa-nav">' + [['home', 'Home', I.home], ['msgs', 'Messages', I.msgs], ['help', 'Help', I.help]].map(function (t) {
        return '<button type="button" data-tab="' + t[0] + '"' + (tab === t[0] ? ' class="on" aria-current="page"' : '') + '>' + t[2] + '<span>' + t[1] + '</span></button>';
      }).join('') + '</nav>';
    };
    var row = function (c) {
      var last = c.msgs[c.msgs.length - 1];
      return '<button type="button" class="fa-row" data-chat="' + c.id + '"><span class="fa-av sm">' + I.spark + '</span><span class="fa-rt"><b>' + esc(c.title) + '</b><span>' + esc((last.role === 'user' ? 'You: ' : '') + last.text).slice(0, 90) + '</span></span><em>' + ago(c.at) + '</em></button>';
    };
    var bindNav = function () {
      view.querySelectorAll('[data-tab]').forEach(function (b) { b.addEventListener('click', function () { showTab(b.dataset.tab); }); });
      view.querySelectorAll('[data-chat]').forEach(function (b) { b.addEventListener('click', function () { showChat(b.dataset.chat); }); });
      view.querySelectorAll('[data-new]').forEach(function (b) { b.addEventListener('click', function () { newChat(b.dataset.q || ''); }); });
      view.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { open(false); launcher.focus(); }); });
    };

    function showTab(t) {
      tab = t; cur = null;
      var close = '<button type="button" class="fa-x" data-close aria-label="Close">' + I.x + '</button>';
      var html = '', list = chats.filter(function (c) { return c.msgs && c.msgs.length; });
      if (t === 'home') {
        var recent = list[0];
        html = '<div class="fa-home"><div class="fa-hero"><div class="fa-top"><img src="/finvry-logo-light.svg" alt="Finvry">' + close + '</div><h2><span>Hello there.</span>How can we help?</h2></div><div class="fa-body">' +
          '<button type="button" class="fa-card fa-ask" data-new><span><b>Ask a question</b><span>Finvry AI can help, any time</span></span><i>' + I.send + '</i></button>' +
          (recent ? '<div class="fa-card fa-recent"><p class="fa-k">Recent conversation</p>' + row(recent) + '</div>' : '') +
          '<a class="fa-card fa-team" href="mailto:' + SUPPORT + '"><span class="fa-av sm lt">' + I.mail + '</span><span><b>Talk to the team</b><span>Email ' + SUPPORT + '</span></span><i>' + I.go + '</i></a>' +
          '<div class="fa-card fa-links"><p class="fa-k">Popular questions</p>' + HELP.slice(0, 4).map(function (h) { return '<button type="button" class="fa-li" data-new data-q="' + esc(h[1]) + '"><span>' + esc(h[1]) + '</span><i>' + I.go + '</i></button>'; }).join('') + '</div>' +
          '</div></div>';
      } else if (t === 'msgs') {
        html = '<div class="fa-hd"><h3>Messages</h3>' + close + '</div><div class="fa-list">' +
          (list.length ? list.map(row).join('') : '<div class="fa-empty">' + I.msgs + '<b>No messages yet</b><span>Questions you ask Finvry AI show here.</span></div>') +
          '</div><div class="fa-cta"><button type="button" class="fa-btn" data-new>Ask a question ' + I.send + '</button></div>';
      } else {
        html = '<div class="fa-hd"><h3>Help</h3>' + close + '</div><div class="fa-list fa-help"><p class="fa-k">Ask Finvry AI</p>' +
          HELP.map(function (h) { return '<button type="button" class="fa-li" data-new data-q="' + esc(h[1]) + '"><span><b>' + esc(h[0]) + '</b><span>' + esc(h[1]) + '</span></span><i>' + I.go + '</i></button>'; }).join('') +
          '<p class="fa-k">Pages</p>' + LINKS.map(function (l) { return '<a class="fa-li" href="' + l[1] + '"><span><b>' + esc(l[0]) + '</b></span><i>' + I.go + '</i></a>'; }).join('') +
          '<a class="fa-li" href="mailto:' + SUPPORT + '"><span><b>Talk to the team</b><span>' + SUPPORT + '</span></span><i>' + I.go + '</i></a></div>';
      }
      view.innerHTML = '<div class="fa-tab">' + html + '</div>' + nav();
      bindNav();
    }

    function newChat(q) {
      var c = { id: String(Date.now()) + Math.random().toString(36).slice(2, 6), title: 'New conversation', at: Date.now(), msgs: [] };
      cur = c.id; chats.unshift(c);
      showChat(c.id);
      if (q) ask(q);
    }

    function find(id) { for (var i = 0; i < chats.length; i++) if (chats[i].id === id) return chats[i]; return null; }

    function showChat(id) {
      var c = find(id); if (!c) return showTab(tab);
      cur = id;
      view.innerHTML = '<div class="fa-chat"><div class="fa-ch"><button type="button" class="fa-bk" aria-label="Back">' + I.back + '</button><span class="fa-av">' + I.spark + '</span><span class="fa-tt"><b>Finvry AI</b><span>The team can also help: ' + SUPPORT + '</span></span><button type="button" class="fa-x" data-close aria-label="Close">' + I.x + '</button></div>' +
        '<div class="fa-log" aria-live="polite"></div>' +
        '<form class="fa-f"><label class="sr" for="fa-q">Your question</label><textarea id="fa-q" rows="1" maxlength="400" placeholder="Ask a question about Finvry…"></textarea><button type="submit" aria-label="Send">' + I.send + '</button></form>' +
        '<p class="fa-legal">By chatting with us, you agree to our <a href="https://app.finvry.com/legal/privacy">Privacy Policy</a>. AI answers can be wrong.</p></div>';
      var log = view.querySelector('.fa-log'), form = view.querySelector('form'), q = view.querySelector('textarea');
      bubble(log, 'ai', HELLO, c.at);
      c.msgs.forEach(function (m) { bubble(log, m.role === 'user' ? 'me' : 'ai', m.text, m.at); });
      view.querySelector('.fa-bk').addEventListener('click', function () { saveChats(); showTab(tab === 'home' ? 'home' : 'msgs'); });
      view.querySelector('[data-close]').addEventListener('click', function () { open(false); launcher.focus(); });
      form.addEventListener('submit', function (e) { e.preventDefault(); var t = q.value; q.value = ''; q.style.height = ''; ask(t); });
      q.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit', { cancelable: true })); } });
      q.addEventListener('input', function () { q.style.height = ''; q.style.height = Math.min(q.scrollHeight, 120) + 'px'; });
      if (busy) wait(log);
      setTimeout(function () { q.focus(); }, 30);
    }

    function bubble(log, who, text, at) {
      var d = document.createElement('div'); d.className = 'fa-m fa-' + who;
      d.innerHTML = '<div class="b">' + (who === 'me' ? esc(text) : fmt(text)) + '</div>' + (who === 'ai' ? '<em>Finvry AI · ' + ago(at || Date.now()) + '</em>' : '');
      log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
    }
    function wait(log) { var d = document.createElement('div'); d.className = 'fa-m fa-ai fa-wait'; d.innerHTML = '<div class="b"><i></i><i></i><i></i></div>'; log.appendChild(d); log.scrollTop = log.scrollHeight; return d; }

    function ask(text) {
      text = String(text || '').trim().slice(0, 400);
      var c = find(cur); if (!text || busy || !c) return;
      var chatId = c.id, live = function () { return cur === chatId ? view.querySelector('.fa-log') : null; };
      if (!c.msgs.length) c.title = text.length > 60 ? text.slice(0, 57) + '…' : text;
      c.msgs.push({ role: 'user', text: text, at: Date.now() }); c.at = Date.now();
      chats = [c].concat(chats.filter(function (x) { return x.id !== chatId; })); saveChats();
      if (live()) bubble(live(), 'me', text);
      var reply = function (t, keep) {
        var l = live(); var w = l && l.querySelector('.fa-wait'); if (w) w.remove();
        if (keep) { c.msgs.push({ role: 'assistant', text: t, at: Date.now() }); c.at = Date.now(); saveChats(); }
        if (live()) bubble(live(), 'ai', t); else if (panel.hidden) { badge.hidden = false; }
      };
      if (HUMAN.test(text)) { setTimeout(function () { reply(HUMAN_REPLY, true); }, 250); return; }
      if (c.msgs.filter(function (m) { return m.role === 'user'; }).length > 6) { setTimeout(function () { reply('That is as far as I can go in one conversation. Start a new one, or email ' + SUPPORT + ' and the team will help.', true); }, 250); return; }
      busy = true; if (live()) wait(live());
      send(c, null, function (t, keep) { reply(t, keep); busy = false; });
    }

    // Questions go to the app. The first one in a while may need a quick human check (Cloudflare Turnstile): the app
    // answers 401 "human", the page shows the check, and the retry carries its token. The app then returns a pass that
    // covers the next few hours, so the check does not repeat.
    var PASS = 'fv_ask_pass';
    function send(c, token, done) {
      var pass = ''; try { pass = sessionStorage.getItem(PASS) || ''; } catch (e) {}
      var body = { messages: c.msgs.slice(-13).map(function (m) { return { role: m.role, text: m.text }; }) };
      if (pass) body.pass = pass; if (token) body.turnstile = token;
      // text/plain keeps this a simple request (no CORS preflight); the server reads the JSON body.
      fetch(API, { method: 'POST', headers: { 'content-type': 'text/plain;charset=UTF-8' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }, function () { return { ok: false, j: null }; }); })
        .then(function (x) {
          var err = x.j && x.j.data && x.j.data.error;
          if (x.ok && x.j && x.j.pass) { try { sessionStorage.setItem(PASS, x.j.pass); } catch (e) {} }
          if (x.ok && x.j && x.j.answer) return done(x.j.answer, true);
          if (err && (err.code === 'human' || err.code === 'captcha') && !token) { try { sessionStorage.removeItem(PASS); } catch (e) {} return human(c, done); }
          done((err && err.message) || 'Finvry AI could not answer just now. Try again, or email ' + SUPPORT + '.', false);
        })
        .catch(function () { done('Finvry AI could not be reached. Try again, or email ' + SUPPORT + '.', false); });
    }
    var siteKey = null, tsLoading = null;
    function loadTurnstile() {
      if (tsLoading) return tsLoading;
      tsLoading = fetch(API).then(function (r) { return r.json(); }).then(function (j) {
        siteKey = j && j.site_key; if (!siteKey) throw new Error('no key');
        if (window.turnstile) return;
        return new Promise(function (ok, no) { var s = document.createElement('script'); s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'; s.async = true; s.onload = ok; s.onerror = no; document.head.appendChild(s); });
      });
      tsLoading.catch(function () { tsLoading = null; });
      return tsLoading;
    }
    function human(c, done) {
      loadTurnstile().then(function () {
        var l = view.querySelector('.fa-log'), w = l && l.querySelector('.fa-wait');
        var box = document.createElement('div'); box.className = 'fa-m fa-ai fa-human';
        box.innerHTML = '<div class="b"><span>Quick check that you are a person, then I will answer.</span><div class="fa-ts"></div></div>';
        if (l) { if (w) l.insertBefore(box, w); else l.appendChild(box); l.scrollTop = l.scrollHeight; }
        window.turnstile.render(box.querySelector('.fa-ts'), {
          sitekey: siteKey, theme: 'light', size: 'flexible',
          callback: function (tok) { box.remove(); send(c, tok, done); },
          'error-callback': function () { box.remove(); done('The check could not load. Email ' + SUPPORT + ' and the team will help.', false); }
        });
      }).catch(function () { done('Finvry AI could not be reached. Try again, or email ' + SUPPORT + '.', false); });
    }
  }
  document.readyState !== 'loading' ? init() : document.addEventListener('DOMContentLoaded', init);
})();
// Product screens: the app is drawn at full size and scaled to fit its laptop or tablet frame.
(function () {
  var fit = function (s) { var w = +s.dataset.w; if (!s.clientWidth) return; Array.prototype.forEach.call(s.children, function (i) { i.style.transform = 'scale(' + (s.clientWidth / w) + ')'; }); };
  // Screens with more than one layer show them in turn while on screen (charts redraw each time a layer comes in).
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cycle = function (s, delay) {
    var layers = s.children; if (layers.length < 2 || still) return;
    var i = 0, t = null, seen = false;
    var step = function () { layers[i].classList.remove('on'); i = (i + 1) % layers.length; layers[i].classList.add('on'); };
    var go = function (on) { clearInterval(t); t = null; if (on) t = setInterval(step, 6000); };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && !seen) { seen = true; setTimeout(function () { go(true); }, delay); } else if (seen) go(e.isIntersecting); }); }, { threshold: .3 }).observe(s);
    else setTimeout(function () { go(true); }, delay);
  };
  var run = function () {
    var all = document.querySelectorAll('.dv-scr');
    all.forEach(fit);
    all.forEach(function (s, k) { cycle(s, (k % 2) * 3000); });
    if ('ResizeObserver' in window) { var ro = new ResizeObserver(function (es) { es.forEach(function (e) { fit(e.target); }); }); all.forEach(function (s) { ro.observe(s); }); }
    else addEventListener('resize', function () { all.forEach(fit); });
  };
  document.readyState !== 'loading' ? run() : document.addEventListener('DOMContentLoaded', run);
})();
// Live graphics on the marketing pages (sample data): bars shift, a highlight moves down a list, a status line changes,
// counters tick and the cap table flips between today and after the round. Only while on screen; off with reduced motion.
(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var timers = [];
  var every = function (el, ms, fn) {
    var t = null;
    var on = function (yes) { clearInterval(t); t = yes ? setInterval(fn, ms) : null; };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { on(es[0].isIntersecting); }, { threshold: .2 }).observe(el); else on(true);
  };
  var start = function () {
    document.querySelectorAll('[data-live="bars"]').forEach(function (box) {
      var bars = box.querySelectorAll('.f-bar'), base = [].map.call(bars, function (b) { return parseFloat(b.style.height); });
      var low = +box.dataset.low || 0, hiLast = box.dataset.hi === 'last';
      every(box, 2600, function () {
        bars.forEach(function (b, i) {
          var v = hiLast && i === bars.length - 1 ? Math.min(100, base[i] * (0.94 + Math.random() * 0.12)) : Math.max(8, Math.min(100, base[i] * (0.7 + Math.random() * 0.6)));
          if (hiLast && i === bars.length - 1) v = Math.max(v, Math.max.apply(null, [].map.call(bars, function (x, k) { return k < bars.length - 1 ? parseFloat(x.style.height) : 0; })) + 4);
          b.style.animation = 'none'; b.style.height = Math.min(100, v).toFixed(0) + '%';
          if (low) b.style.background = v < low ? '#9aa4b2' : (box.closest('.f-navy') ? '#6fb0ff' : '#2f6fb3');
        });
      });
    });
    document.querySelectorAll('[data-cycle]').forEach(function (box) {
      var kids = box.children, i = 0;
      every(box, +box.dataset.cycle || 2500, function () { kids[i].classList.remove('on'); i = (i + 1) % kids.length; kids[i].classList.add('on'); });
    });
    document.querySelectorAll('[data-rotate]').forEach(function (el) {
      if (el.dataset.sync) return;
      var items = []; try { items = JSON.parse(el.dataset.rotate); } catch (e) {} if (items.length < 2) return;
      var i = 0;
      every(el, 3400, function () { el.classList.add('out'); setTimeout(function () { i = (i + 1) % items.length; el.textContent = items[i]; el.classList.remove('out'); }, 350); });
    });
    document.querySelectorAll('[data-count]').forEach(function (el) {
      var n = +el.dataset.count, st = +el.dataset.step || 1;
      every(el, 4000, function () { n += 1 + Math.floor(Math.random() * st); el.textContent = n.toLocaleString('en-US'); });
    });
    document.querySelectorAll('[data-swap]').forEach(function (bar) {
      var key = bar.dataset.swap, A = bar.dataset.a.split(','), B = bar.dataset.b.split(','), segs = bar.children, b = false;
      var label = document.querySelector('[data-sync="' + key + '"]'), tile = bar.closest('.f-bt');
      // a: founders, seed, safes, pool -> segments 0,1,2,4 (3 is the new round, empty today)
      var widths = function (useB) { return useB ? B : [A[0], A[1], A[2], '0', A[3]]; };
      every(bar, 4200, function () {
        b = !b; var w = widths(b);
        [].forEach.call(segs, function (s, k) { s.style.width = w[k] + '%'; });
        if (label) { var items = JSON.parse(label.dataset.rotate); label.textContent = items[b ? 1 : 0]; }
        if (tile) tile.querySelectorAll('.f-capleg b').forEach(function (x) { x.textContent = b ? x.dataset.b : x.dataset.a; });
      });
    });
  };
  document.readyState !== 'loading' ? start() : document.addEventListener('DOMContentLoaded', start);
})();
