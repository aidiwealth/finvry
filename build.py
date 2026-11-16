"""Builds finvry.com from shared parts: python3 build.py

Rewrites the body of every page between <body> and the end of the footer, keeping each page's <head> and the
live-data scripts after the footer (country pricing, services catalog, perks, partner list and form, cookies).
Home, Founders, Startups raising, Finance teams and About get new bodies; Pricing, Compare and Partners keep
their working sections and get the shared header, closing banner and footer.
"""
import math
import re
from pathlib import Path

from mockups import mac, ipad, pair

ROOT = Path(__file__).parent
R2 = 'https://pub-4af29fd81be44e49861e29c7da302f4a.r2.dev/'
APP = 'https://app.finvry.com'


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def icon(d):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


I = {
    'metrics': 'M4 19V9M10 19V5M16 19v-7M22 19H2',
    'raise': 'M12 3v18M17 7.5c0-1.9-2.2-3.5-5-3.5s-5 1.6-5 3.5 2.2 3.5 5 3.5 5 1.6 5 3.5-2.2 3.5-5 3.5-5-1.6-5-3.5',
    'cal': 'M4 6h16v14H4zM4 10h16M9 3v4M15 3v4',
    'mail': 'M3 6h18v12H3zM3 7l9 6 9-6',
    'deck': 'M4 5h16v11H4zM8 20h8M12 16v4',
    'doc': 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6',
    'books': 'M4 6h16M4 12h16M4 18h10',
    'board': 'M4 5h7v6H4zM13 5h7v14h-7zM4 13h7v6H4z',
    'shield': 'M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z',
    'up': 'M4 18l5-6 4 3 7-9M15 6h5v5',
    'team': 'M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3 2.5-5 5-5s5 2 5 5M11 20c0-3 2.5-5 5-5s5 2 5 5',
}

# ---------------------------------------------------------------- shared parts

PRODUCT = [('Founders', 'Updates, deck and paperwork', '/founders/', 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5'),
           ('Startups raising', 'Pipeline, data room and SAFEs', '/startups-raising/', 'M4 18l5-6 4 3 7-9M15 6h5v5'),
           ('Finance teams', 'Books, statements and boards', '/finance-teams/', 'M4 19V9M10 19V5M16 19v-7M22 19H2'),
           ('Finvry vs others', 'How Finvry compares', '/compare/', 'M7 4v16M17 4v16M3 8l4-4 4 4M13 16l4 4 4-4')]
PRODUCT_KEYS = {'home', 'founders', 'raising', 'finance', 'compare'}


def NAV(active):
    on = lambda k: ' class="on" aria-current="page"' if k == active else ''
    menu = ''.join(f'<a href="{u}"><i>{icon(ic)}</i><span><b>{t}</b><em>{d}</em></span></a>' for t, d, u, ic in PRODUCT)
    mob = ''.join(f'<a href="{u}">{t}</a>' for t, d, u, ic in PRODUCT)
    return f'''<header class="f-hd"><div class="f-w">
  <a class="f-brand" href="/" aria-label="Finvry home"><img src="/finvry-logo.svg" alt="Finvry"></a>
  <nav class="f-nav" aria-label="Main"><div class="f-dd"><button type="button" class="f-ddb{' on' if active in PRODUCT_KEYS else ''}" aria-expanded="false" aria-haspopup="true">Product<svg width="10" height="10" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.4"/></svg></button><div class="f-ddm">{menu}</div></div><a href="/pricing/"{on('pricing')}>Pricing</a><a href="/about/"{on('about')}>About us</a></nav>
  <div class="f-hda"><a class="si" href="{APP}/login">Sign in</a><a class="f-btn dk" href="{APP}/start">Get started free</a>
  <button type="button" class="f-mb" aria-label="Menu" aria-expanded="false" aria-controls="f-mm"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></button></div>
</div><div class="f-mm" id="f-mm" hidden><span class="f-mml">Product</span>{mob}<a href="/pricing/">Pricing</a><a href="/about/">About us</a><a href="{APP}/login">Sign in</a><a class="f-btn dk" href="{APP}/start">Get started free</a></div></header>'''


def CTA(head, accent, video=None):
    v = f'<video class="f-vid" autoplay muted loop playsinline preload="none" aria-hidden="true"><source src="{R2}{video}" type="video/mp4"></video><div style="position:absolute;inset:0;background:rgba(3,6,12,.72)"></div>' if video else ''
    return f'''<section class="f-cta"><div class="f-box"><div class="f-gridbg"></div>{v}
  <div class="in"><h2>{head} <span class="f-emd">{accent}</span></h2>
  <div class="f-acts" style="justify-content:center"><a class="f-btn lt" href="{APP}/start">Start your 14-day free trial →</a><a class="f-btn ln" href="/pricing/">See pricing</a></div></div>
</div></section>'''


SOC = '''<div class="f-soc"><a href="https://x.com/finvry" aria-label="Finvry on X"><svg viewBox="0 0 24 24"><path d="M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7.4 4.7H5.6z" fill="currentColor"/></svg></a><a href="https://www.linkedin.com/company/finvry" aria-label="Finvry on LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5M3 9.5h4v11H3zm7 0h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6v5.4h-4v-4.8c0-1.2 0-2.6-1.6-2.6s-1.9 1.2-1.9 2.5v4.9h-4z" fill="currentColor"/></svg></a><a href="mailto:support@finvry.com" aria-label="Email support@finvry.com"><svg viewBox="0 0 24 24"><path d="M3 5h18v14H3z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m3.5 6 8.5 7 8.5-7" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></a></div>'''

FCOLS = [
    ('Product', [('Investor metrics', '/finance-teams/'), ('Fundraising', '/startups-raising/'), ('Compliance calendar', '/#product'), ('Investor updates', '/founders/'), ('Finvry AI', '/#ai')]),
    ('Platform', [('Integrations', '/#integrations'), ('Investor page', '/#features'), ('Boards', '/finance-teams/'), ('API documentation', APP + '/developers')]),
    ('Plans', [('Pricing', '/pricing/'), ('Company services', '/pricing/#services'), ('Partner discounts', '/partners/')]),
    ('Customers', [('Founders', '/founders/'), ('Startups raising', '/startups-raising/'), ('Finance teams', '/finance-teams/'), ('Founder perks', APP + '/rewards')]),
    ('Resources', [('Finvry vs others', '/compare/'), ('System status', APP + '/status'), ('Support', 'mailto:support@finvry.com')]),
    ('Company', [('About us', '/about/'), ('Sign in', APP + '/login'), ('Create an account', APP + '/start')]),
]


def FOOT():
    cols = ''.join(f'<div><h4>{h}</h4>' + ''.join(f'<a href="{u}">{t}</a>' for t, u in ls) + '</div>' for h, ls in FCOLS)
    countries = ''.join(f'<option>{c}</option>' for c in ['United States', 'Canada', 'Nigeria', 'Kenya', 'Ghana', 'United Kingdom', 'Others'])
    return f'''<footer class="f-ft"><div class="f-wi">
  <div class="f-fcols">{cols}</div>
  <div class="f-frow"><a href="/" aria-label="Finvry home"><img src="/finvry-logo.svg" alt="Finvry"></a>{SOC}</div>
  <div class="f-legal"><label><svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" fill="none" stroke="currentColor" stroke-width="1.6"/></svg><span class="sr">Country</span><select aria-label="Country">{countries}</select></label>
    <a href="{APP}/legal/terms">Terms of Service</a><a href="{APP}/legal/privacy">Privacy Policy</a><a href="{APP}/status">System status</a><a href="mailto:support@finvry.com">Contact support</a></div>
  <div class="f-small">
    <p>© <span class="yr">2026</span> TAGroup. Finvry is a product of TAGroup. All rights reserved.</p>
    <p>Finvry is software. It is not a broker-dealer, funding portal, investment adviser, bank, law firm or accounting firm, and does not offer, sell or solicit securities. Company services are offered in the United States and parts of Africa. Documents and AI output are not legal, tax, accounting or investment advice; review them with qualified advisers before you rely on them.</p>
    <p>Third-party names and trademarks belong to their owners and are used for identification only.</p>
    <p>For any questions, email <a href="mailto:support@finvry.com">support@finvry.com</a> or write to Finvry at 6472 Camden Ave, Suite 204, San Jose, CA 95120, US.</p>
  </div>
</div></footer>'''


def head_card(lab, h2, sub, light=True):
    return f'<div class="f-head"><p class="f-lab">{lab}</p><h2 class="f-h2">{h2}</h2><p class="f-sub">{sub}</p></div>'


def cards(rows, cls='f-cols4'):
    out = ''
    for r in rows:
        out += f'''<a class="f-card" href="{r['href']}"><span class="f-ico">{icon(I[r['icon']])}</span><span class="f-tag">{r['kicker']}</span>
<span class="t">{r['title']}</span><span class="d">{r['body']}</span><span class="ft"><span>{r['chipL']} · <b>{r['chipV']}</b></span><i>→</i></span></a>'''
    return f'<div class="{cls}">{out}</div>'


def showcase(rows, lab='See it work', span=(5, 7)):
    tabs = ''
    for i, r in enumerate(rows):
        pts = ''.join(f'<li><span class="f-tick">✓</span>{p}</li>' for p in r.get('points', []))
        extra = (f'<ul>{pts}</ul>' if pts else '') + (f'<a class="f-link" href="{r["href"]}">{r["cta"]} →</a>' if r.get('cta') else '')
        tabs += f'''<div class="f-tab{' on' if i == 0 else ''}" data-i="{i}" data-video="{R2}{r['video']}" data-k="{esc(r['kicker'])}" data-l="{esc(r['chipL'])}" data-v="{esc(r['chipV'])}"><button type="button" aria-expanded="{'true' if i == 0 else 'false'}">{r['kicker']}</button><div class="bd"><p>{r['body']}</p>{extra}</div></div>'''
    r0 = rows[0]
    return f'''<section class="f-inset f-show"><div class="f-box f-navy"><div class="f-g f-wi" style="max-width:1312px;margin:0 auto">
  <div class="s{span[0]}"><p class="f-lab" style="margin-bottom:16px">{lab}</p><div class="f-tabs" data-show>{tabs}</div></div>
  <div class="s{span[1]} f-media"><div class="f-gridbg"></div><div class="f-ghost" data-sk>{r0['kicker']}</div>
    <video class="f-vid" data-sv autoplay muted loop playsinline preload="none" aria-hidden="true"><source src="{R2}{r0['video']}" type="video/mp4"></video>
    <div class="f-chip"><span data-sl>{r0['chipL']}</span><b data-sc>{r0['chipV']}</b></div></div>
</div></div></section>'''


def hero_video(video, lab, h1a, h1b, sub, size=92):
    return f'''<section class="f-inset" style="padding-top:6px"><div class="f-box f-navy">
  <video class="f-vid" autoplay muted loop playsinline preload="metadata" aria-hidden="true"><source src="{R2}{video}" type="video/mp4"></video><div class="f-scrim"></div>
  <div class="f-hero"><div class="f-herocol"><p class="f-lab">{lab}</p><h1 class="f-h1" style="max-width:900px">{h1a} <span class="f-emd">{h1b}</span></h1>
  <p class="f-sub">{sub}</p><div class="f-acts"><a class="f-btn lt" href="{APP}/start">Start free for 14 days →</a><a class="f-btn ln" href="/pricing/">See pricing</a></div></div></div>
</div></section>'''


def dev(lab, h2, sub, laptop, tablet, side='right', big=False):
    """The app in a laptop with a tablet beside it (sample data from mockups.py). Compact: heading left, text right.
    big: the heading stacked above and the devices across the band (the home page)."""
    if big:
        return f'<section class="f-dev big"><div class="f-box">{head_card(lab, h2, sub)}{pair(laptop, tablet, side)}</div></section>'
    return f'<section class="f-dev"><div class="f-box"><div class="f-devhead"><div><p class="f-lab">{lab}</p><h2 class="f-h2">{h2}</h2></div><p class="f-sub">{sub}</p></div>{pair(laptop, tablet, side)}</div></section>'


# A generic, faded seal for the sample notice (not any agency's emblem).
CREST = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18.5" fill="none" stroke="currentColor" stroke-width="1.2"/>'
         '<circle cx="20" cy="20" r="14.5" fill="none" stroke="currentColor" stroke-width=".8" stroke-dasharray="1.2 1.6"/>'
         '<path d="M20 9.5l2.2 4.5 5 .7-3.6 3.5.9 5-4.5-2.4-4.5 2.4.9-5-3.6-3.5 5-.7z" fill="currentColor"/>'
         '<path d="M11 27c3 2.6 6 3.6 9 3.6s6-1 9-3.6M13 24.5c2.3 1.8 4.6 2.6 7 2.6s4.7-.8 7-2.6" fill="none" stroke="currentColor" stroke-width="1"/></svg>')


def filing(steps=('EIN (SS-4) submitted', 'Formation documents filed', 'Registered agent included, year 1'), doc=('Department of the Treasury<br>Internal Revenue Service', 'Sample notice', 'Date of this notice: 03-14-2026<br>Employer ID number: 00-0000000<br>Form: SS-4<br>Number of this notice: CP 575 G', 'We assigned you an employer identification number')):
    """A company-services visual: a sample notice behind a card of completed steps. Sample company, sample number."""
    tick = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#1c547d"/><path d="m7 12.5 3.2 3L17 9" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    rows = ''.join(f'<li>{tick}<span>{t}</span></li>' for t in steps)
    return f'''<div class="f-file" aria-hidden="true"><div class="doc"><div class="dh"><span class="crest">{CREST}<span><b>{doc[0]}</b>{doc[1]}</span></span><span>{doc[2]}</span></div>
<div class="dt"><span>KESTREL LABS INC<br>ATTN: AMARA OKAFOR<br>548 MARKET ST<br>SAN FRANCISCO, CA 94104</span><span>{doc[3]}</span></div><i></i><i></i><i class="s"></i></div>
<ol class="card">{rows}</ol></div>'''


# ---------------------------------------------------------------- home

JOBS = [
    dict(kicker='Investor metrics', icon='metrics', title='Your numbers, always investor-ready.', body='Statements, burn, runway and retention, straight from your books.', video='investor-ready.mp4', chipL='Runway', chipV='21 months', href='/finance-teams/'),
    dict(kicker='Fundraise', icon='raise', title='Run the round, not the admin.', body='Pipeline, invite-only data room, deck analytics and SAFEs.', video='run-round.mp4', chipL='Seed round', chipV='$1.9M of $2.5M', href='/startups-raising/'),
    dict(kicker='Requirements', icon='cal', title='Never miss what you owe.', body='Every filing and renewal on one calendar, with reminders.', video='miss-owe.mp4', chipL='Next due', chipV='Delaware franchise tax', href='/pricing/#services'),
    dict(kicker='Investor updates', icon='mail', title='Updates investors actually read.', body='Drafted from your metrics, with opens and replies tracked.', video='investor-update.mp4', chipL='September update', chipV='Opened by 36 of 42', href='/founders/'),
]
ASK = [
    dict(label='Runway', ask='How long is our runway?', src='QuickBooks · last 6 months', answer='At your average burn, cash lasts about 21 months.', kpis=[('Cash', '$1.4M'), ('Burn / mo', '$66k'), ('Runway', '21 months')]),
    dict(label='Update', ask='Draft the September update.', src='Books · last update', answer='Drafted: strong quarter, two key hires, raising next. Ready for your edit.', kpis=[('Q3 revenue', '$84,210'), ('New hires', '2'), ('Recipients', '42')]),
    dict(label='Round', ask='Where is the seed round?', src='Pipeline · SAFEs', answer='$1.9M committed of $2.5M. Three investors opened the data room this week.', kpis=[('Committed', '$1.9M'), ('Target', '$2.5M'), ('Progress', '76%')]),
    dict(label='Deadlines', ask='What do we owe this quarter?', src='Compliance calendar', answer='Delaware franchise tax and the Q4 investor report are next. Reminders are set.', kpis=[('Due soon', '2'), ('Overdue', 'None'), ('Filed', '5')]),
]
APPS = [('/logos/quickbooks.png', 'QuickBooks', 'Live sync', 'Statements and transactions, synced from your books.'), ('/logos/google-sheets.png', 'Google Sheets', 'Live sync', 'Keep your model in Sheets; Finvry reads it on schedule.'),
        ('/logos/excel.png', 'Excel', 'Import', 'Upload a workbook and map it once.'), ('/logos/bank.svg', 'Bank accounts', 'Read-only', 'Balances and money in and out, never moved.'),
        ('/logos/pdf.svg', 'PDF statements', 'AI import', 'Finvry AI reads past statements and reports.'), ('/finvry-mark.svg', 'Finvry Data API', 'Two-way', 'Push data in or pull metrics out of your own tools.')]
FAQ_HOME = [('What does Finvry do?', 'Finvry keeps the investor side of your company in one place: metrics, fundraising, compliance and investor updates, with AI that drafts the work.'),
            ('Does Finvry hold or move money?', 'No. Finvry is software. It reads balances to show burn and runway, and never moves funds.'),
            ('Which tools does it connect to?', 'QuickBooks, Google Sheets, Excel, PDF statements and bank accounts, plus the Finvry Data API.'),
            ('Is there a free plan?', 'Yes. The Free plan covers your dashboard, annual report, investor page and data room. Paid plans start with 14 days free.'),
            ('Where is Finvry available?', 'The software works anywhere. Company services are offered in the United States and parts of Africa.')]


def faq(items):
    return '<div class="f-faq">' + ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items)) + '</div>'


def bars(h, hi, fn):
    return ''.join(f'<div class="f-bar" style="flex:1;height:{v}%;background:{fn(v, i)};animation-delay:{i * 40}ms"></div>' for i, v in enumerate(h))


def home():
    a0, ap = ASK[0], ASK[3]
    kp = ''.join(f'<span>{l} <b>{v}</b></span>' for l, v in a0['kpis'])
    tabs = ''.join(f'<button type="button"{" class=on" if i == 0 else ""} data-i="{i}">{a["label"]}</button>' for i, a in enumerate(ASK))
    apps = ''.join(f'<div class="f-app"><div class="top"><span class="f-logo img"><img src="{m}" alt="{n}" width="48" height="48" loading="lazy"></span><span class="tg{" live" if t == "Live sync" else ""}">{t}</span></div><div><b>{n}</b><p>{d}</p></div></div>' for m, n, t, d in APPS)
    flow = ''.join(f'<div class="st"><span class="n">{i + 1}</span><span><b>{t}</b><em>{b}</em></span></div>' for i, (t, b) in enumerate([('Connect', 'Sign in to your books or drop in a file.'), ('Finvry reads it', 'Statements, metrics and runway, worked out.'), ('Stays current', 'Every report, update and page refreshes itself.')]))
    revbars = bars([38, 44, 41, 52, 49, 58, 61, 57, 66, 72, 70, 84], None, lambda v, i: '#2f6fb3' if i == 11 else '#c7d7ea')
    slbars = bars([90, 75, 82, 40, 66, 58, 30, 52, 20, 44], None, lambda v, i: '#9aa4b2' if v < 35 else '#2f6fb3')
    trust = ''.join(f'<div><b>{t}</b><span>{b}</span></div>' for t, b in [('Access by role', 'Your team, board and advisers see only what they need.'), ('Private by default', 'Invite-only data rooms and access you can revoke at once.'), ('A record of every change', 'Who edited, sent or shared what, and when.'), ('Open about uptime', 'A public status page and a documented API.')])
    svc = ''.join(f'<a href="{APP}/start">{n}<span>{d} →</span></a>' for n, d in [('C-Corp (Inc) formation', 'Delaware or any state'), ('LLC formation', 'Any state'), ('EIN application', 'From the IRS'), ('Registered agent', 'Handled every year'), ('State tax filing', 'Filed on time'), ('Federal annual filing', 'Prepared and filed')])
    return f'''<main>
<section class="f-inset" style="padding-top:6px"><div class="f-box f-navy">
  <video class="f-vid" autoplay muted loop playsinline preload="metadata" aria-hidden="true"><source src="{R2}hero2.mp4" type="video/mp4"></video><div class="f-scrim"></div>
  <div class="f-hero f-g" style="align-items:center">
    <div class="s7 f-herocol"><p class="f-lab" style="display:flex;gap:10px;align-items:center"><span class="f-dot"></span>The OS for every founder</p>
      <h1 class="f-h1">Be always <span class="f-emd">investor&#8209;ready.</span></h1>
      <p class="f-sub">Metrics, your raise, deadlines and investor updates in one place, kept current by AI.</p>
      <div class="f-acts"><a class="f-btn lt" href="{APP}/start">Get started free →</a><a class="f-btn ln" href="/pricing/">See pricing</a></div></div>
    <div class="s5 f-hide-m"><div class="f-ai" data-ai aria-live="polite">
      <div class="prev"><div class="q" data-pq>{ap['ask']}</div><div class="a" data-pa>{ap['answer']}</div></div>
      <div class="f-fade" data-cur style="display:flex;flex-direction:column;gap:10px"><div class="q" data-q>{a0['ask']}</div>
        <div class="ans"><span class="src"><span class="f-dot" style="width:5px;height:5px"></span>Finvry AI · <span data-src>{a0['src']}</span></span><span data-a>{a0['answer']}</span><div class="kp" data-kp>{kp}</div></div></div>
      <div class="tabs">{tabs}</div><span class="note">Sample company</span></div></div>
  </div>
</div></section>

{dev('Inside Finvry', 'Your company, <span class="f-em">on one screen.</span>', 'Revenue, cash, runway and live bank balances sit next to your raise, your investor page and<br class="f-br"> what is due next. Every figure comes from your books and updates itself.', ('dashboard', 'financials', 'fundraising'), ('captable', 'model'), big=True)}

<section class="f-sec" id="product"><div class="f-w">
  {head_card('The platform', 'Four jobs, one place. <span class="f-em">Done properly.</span>', 'Investor metrics, fundraising, requirements and investor updates. Everything a founder owes investors, kept in one workspace.')}
  {cards(JOBS)}
</div></section>

<section class="f-inset" id="ai"><div class="f-box f-navy"><div class="f-wi" style="padding-top:110px;padding-bottom:110px">
  <div class="f-split"><div><p class="f-lab">Finvry AI</p><h2 class="f-h2" style="font-size:64px">An analyst that <span class="f-emd">already knows your numbers.</span></h2></div><p class="f-sub">It reads your books and drafts the work. You stay the editor.</p></div>
  <div class="f-cols3">
    <div class="f-ai3"><span class="k">01 · Reads</span><div style="display:flex;flex-wrap:wrap;gap:6px"><span class="f-pill">QuickBooks</span><span class="f-pill">Google Sheets</span><span class="f-pill">Excel</span><span class="f-pill">PDF</span></div><span class="m">Connect live books or drop in last year's files.</span></div>
    <div class="f-ai3"><span class="k">02 · Drafts</span><div style="background:#fff;color:#14161a;padding:14px;display:flex;flex-direction:column;gap:6px"><span class="f-lab" style="font-size:10.5px;color:#1c547d">September update</span><span style="font-size:14px;line-height:1.45">Q3 revenue reached $84,210 and runway is 21 months. Two key hires joined…</span></div><span class="m">With your real figures, never invented ones.</span></div>
    <div class="f-ai3"><span class="k">03 · You decide</span><div style="display:flex;gap:8px;flex-wrap:wrap"><span style="background:#fff;color:#0c1a2e;padding:9px 14px;font-size:14px;font-weight:600">Send to 42 investors</span><span class="f-pill">Edit</span></div><span class="m">Nothing goes out until you review and send it.</span></div>
  </div>
</div></div></section>

<section class="f-sec" id="integrations"><div class="f-w">
  <div class="f-split"><div><p class="f-lab">Integrations</p><h2 class="f-h2">Works with the tools <span class="f-em">you already use.</span></h2></div><p class="f-sub">Connect once. Your numbers stay current without copying a cell.</p></div>
  <div class="f-g" style="gap:14px"><div class="s4 f-flow"><p class="f-lab">How it flows</p><div style="display:flex;flex-direction:column;gap:12px">{flow}</div><a class="f-btn lt" style="align-self:flex-start;font-size:15px;padding:12px 16px" href="{APP}/start">Connect your books →</a></div>
  <div class="s8 f-cols3">{apps}</div></div>
</div></section>

<section class="f-sec t0" id="features"><div class="f-w">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:20px;margin-bottom:32px"><h2 class="f-h2" style="max-width:720px">Everything a raise needs, <span class="f-em">already built.</span></h2><a class="f-link" href="{APP}/start">Try it free →</a></div>
  <div class="f-g" style="gap:12px;grid-template-columns:repeat(6,minmax(0,1fr))">
    <div class="s3 f-bt" style="grid-column:span 3"><p class="f-lab">Investor page</p><span class="h">One link, always current.</span>
      <div class="f-wht"><div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:#6b7280">finvry.com/your-company</span><span style="color:#1c547d;display:flex;gap:6px;align-items:center"><span class="f-dot" style="width:6px;height:6px;background:#2f6fb3"></span>Live · <span data-count="128" data-step="3">128</span> views</span></div>
      <div class="f-bars" style="gap:5px;height:70px" data-live="bars" data-hi="last">{revbars}</div>
      <div class="f-chips" data-cycle="2600"><span class="on">Deck</span><span>Data room · invite only</span><span>Cap table</span><span>Updates</span></div></div></div>
    <div class="s3 f-bt" style="grid-column:span 3"><p class="f-lab">Deck analytics</p><span class="h">See which slide they stopped on.</span>
      <div class="f-wht"><div class="f-bars" style="height:104px" data-live="bars" data-low="35">{slbars}</div><div style="display:flex;justify-content:space-between;font-size:12.5px;color:#6b7280"><span>Slide 1</span><span data-rotate='["Time spent per slide","Deck v5 · read by Harbor Lane Capital","Deck v5 · read by Meridian Seed Fund","Deck v5 · read by Atlas Angels"]'>Time spent per slide</span><span>Slide 10</span></div></div></div>
    <div class="f-bt" style="grid-column:span 2"><p class="f-lab">Data room</p><div class="f-rows" data-cycle="2200"><div class="f-row on"><span>Financials</span><span style="color:#6b7280">12 files</span></div><div class="f-row"><span>Legal</span><span style="color:#6b7280">8 files</span></div><div class="f-row"><span>Seed round</span><span style="color:#1c547d">NDA</span></div></div>
      <span class="f-live"><span class="f-dot" style="width:6px;height:6px;background:#2f6fb3"></span><span data-rotate='["Opened by Harbor Lane Capital · just now","NDA signed by Meridian Seed Fund · 2 min ago","Financials downloaded by Atlas Angels · 6 min ago"]'>Opened by Harbor Lane Capital · just now</span></span></div>
    <div class="f-bt" style="grid-column:span 2"><p class="f-lab">Cap table · <span data-rotate='["Today","After the round"]' data-sync="cap">Today</span></p>
      <div class="f-stack" data-swap="cap" data-a="62,18,12,8" data-b="50,15,10,17,8"><i style="width:62%;background:#0c1a2e"></i><i style="width:18%;background:#2f6fb3"></i><i style="width:12%;background:#9fc0e4"></i><i style="width:0%;background:#5b8fc4"></i><i style="width:8%;background:#d5dde8"></i></div>
      <div class="f-capleg"><span>■ Founders <b data-a="62%" data-b="50%">62%</b></span><span style="color:#1c547d">■ Seed <b data-a="18%" data-b="15%">18%</b></span><span style="color:#1c547d">■ SAFEs <b data-a="12%" data-b="10%">12%</b></span><span style="color:#5b8fc4">■ New round <b data-a="0%" data-b="17%">0%</b></span><span style="color:#8a96a8">■ Pool <b data-a="8%" data-b="8%">8%</b></span></div></div>
    <div class="f-bt" style="grid-column:span 2"><p class="f-lab">Deadlines</p><div class="f-rows" data-cycle="2400"><div class="f-row on"><span>Delaware franchise tax</span><span style="color:#1c547d">Mar 1</span></div><div class="f-row"><span>Q4 investor report</span><span style="color:#1c547d">Mar 15</span></div><div class="f-row"><span>Federal annual filing</span><span style="color:#6b7280">Apr 15</span></div></div>
      <span class="f-live"><span class="f-dot" style="width:6px;height:6px;background:#2f6fb3"></span><span data-rotate='["Reminder set for Delaware franchise tax","Q4 report drafted by Finvry AI","Nothing overdue"]'>Reminder set for Delaware franchise tax</span></span></div>
  </div>
</div></section>

{showcase([dict(j, body=j['title'] + ' ' + j['body']) for j in JOBS], span=(4, 8))}

<section class="f-sec" id="services"><div class="f-w">
  <div class="f-split"><div><p class="f-lab">Company services</p><h2 class="f-h2" style="font-size:52px">Form, file and <span class="f-em">stay compliant.</span></h2></div><div style="display:flex;flex-direction:column;gap:12px"><p class="f-sub" style="font-size:17px">Done for you, on every plan, Free included.</p><a class="f-link" href="/pricing/#services">See all services →</a></div></div>
  <div class="f-g" style="gap:14px;align-items:stretch"><div class="s6 f-svcv">{filing()}</div><div class="s6 f-svc">{svc}</div></div>
</div></section>

<section class="f-inset" id="developers"><div class="f-box f-pale"><div class="f-g f-wi" style="padding-top:90px;padding-bottom:90px;align-items:center;gap:48px;max-width:1312px;margin:0 auto">
  <div class="s5" style="display:flex;flex-direction:column;gap:18px"><p class="f-lab">Developers</p><h2 class="f-h2" style="font-size:44px">Built to connect. <span class="f-em">Built to stay up.</span></h2><p class="f-sub" style="font-size:17px;color:#3b414b">Twelve endpoints for statements, metrics, cap table, updates and more.</p>
    <div style="display:flex;gap:22px;flex-wrap:wrap"><a class="f-link" href="{APP}/developers">API documentation →</a><a class="f-link" href="{APP}/status" style="display:flex;gap:8px;align-items:center"><span class="f-dot" style="background:#2f6fb3"></span>System status</a></div></div>
  <div class="s7 f-code" data-code><div class="bar"><div role="tablist" aria-label="Language" style="display:flex;gap:4px"><button type="button" class="on" data-i="0">cURL</button><button type="button" data-i="1">Node</button><button type="button" data-i="2">Python</button></div><span class="ep"><span class="f-dot" style="width:6px;height:6px"></span>GET /api/v1/metrics</span></div>
    <pre data-pre></pre><div class="fn">Also: /financials · /forecasts · /cap-table · /updates · /compliance · /pipelines</div></div>
</div></div></section>

<section class="f-sec"><div class="f-w f-cols4 f-trust" style="gap:24px">{trust}</div></section>

<section class="f-sec t0"><div class="f-wi f-g" style="align-items:start;gap:48px">
  <div class="s4" style="display:flex;flex-direction:column;gap:14px"><p class="f-lab">Questions</p><h2 class="f-h2" style="font-size:48px">Still have <span class="f-em">questions?</span></h2><a class="f-link" href="mailto:support@finvry.com">Ask our team →</a></div>
  <div class="s8">{faq(FAQ_HOME)}</div>
</div></section>

<section class="f-inset f-band"><div class="f-box f-greybg"><div class="f-wi"><div><b>Backed by a VC, incubator or accelerator?</b><span>Your founders get Finvry at a partner discount.</span></div><a class="f-btn dk" href="/partners/">See partner discounts</a></div></div></section>
</main>
''' + CTA('Run your company.', 'Finvry runs the investor side.', 'runcompanybg.mp4') + FOOT()


# ---------------------------------------------------------------- founders / finance

FOUNDERS = [
    dict(kicker='Updates', icon='mail', title='Updates in ten minutes.', body='Finvry AI drafts it from your numbers. You edit, send and see who opened it.', video='updatesinten.mp4', chipL='Revenue this month', chipV='$96,400 · up 14%', points=['Metrics pulled in from your books', 'Opens and reactions tracked per investor', 'Send to a list or one investor at a time'], cta='Start your first update', href=APP + '/start'),
    dict(kicker='Deck', icon='deck', title='Know who read the deck.', body='One link per investor, time on every slide, and versions swapped under the same link.', video='deck-read.mp4', chipL='Deck v5', chipV='31 readers this week', points=['A separate link for each investor', 'Time spent on every slide', 'Upload a new version under the same link'], cta='Share your deck', href=APP + '/start'),
    dict(kicker='Paperwork', icon='doc', title='Paperwork, drafted.', body='Board resolutions, NDAs, offer letters and advisor agreements from a short form.', video='Paperwork.mp4', chipL='Board resolution', chipV='Signed by 2 of 2 directors', points=['Board resolutions and consents', 'NDAs, offer letters and advisor agreements', 'E-signed and kept in Documents'], cta='Draft a document', href=APP + '/start'),
]
FINANCE = [
    dict(kicker='Books', icon='books', title='Connected to your books.', body='QuickBooks, Sheets, Excel or PDF, into a standard P&amp;L, balance sheet and cash flow.', video='connected-books.mp4', chipL='Mapped once', chipV='Carries over every month', points=['QuickBooks, Google Sheets, Excel or PDF', 'Standard P&amp;L, balance sheet and cash flow', 'Map accounts once and it carries over'], cta='Connect your books', href=APP + '/start'),
    dict(kicker='Burn and runway', icon='metrics', title='Burn and runway, done. Then forecast.', body='The same maths every period, big swings flagged, best and worst case side by side.', video='connect-books.mp4', chipL='Q3', chipV='Runway 21 months · Margin 68%', points=['One-off costs flagged, not hidden', 'Cash plus treasury bills', 'Best and worst case forecasts side by side'], cta='See your runway', href=APP + '/start'),
    dict(kicker='One source', icon='board', title='Same numbers everywhere.', body='Boards, updates and the investor page all draw on approved figures.', video='Same-numbers.mp4', chipL='Used in', chipV='Board · Update · Investor page', points=['Approved figures feed every board', 'Updates and the investor page stay in step', 'Share live boards by link'], cta='Build a board', href=APP + '/start'),
]


def founders():
    return '<main>' + hero_video('founder-hero.mp4', 'For founders', 'Build the company.', 'Keep investors close.', 'Updates, metrics, your deck and paperwork in one place. Ten minutes a month.') + f'''
<section class="f-sec"><div class="f-w">{head_card('What changes', 'Investor relations, <span class="f-em">in ten minutes a month.</span>', 'Updates, your deck and company paperwork, handled from one workspace.')}{cards(FOUNDERS, 'f-cols3')}</div></section>
{dev('Investor relations', 'Investor, <span class="f-em">and their rights.</span>', 'Contacts, lists and updates in one place, with each investor\'s rights read from their letters. Sample company shown.', ('contacts', 'fundraising'), ('rights', 'captable'), 'left')}
{showcase(FOUNDERS)}
<section class="f-sec" id="perks"><div class="f-w">
  <div class="f-split"><div><p class="f-lab">Founder perks</p><h2 class="f-h2" style="font-size:48px">Perks on the tools you use. <span class="f-em">Free with Finvry.</span></h2></div><p class="f-sub">Credits and discounts from our partners, claimed from your workspace.</p></div>
  <div id="perks-list"><p class="pempty">Loading perks…</p></div>
  <div class="f-acts" style="margin-top:28px"><a class="f-btn dk" href="{APP}/rewards">See all perks →</a><a class="f-btn gh" href="{APP}/start">Get started to claim them</a></div>
</div></section>
</main>''' + CTA('Ten minutes a month.', 'Investors stay close.') + FOOT()


def finance():
    data = [[100, 96, 94, 92, 91, 90], [100, 97, 95, 94, 93], [100, 98, 96, 95], [100, 97, 96], [100, 99]]
    grid = ''
    for name, row in zip(['Jan', 'Feb', 'Mar', 'Apr', 'May'], data):
        grid += f'<span style="display:flex;align-items:center">{name}</span>'
        for k in range(6):
            v = row[k] if k < len(row) else None
            grid += '<span style="height:26px;background:#f4f6f9"></span>' if v is None else f'<span style="height:26px;background:rgba(29,79,134,{0.25 + (v - 88) / 12 * 0.75:.2f})"></span>'
    return '<main>' + hero_video('finance-teams.mp4', 'For finance teams', 'Close the month.', 'Report in minutes.', 'Your books, turned into statements, boards and updates, without copy and paste.') + f'''
<section class="f-sec"><div class="f-w">{head_card('For the close', 'Your books in. <span class="f-em">Reports out.</span>', 'Connect your books once. Statements, runway and boards stay current.')}{cards(FINANCE, 'f-cols3')}</div></section>
{dev('Financials', 'Numbers, <span class="f-em">already worked out.</span>', 'Statements, burn and runway from your books, and where the company stands against its stage. Sample company shown.', ('financials', 'dashboard'), ('stage', 'captable'))}
{showcase(FINANCE)}
<section class="f-sec"><div class="f-w f-g" style="gap:14px">
  <div class="s7 f-bt" style="background:#fff;border:1px solid #e2e5eb"><p class="f-lab">Retention</p><h2 class="f-h3" style="color:#0c1a2e">Know which customers <span class="f-em">stay.</span></h2><p class="f-sub" style="font-size:16px">Net and gross retention, churn and cohorts, by segment, from revenue in any layout.</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap"><span style="font-size:14px;background:#e6eef6;padding:7px 11px">Net retention 112%</span><span style="font-size:14px;background:#f4f6f9;padding:7px 11px">Enterprise 118%</span><span style="font-size:14px;background:#f4f6f9;padding:7px 11px">Gross retention 93%</span></div>
    <div style="display:grid;grid-template-columns:70px repeat(6,minmax(0,1fr));gap:4px;font-size:12px;color:#6b7280">{grid}</div><span style="font-size:12.5px;color:#8a96a8">Sample company: revenue kept by monthly cohort, darker is more</span></div>
  <div class="s5 f-navy" style="padding:28px;display:flex;flex-direction:column;gap:18px"><p class="f-lab">Annual report</p><h2 class="f-h3">Annual report, <span class="f-emd">ready to sign.</span></h2><p class="f-sub" style="font-size:16px">Directors, policies, statements, notes and shareholding, with your logo.</p>
    <div style="position:relative;height:210px;margin-top:auto"><div style="position:absolute;left:40px;top:0;width:62%;height:190px;background:#3a4f6c"></div><div style="position:absolute;left:20px;top:10px;width:62%;height:190px;background:#9fb2cc"></div>
      <div style="position:absolute;left:0;top:20px;width:62%;height:190px;background:#fff;color:#0c1a2e;padding:16px;display:flex;flex-direction:column;gap:8px"><span style="font-size:14px;font-weight:600">Annual report 2026</span><span style="height:6px;background:#e6eef6"></span><span style="height:6px;width:80%;background:#e6eef6"></span><span style="height:6px;width:65%;background:#e6eef6"></span><span style="margin-top:auto;font-size:12px;color:#6b7280">PDF · Excel</span></div>
      <div style="position:absolute;right:0;top:30px;display:flex;flex-direction:column;gap:6px;align-items:flex-end"><span class="f-pill" style="font-size:12.5px">US GAAP</span><span class="f-pill" style="font-size:12.5px">IFRS</span><span class="f-pill" style="font-size:12.5px">IFRS for SMEs</span></div></div></div>
  <div class="s12 f-g" style="border:1px solid #e2e5eb;padding:36px 40px;gap:40px;align-items:center"><div class="s6" style="display:flex;flex-direction:column;gap:12px"><b style="font-size:26px;font-weight:600;letter-spacing:-.02em;color:#0c1a2e">Form, file and stay compliant.</b><span style="font-size:16px;line-height:1.55;color:#4a515c">Formation, EIN, registered agent and state and IRS filings, ordered and tracked in your workspace, with reminders before they are due.</span><a class="f-link" href="/pricing/#services">See company services →</a></div><div class="s6">{filing(('State annual report filed', 'Delaware franchise tax paid', 'Next reminder set for Mar 1'), ('State of Delaware<br>Division of Corporations', 'Sample notice', 'Date of this notice: 03-01-2026<br>File number: 0000000<br>Tax year: 2025<br>Status: Filed', 'Annual franchise tax report received'))}</div></div>
</div></section>
</main>''' + CTA('Same numbers.', 'Every board, update and page.') + FOOT()


# ---------------------------------------------------------------- startups raising

def raising():
    sl = bars([88, 72, 80, 36, 64, 58, 28, 50, 22, 46], None, lambda v, i: '#4a5a73' if v < 35 else '#6fb0ff')
    cols = [('Contacted', [('Seed fund', 'Intro sent'), ('Angel syndicate', 'Follow up Friday')]), ('First call', [('Fintech fund', 'Call booked'), ('Operator angel', 'Deck opened twice')]),
            ('Diligence', [('Growth fund', 'In the data room')]), ('Committed', [('Northgate', '$500k committed'), ('Lead investor', 'SAFE signed')])]
    board = ''.join(f'<div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);padding:14px;display:flex;flex-direction:column;gap:8px"><span class="f-lab" style="font-size:10.5px">{c}</span>' + ''.join(f'<div style="background:#fff;padding:12px 13px;display:flex;flex-direction:column;gap:3px"><span style="font-size:14.5px;font-weight:500;color:#0c1a2e">{n}</span><span style="font-size:12.5px;color:#6b7280">{d}</span></div>' for n, d in cs) + '</div>' for c, cs in cols)
    matches = ''.join(f'<div class="f-row" style="padding:14px 16px;align-items:center;gap:12px"><span style="display:flex;flex-direction:column;gap:3px"><b style="font-size:15px;font-weight:500;color:#0c1a2e">{n}</b><span style="font-size:13px;color:#6b7280">{d}</span></span><span style="font-size:13px;color:#1c547d;border:1px solid #c9d6e8;padding:5px 9px;white-space:nowrap">+ Add to pipeline</span></div>' for n, d in [('Seed-stage fintech fund', 'Your stage · Your sector · Invests in your country'), ('Accelerator programme', 'Pre-seed and seed · Applications open'), ('Non-dilutive grant', 'Matches your sector and location')])
    return f'''<main>
<section class="f-sec" style="padding:96px 0 72px"><div class="f-w f-g" style="align-items:center;gap:48px">
  <div class="s6 f-herocol"><p class="f-lab">For startups raising</p><h1 class="f-h1" style="color:#0c1a2e">Run the round. <span class="f-em">Not the admin.</span></h1>
    <p class="f-sub" style="font-size:20px;max-width:500px">Find the right investors, see who is interested and close on SAFEs, from one workspace.</p>
    <div class="f-acts"><a class="f-btn dk" href="{APP}/start">Start free for 14 days →</a><a class="f-btn gh" href="/pricing/">See pricing</a></div>
    <div style="display:flex;gap:22px;flex-wrap:wrap;font-size:14px;color:#4a515c"><span>✓ Investor and grant finder</span><span>✓ Deck analytics</span><span>✓ SAFEs and cap table</span></div></div>
  <div class="s6 f-pale" style="position:relative;min-height:520px;overflow:hidden" aria-hidden="true"><div class="f-gridbg dk"></div>
    <div style="position:absolute;z-index:2;left:6%;top:7%;width:56%;background:#fff;padding:22px;display:flex;flex-direction:column;gap:12px;box-shadow:0 24px 60px rgba(12,26,46,.14)"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:14px;color:#6b7280">Seed round · SAFE</span><span style="font-size:12px;color:#1c547d;background:#e6eef6;padding:3px 7px">Open</span></div>
      <span style="font-size:22px;font-weight:500;color:#0c1a2e">$1.9M committed of $2.5M</span><div style="height:8px;background:#e6eef6"><div class="f-grow" style="width:76%;height:8px;background:#2f6fb3"></div></div>
      <div style="display:flex;gap:6px;align-items:center"><span style="width:26px;height:26px;background:#0c1a2e"></span><span style="width:26px;height:26px;background:#2f6fb3"></span><span style="width:26px;height:26px;background:#9fc0e4"></span><span style="font-size:13px;color:#6b7280;margin-left:4px">8 investors committed</span></div></div>
    <div class="f-colmac">{mac(('fundraising', 'contacts'))}</div>
    <div style="position:absolute;z-index:2;left:4%;bottom:8%;width:52%;background:#fff;padding:14px 16px;display:flex;gap:12px;align-items:center;box-shadow:0 18px 44px rgba(12,26,46,.14)"><span class="f-dot" style="width:8px;height:8px;background:#2f6fb3;flex:none"></span><span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:14.5px;font-weight:500;color:#0c1a2e">Growth fund opened the data room</b><span style="font-size:12.5px;color:#6b7280">Financials folder · 2 minutes ago</span></span></div>
  </div>
</div></section>

<section class="f-inset"><div class="f-box f-navy"><div class="f-wi" style="padding-top:96px;padding-bottom:96px">
  <div class="f-split"><div><p class="f-lab">Pipeline</p><h2 class="f-h2" style="font-size:52px">Every investor, <span class="f-emd">one pipeline.</span></h2></div><p class="f-sub" style="font-size:17px">Stages, notes and next steps for each investor, with opens and replies logged for you.</p></div>
  <div style="overflow-x:auto"><div style="min-width:860px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">{board}</div></div>
</div></div></section>

<section class="f-sec"><div class="f-w f-g" style="gap:14px">
  <div class="s7 f-bt"><p class="f-lab">Investor and grant finder</p><h2 class="f-h3" style="color:#0c1a2e">Find investors and grants <span class="f-em">that fit.</span></h2><p class="f-sub" style="font-size:16px">Matched to your location, stage, sector and raise. One click adds them to your pipeline.</p><div style="display:flex;flex-direction:column;gap:8px">{matches}</div></div>
  <div class="s5 f-navy" style="padding:32px;display:flex;flex-direction:column;gap:22px"><p class="f-lab">Signals</p><h2 class="f-h3">Signals, <span class="f-emd">not guesses.</span></h2><p class="f-sub" style="font-size:16px">Time per slide, repeat visits and data room downloads.</p>
    <div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid #24364f;padding-top:16px;font-size:14px;color:#c3d1e4"><span>Data room views this week</span><b style="font-weight:500;color:#fff;display:flex;gap:8px;align-items:center"><span class="f-dot" style="width:6px;height:6px"></span>48 · 12 today</b></div>
    <div class="f-bars" style="height:120px;margin-top:auto" data-live="bars" data-low="35">{sl}</div><span style="font-size:12.5px;color:#8ea3bf">Time spent per slide, slides 1 to 10</span></div>
  <div class="s5 f-bt"><p class="f-lab">SAFEs</p><h2 class="f-h3" style="color:#0c1a2e">SAFEs <span class="f-em">in minutes.</span></h2><p class="f-sub" style="font-size:16px">Post-money SAFEs with MFN and pro rata side letters, filed and added to the cap table.</p>
    <div class="f-wht" style="padding:20px;gap:12px;box-shadow:0 10px 30px rgba(12,26,46,.08)"><div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:15px;color:#0c1a2e">Post-money SAFE</b><span style="font-size:12.5px;color:#1c547d;background:#e6eef6;padding:4px 8px">Signed</span></div>
      <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;font-size:14px"><span style="display:flex;flex-direction:column;gap:2px"><span style="color:#6b7280;font-size:12.5px">Purchase amount</span>$500,000</span><span style="display:flex;flex-direction:column;gap:2px"><span style="color:#6b7280;font-size:12.5px">Valuation cap</span>$12,000,000</span></div>
      <div style="display:flex;gap:6px;flex-wrap:wrap"><span style="font-size:12.5px;border:1px solid #d5d9e0;padding:4px 8px">MFN</span><span style="font-size:12.5px;border:1px solid #d5d9e0;padding:4px 8px">Pro rata side letter</span><span style="font-size:12.5px;border:1px solid #d5d9e0;padding:4px 8px">Filed to data room</span></div></div></div>
  <div class="s7 f-bt"><p class="f-lab">Cap table</p><h2 class="f-h3" style="color:#0c1a2e">Model the next round <span class="f-em">before you sign.</span></h2><p class="f-sub" style="font-size:16px">Import your cap table or another tool's export. Grants, consents and certificates, e-signed.</p>
    <div class="f-tiledev" style="max-width:560px">{ipad(('model', 'captable'))}</div></div>
</div></section>
</main>''' + CTA('Spend the raise', 'in the right meetings.') + FOOT()


# ---------------------------------------------------------------- about

def about():
    A = [('Runway', '21 months', 'From your books'), ('Seed round', '$1.9M of $2.5M', 'Pipeline'), ('Update', 'Opened by 36 of 42', 'September'), ('Due next', 'Delaware franchise tax', 'Reminder set')]
    B = [('Deck v5', '31 readers this week', 'Time per slide'), ('Data room', 'Invite only', 'NDA signed'), ('Cap table', 'SAFEs converted', 'After the round'), ('Finvry AI', 'Draft ready', 'For your edit')]
    col = lambda xs: ''.join(f'<div class="f-gl"><span>{l}</span><b>{v}</b><em>{s}</em></div>' for l, v, s in xs * 2)
    prod = f'''<section class="f-inset ab2-prod"><div class="f-box f-navy"><div class="f-gridbg"></div><div class="ab2-dev">{mac(('dashboard', 'captable', 'financials'))}</div></div></section>'''
    return f'''<main>
<section class="f-inset" style="padding-top:6px"><div class="f-box f-navy">
  <video class="f-vid" autoplay muted loop playsinline preload="metadata" aria-hidden="true"><source src="https://pub-f138f42d66b748108ebf7432c7314665.r2.dev/iStock-1702872444.mp4" type="video/mp4"></video><div class="f-scrim"></div>
  <div class="f-hero f-g" style="padding-top:0;padding-bottom:0;align-items:center;min-height:560px">
  <div class="s6 f-herocol" style="padding:110px 0"><p class="f-lab">About Finvry</p><h1 class="f-h1 ab-h1"><span class="l1">Investor relations,</span> <span class="f-emd">made simple.</span></h1><p class="f-sub" style="font-size:19px;max-width:480px">Built by operators who report to investors themselves.</p></div>
  <div class="s6 f-hide-m f-scroll1" aria-hidden="true"><div class="f-down">{col(B)}</div></div>
</div></div></section>
<section class="f-sec ab-sec"><div class="f-w">
  <div class="ab-lead"><div><p class="f-lab">Why we built it</p><h2>Founders were rebuilding the same spreadsheet <span class="f-em">every month.</span></h2></div>
    <p>We started Finvry so the numbers, the raise and the paperwork keep themselves current, and investors get better updates.</p></div>
</div></section>
<section class="ab2-how"><div class="ab2-grid">
  <div class="ab2-c"><p class="f-lab">How we write</p><b>Plain language</b><span>No jargon, anywhere.</span></div>
  <div class="ab2-c"><p class="f-lab">Who owns us</p><b>Founder-owned</b><span>Profitable and independent.</span></div>
  <div class="ab2-c"><p class="f-lab">Who answers</p><b>Answered by us</b><span>Every message, by the team.</span></div>
  <div class="ab2-c"><p class="f-lab">Headquarters</p><b>San Jose, California</b><span>6472 Camden Ave, Suite 204</span></div>
  <div class="ab2-c"><p class="f-lab">Talk to us</p><a href="mailto:support@finvry.com">support@finvry.com</a><span><a class="st" href="{APP}/status"><i class="f-dot" style="background:#2f6fb3"></i>System status</a></span></div>
  <div class="ab2-c dk"><p class="f-lab">Part of</p><b>TAGroup</b><span>Finvry is a TAGroup product.</span></div>
</div></section>
{prod}
</main>''' + CTA('Built by operators.', 'For founders.').replace('class="f-cta"', 'class="f-cta ab2-end"', 1) + FOOT()


# ---------------------------------------------------------------- partners hero (the list and form below keep their live scripts)

PARTNERS_HERO = f'''<!--fv-hero--><section class="f-inset" style="padding-top:6px"><div class="f-box f-navy">
  <video class="f-vid" autoplay muted loop playsinline preload="metadata" aria-hidden="true"><source src="https://pub-f138f42d66b748108ebf7432c7314665.r2.dev/iStock-2180538267.mp4" type="video/mp4"></video><div class="f-scrim"></div>
  <div class="f-hero f-g" style="align-items:center;padding-top:110px;padding-bottom:110px">
  <div class="s7 f-herocol"><p class="f-lab">Partner discounts</p><h1 class="f-h1">Startup discounts. <span class="f-emd">From the people who back you.</span></h1>
    <p class="f-sub" style="font-size:19px">VCs, incubators, accelerators and communities give their founders a Finvry discount. A partner code also skips the access queue.</p>
    <div class="f-acts"><a class="f-btn lt" href="#list">See partners</a><a class="f-btn ln" href="#apply">Become a partner</a></div></div>
  <div class="s5"><div style="max-width:360px;margin-left:auto;display:flex;flex-direction:column;gap:10px">
    <div style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);padding:18px;display:flex;flex-direction:column;gap:8px"><span class="f-lab" style="font-size:10.5px">Your partner code</span><b style="font-size:22px;font-weight:600;letter-spacing:.12em">PARTNER-CODE</b><span style="font-size:13px;color:#9fb2cc">From your VC, incubator or accelerator</span></div>
    <div style="background:#fff;padding:16px 18px;display:flex;justify-content:space-between;align-items:center"><span style="display:flex;flex-direction:column;gap:2px"><span style="font-size:13px;color:#6b7280">Plan</span><b style="font-size:15px;font-weight:500;color:#0c1a2e">Startup, with partner discount</b></span><span style="font-size:12.5px;background:#e6eef6;color:#1c547d;padding:4px 8px">Applied</span></div>
  </div></div>
</div></div></section><!--/fv-hero-->'''


# ---------------------------------------------------------------- assemble

import hashlib


def ver(name):
    return hashlib.sha1((ROOT / name).read_bytes()).hexdigest()[:8]


HEAD_ADD = '<link rel="stylesheet" href="/site.css">'
SCRIPT_ADD = '<script src="/site.js" defer></script>'


def versioned(s):
    """Add a content hash to the stylesheet and script links so browsers and the CDN fetch new copies after each deploy."""
    s = re.sub(r'href="(?:\.\./|/)?styles\.css(\?v=\w+)?"', f'href="/styles.css?v={ver("styles.css")}"', s)
    s = re.sub(r'href="/site\.css(\?v=\w+)?"', f'href="/site.css?v={ver("site.css")}"', s)
    return re.sub(r'src="/site\.js(\?v=\w+)?"', f'src="/site.js?v={ver("site.js")}"', s)


STALE = (r'<script>window\.__FV_POOL.*?</script>\s*', r'<script>\s*\(\(\) => \{.*?\}\)\(\)\s*</script>\s*')


def clean(tail):
    """Drop the old page animations and video shuffle; the live-data and cookie scripts stay."""
    for pat in STALE:
        tail = re.sub(pat, '', tail, flags=re.S)
    return tail


def splice(path, body, keep=None):
    """Replace <body> .. end of old footer with `body`; keep the head and the scripts after the footer."""
    s = path.read_text()
    if '/site.css' not in s:
        s = s.replace('</head>', HEAD_ADD + '\n' + SCRIPT_ADD + '\n</head>', 1)
    s = versioned(s)
    s = re.sub(r'<html[^>]*>', '<html lang="en" style="zoom: .79;">', s, count=1)
    i = s.index('<body')
    j = s.index('>', i) + 1
    k = s.index('</footer>', j) + len('</footer>') if '</footer>' in s[j:] else None
    tail = clean(s[k:])
    s = s[:i] + '<body class="f">' + body + tail
    path.write_text(s)


def reskin(path, active, cta, cut=()):
    """Keep the page's own <main> (live pricing, comparison, partner list and form), swap header and footer."""
    s = path.read_text()
    if '/site.css' not in s:
        s = s.replace('</head>', HEAD_ADD + '\n' + SCRIPT_ADD + '\n</head>', 1)
    s = versioned(s)
    s = re.sub(r'<html[^>]*>', '<html lang="en" style="zoom: .79;">', s, count=1)
    i = s.index('<body'); j = s.index('>', i) + 1
    m0 = s.index('<main', j); m1 = s.index('</main>', m0) + len('</main>')
    main = s[m0:m1]
    for pat in cut:
        main = re.sub(pat, '', main, flags=re.S)
    k = s.index('</footer>', m1) + len('</footer>')
    s = s[:i] + '<body class="f">' + NAV(active) + main + cta + FOOT() + clean(s[k:])
    path.write_text(s)


if __name__ == '__main__':
    splice(ROOT / 'index.html', NAV('home') + home())
    splice(ROOT / 'founders/index.html', NAV('founders') + founders())
    splice(ROOT / 'finance-teams/index.html', NAV('finance') + finance())
    splice(ROOT / 'startups-raising/index.html', NAV('raising') + raising())
    splice(ROOT / 'about/index.html', NAV('about') + about())
    reskin(ROOT / 'pricing/index.html', 'pricing', CTA('Fourteen days free.', 'Then pick your plan.'), cut=(r'<section class="pcta">.*?</section>',))
    reskin(ROOT / 'compare/index.html', 'compare', CTA('Replace five tools', 'with one.'), cut=(r'<section class="close">.*?</section>',))
    reskin(ROOT / 'partners/index.html', '', CTA('Your partner code', 'skips the queue.'), cut=(r'<section class="close">.*?</section>', r'<section class="chero">.*?</section>', r'<!--fv-hero-->.*?<!--/fv-hero-->'))
    p = ROOT / 'partners/index.html'; s = p.read_text(); s = s.replace('<main>', '<main>' + PARTNERS_HERO, 1); p.write_text(s)
    print('built')
