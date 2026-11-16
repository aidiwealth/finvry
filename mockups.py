"""Finvry app screens for the marketing site, drawn in HTML inside a laptop or tablet frame.

Every name and number here is invented sample data (the company is "Kestrel Labs"); none of it comes from a real
workspace. The screens follow the app's own layout: sidebar, breadcrumb bar, page tabs, cards and charts.
"""
import math

def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def ic(d, w=20):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" aria-hidden="true"><path d="{d}" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'


P = {
    'dash': 'M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z', 'inv': 'M4 19l5-6 4 3 7-9M4 21h16',
    'cap': 'M12 3a9 9 0 1 0 9 9h-9zM14 3.3A9 9 0 0 1 20.7 10H14z', 'boards': 'M3 12h4l2-5 4 10 2-5h6',
    'stage': 'M5 18a7 7 0 1 1 14 0M12 18l3-5', 'fin': 'M5 20V12M10 20V8M15 20v-6M20 20V5M3 20h18',
    'bank': 'M3 10l9-6 9 6M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18', 'docs': 'M7 3h7l5 5v13H7zM14 3v5h5',
    'comp': 'M4 6h16v14H4zM4 10h16M9 3v4M15 3v4M9 15l2 2 4-4', 'svc': 'M4 8h16v11H4zM9 8V5h6v3M4 13h16',
    'set': 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19 12a7 7 0 0 0-.1-1.2l2-1.5-2-3.4-2.3.9a7 7 0 0 0-2.1-1.2L14 3h-4l-.5 2.6a7 7 0 0 0-2.1 1.2l-2.3-.9-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.5 2 3.4 2.3-.9a7 7 0 0 0 2.1 1.2L10 21h4l.5-2.6a7 7 0 0 0 2.1-1.2l2.3.9 2-3.4-2-1.5c.1-.4.1-.8.1-1.2z',
    'help': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM6 6l3.5 3.5M14.5 14.5 18 18M18 6l-3.5 3.5M9.5 14.5 6 18',
    'out': 'M9 4H5v16h4M16 8l4 4-4 4M20 12H10', 'money': 'M3 7h18v10H3zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 10v4M18 10v4',
    'bars': 'M6 19V13M11 19V9M16 19v-4M4 21h16', 'receipt': 'M7 3h10v18l-2-1.5L13 21l-1-1-1 1-2-1.5L7 21zM10 8h4M10 12h4M10 16h2',
    'flag': 'M6 21V4M6 4h11l-2 4 2 4H6', 'people': 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM3 20c0-3 2.7-5 6-5s6 2 6 5M16 11a3 3 0 1 0 0-6M18 15c2 .6 3 2.3 3 5',
    'file': 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6', 'clock': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2',
    'upload': 'M12 16V4M7 9l5-5 5 5M4 20h16', 'spark': 'M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z',
    'down': 'M6 9l6 6 6-6', 'refresh': 'M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7',
}

NAV = [(None, [('dash', 'Dashboard')]), ('Investors', [('inv', 'Investors'), ('cap', 'Cap table'), ('boards', 'Boards'), ('stage', 'Stage monitor')]),
       ('Money', [('fin', 'Financials'), ('bank', 'Banking')]), ('Company', [('docs', 'Documents'), ('comp', 'Compliance'), ('svc', 'Services')]),
       ('Administration', [('set', 'Settings'), ('help', 'Help & support')])]


def shell(active, crumb, body, compact=False):
    side = ''
    for group, items in NAV:
        if group and not compact:
            side += f'<p class="ap-grp">{group}</p>'
        elif group:
            side += '<span class="ap-sep"></span>'
        for key, label in items:
            side += f'<span class="ap-nv{" on" if label == active else ""}">{ic(P[key])}{"" if compact else "<span>" + label + "</span>"}</span>'
    logo = '<img src="/finvry-mark.svg" alt="" class="ap-mark">' if compact else '<img src="/finvry-logo.svg" alt="" class="ap-logo">'
    user = '<span class="ap-me"><b>A</b></span>' if compact else '<span class="ap-me"><b>A</b><span>amara@kestrellabs.co</span></span><span class="ap-nv">' + ic(P['out']) + '<span>Sign out</span></span>'
    a, b = crumb
    return f'''<div class="ap{' ap-c' if compact else ''}" aria-hidden="true"><aside class="ap-side">{logo}<nav>{side}</nav><div class="ap-foot">{user}</div></aside>
<div class="ap-main"><div class="ap-top"><span class="ap-crumb"><span>{a}</span><i>/</i><b>{b}</b></span><span class="ap-org"><b>K</b><span><strong>Kestrel Labs</strong><em>Scale</em></span></span></div>
<div class="ap-body">{body}</div></div><span class="ap-ai">{ic(P['spark'], 22)}</span></div>'''


def tabs(items, on, cls='ap-tabs'):
    return f'<div class="{cls}">' + ''.join(f'<span{" class=on" if t == on else ""}>{t}</span>' for t in items) + '</div>'


def kpi(label, value, sub='', icon=None, cls='', vcls=''):
    i = f'<span class="ap-ki">{ic(P[icon], 22)}</span>' if icon else ''
    return f'<div class="ap-kpi {cls}">{i}<span><em>{label}</em><b class="{vcls}">{value}</b>{f"<small>{sub}</small>" if sub else ""}</span></div>'


def area(vals, w=520, h=190, color='#2f6fb3'):
    lo, hi = min(vals), max(vals)
    pts = [(i * w / (len(vals) - 1), h - 8 - (v - lo) / ((hi - lo) or 1) * (h - 30)) for i, v in enumerate(vals)]
    line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    gid = 'g' + str(abs(hash((tuple(vals), color))) % 99999)
    return f'''<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" class="ap-svg"><defs><linearGradient id="{gid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>
<polygon points="0,{h} {line} {w},{h}" fill="url(#{gid})"/><polyline points="{line}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linejoin="round"/></svg>'''


def pnl(vals, w=520, h=190):
    m = max(abs(v) for v in vals); zero = h * 0.62; bw = w / len(vals)
    out = ''
    for i, v in enumerate(vals):
        bh = abs(v) / m * (zero - 10 if v > 0 else h - zero - 6)
        y = zero - bh if v > 0 else zero
        out += f'<rect x="{i * bw + bw * .2:.1f}" y="{y:.1f}" width="{bw * .6:.1f}" height="{bh:.1f}" fill="{"#273449" if v > 0 else "#c0504d"}"/>'
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" class="ap-svg">{out}<line x1="0" x2="{w}" y1="{zero}" y2="{zero}" stroke="#c9ced8" stroke-dasharray="4 4"/></svg>'


def donut(parts, big, small, size=170):
    r = 62; c = 2 * math.pi * r; off = 0; segs = ''
    for pct, col in parts:
        segs += f'<circle cx="85" cy="85" r="{r}" fill="none" stroke="{col}" stroke-width="22" stroke-dasharray="{c * pct / 100:.2f} {c:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 85 85)"/>'
        off += c * pct / 100
    return f'<span class="ap-donut" style="width:{size}px;height:{size}px"><svg viewBox="0 0 170 170">{segs}</svg><span><b>{big}</b><em>{small}</em></span></span>'


def legend(rows):
    return '<div class="ap-leg">' + ''.join(f'<span><i style="background:{c}"></i>{l}<b>{v}</b></span>' for l, v, c in rows) + '</div>'


# ---------------------------------------------------------------- screens (sample company: Kestrel Labs)

def s_dashboard(compact=False):
    acct = [('Operating', 'checking', '4821', '$1,204,330.12'), ('Treasury', 'checking', '7710', '$612,000.00'), ('Payroll', 'checking', '3305', '$98,442.70'), ('Reserve', 'savings', '9052', '$45,118.04')]
    cards = ''.join(f'<div class="ap-acct"><span><b>BANK</b><em>·· {n}</em></span><span class="nm">{a} <i>{t}</i></span><strong>{v}</strong></div>' for a, t, n, v in (acct[:3] if compact else acct))
    body = f'''<p class="ap-k">Kestrel Labs</p><div class="ap-hrow"><h1>Good morning, Amara</h1><span class="ap-btns"><span class="ap-b dk">Add financials</span><span class="ap-b">Order a service</span></span></div>
<p class="ap-sub">2 companies consolidated in USD</p>
<div class="ap-kpis">{kpi('Revenue · Sept 26', '$312k', '<span class="up">▲ 4.2% vs last month</span>', 'money')}{kpi('Net income', '$18.4k', 'Gross margin 61%', 'bars')}{kpi('Cash', '$2.4M', 'incl. $400k treasury bills · 28 months runway', 'receipt')}{kpi('Monthly burn', '$86k', '3-month average', 'flag')}</div>
<p class="ap-lnk">Charts and statements in Financials →</p>
<div class="ap-card ap-banks"><div class="ap-bh"><span class="ap-live">LIVE</span><b>Bank balances</b><strong>$1,959,890.86</strong><em>4 accounts · updated 12 min ago</em><span class="ap-b sm">+ Add bank</span></div><div class="ap-accts">{cards}</div></div>
<div class="ap-g2"><div class="ap-card"><h3>Investors</h3><div class="ap-rows"><span>Investor page<b>Live</b></span><span>Investor page views<b>342</b></span><span>Active share links<b>3 · 41 views</b></span></div><p class="ap-lnk">Edit your investor page →</p></div>
<div class="ap-card"><h3>Coming up</h3><div class="ap-rows"><span>Delaware franchise tax<b class="bl">Mar 1</b></span><span>Q4 investor update<b class="bl">Jan 10</b></span><span>Open service requests<b>1</b></span></div><p class="ap-lnk">Compliance →</p></div></div>'''
    return shell('Dashboard', ('Kestrel Labs', 'Dashboard'), body, compact)


def s_financials(compact=False):
    rev = [180, 186, 179, 195, 204, 199, 214, 226, 221, 238, 245, 252, 249, 263, 271, 268, 284, 291, 288, 299, 312]
    pl = [-14, -11, -16, -8, -5, -9, 3, -2, 6, 4, -3, 8, 11, 7, 12, -4, 9, 14, 13, 16, 18]
    cash = [1.6, 1.58, 1.55, 1.9, 1.86, 1.83, 1.8, 1.78, 2.3, 2.27, 2.25, 2.24, 2.22, 2.25, 2.28, 2.3, 2.33, 2.35, 2.37, 2.39, 2.4]
    body = f'''<div class="ap-hrow"><h1>Kestrel Labs Inc <span class="ap-dd">{ic(P['down'], 22)}</span></h1></div><p class="ap-sub">Parent company · USD</p>
{tabs(['Overview', 'Statements', 'Sharing', 'Revenue retention', 'Customers', 'Forecast', 'What to do next', 'Reports'], 'Overview')}
<div class="ap-seg"><span class="on">Monthly</span><span>Quarterly</span><span>Yearly</span><span>Custom</span></div><span class="ap-b dk" style="margin-left:12px">Add figures</span>
<div class="ap-card ap-sheet"><span><b>Linked sheets</b><em>Kept in sync automatically.</em></span><span class="row"><span><b>Kestrel Financials</b><em>Tab P&amp;L · USD · 48 rows · synced 2 min ago</em></span><span class="ap-lk">Sync now · Edit</span></span></div>
<div class="ap-kpis">{kpi('Revenue · Sept 26', '$312k', '<span class="up">▲ 4.2% vs previous</span>', 'money')}{kpi('Net income', '$18.4k', 'EBITDA $26.1k', 'bars')}{kpi('Cash', '$2.4M', 'Cash-flow positive', 'receipt')}{kpi('Gross margin', '61%', 'Burn $86k / month (3-month average)', 'bars')}</div>
<div class="ap-g3"><div class="ap-card ap-ch"><h3>Revenue</h3>{area(rev)}<span class="ap-ax"><span>Jan 25</span><span>Sept 26</span></span><span class="ap-cf"><span>21 periods</span><b>$312k</b></span></div>
<div class="ap-card ap-ch"><h3>Profit and loss <em>13 up, 8 down</em></h3>{pnl(pl)}<span class="ap-ax"><span>Jan 25</span><span>Sept 26</span></span><span class="ap-cf"><span>Net income after all costs</span><b>$18.4k</b></span></div>
<div class="ap-card ap-ch"><h3>Cash</h3>{area(cash)}<span class="ap-ax"><span>Jan 25</span><span>Sept 26</span></span><span class="ap-cf"><span>At Sept 26</span><b>$2.4M</b></span></div></div>'''
    return shell('Financials', ('Money', 'Financials'), body, compact)


def s_stage(compact=False):
    n = 34; bars = ''; w = 1000; h = 300; bw = w / n
    pts = []
    for i in range(n):
        f = i >= 12
        r = 120 + i * 9 + (i ** 1.6 if f else 0) + (6 if i % 3 == 0 else 0)
        c = 150 + i * 3.2 + (4 if i % 2 else 0)
        rh, chh = r / 520 * h, c / 520 * h
        bars += f'<rect x="{i * bw + bw * .1:.1f}" y="{h - rh:.1f}" width="{bw * .38:.1f}" height="{rh:.1f}" fill="{"#5b7fa8" if f else "#13243b"}"/>'
        bars += f'<rect x="{i * bw + bw * .5:.1f}" y="{h - chh:.1f}" width="{bw * .38:.1f}" height="{chh:.1f}" fill="{"#d9dee6" if f else "#a9b3c1"}"/>'
        cash = 40 + (0 if i < 14 else (i - 14) ** 1.75 * 1.5)
        pts.append(f'{i * bw + bw / 2:.1f},{h - cash:.1f}')
    chart = f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" class="ap-svg" style="height:300px"><rect x="{12 * bw}" y="0" width="{w - 12 * bw}" height="{h}" fill="#f4f6f9"/><line x1="{12 * bw}" x2="{12 * bw}" y1="0" y2="{h}" stroke="#9aa4b2" stroke-dasharray="3 4"/>{bars}<polyline points="{" ".join(pts)}" fill="none" stroke="#2f6fb3" stroke-width="2.6"/></svg>'
    body = f'''<div class="ap-hrow"><h1>Kestrel Group <span class="ap-dd">{ic(P['down'], 22)}</span></h1><span class="ap-b">Refresh</span></div>
<p class="ap-sub">Stage monitor · Consolidated · USD · 2 companies<br>Where Kestrel Group stands today, as of Sept 2026.</p>
<div class="ap-kpis">{kpi('Funding stage', 'Seed', 'About $3.2M raised')}{kpi('Revenue stage', 'Growing', '$3.7M a year · Typical of Seed to Series A')}{kpi('Health', 'Default alive')}{kpi('Runway', '28 months', 'Cash runs out Jan 2029')}</div>
<div class="ap-note"><b>Default alive.</b> At today's growth and spending, revenue overtakes costs before the cash runs out, in about Apr 2027.</div>
<div class="ap-card"><div class="ap-hrow"><h3>Default alive?</h3><em class="ap-mute">Last 12 months, then the 3-month trend</em></div>
<div class="ap-lg2"><span><i style="background:#13243b"></i>Revenue</span><span><i style="background:#a9b3c1"></i>Costs</span><span><i class="ln"></i>Cash</span><span class="ap-mute">Actual | Forecast</span></div>{chart}
<span class="ap-ax"><span>Oct 25</span><span>Apr 26</span><span>Oct 26</span><span>Apr 27</span><span>Oct 27</span><span>Apr 28</span></span></div>'''
    return shell('Stage monitor', ('Investors', 'Stage monitor'), body, compact)


def cap_head(sub_on):
    return f'''{tabs(['Investor updates', 'Investor page', 'Forecast', 'Cap table'], 'Cap table')}
<div class="ap-hrow"><span><h1>Cap table</h1><p class="ap-sub">Shares, options, SAFEs and notes for Kestrel Labs.</p></span><span class="ap-btns"><span class="ap-b">Share</span><span class="ap-b">Actions ⌄</span><span class="ap-b dk">Issue shares</span></span></div>
{tabs(['Overview', 'Shareholders', 'Options', 'SAFEs & notes', 'Rights & positions', 'Signing', 'Model a round', 'Valuation', 'Exit'], sub_on, 'ap-tabs sm')}'''


def s_captable(compact=False):
    holders = [('Amara Okafor', 'Founder', '4,200,000', '—', 42.0), ('Daniel Reyes', 'Founder', '2,600,000', '—', 26.0), ('Harbor Lane Capital', 'Investor', '1,500,000', '—', 15.0), ('Meridian Seed Fund', 'Investor', '700,000', '—', 7.0)]
    rows = ''.join(f'<div class="ap-tr"><span><b>{n}</b><em>{r}</em></span><span>{c}</span><span>{o}</span><span class="bar"><i style="width:{p * 1.9:.0f}%"></i></span><span><b>{p:.2f}%</b></span></div>' for n, r, c, o, p in holders)
    body = cap_head('Overview') + f'''
<div class="ap-kpis">{kpi('Fully diluted shares', '10,000,000', 'Issued, options and the open pool')}{kpi('Shares issued', '9,000,000', '12 holders · 1 class')}{kpi('Option pool left', '420,000', '1,000,000 reserved · 580,000 granted')}{kpi('SAFEs and notes', '$1.9M', '8 outstanding · convert next round')}</div>
<div class="ap-g2 w"><div class="ap-card"><div class="ap-hrow"><h3>Ownership today</h3><em class="ap-mute">Fully diluted</em></div><div class="ap-dn">{donut([(68, '#0c1a2e'), (22, '#9db8d6'), (6, '#4a6f97'), (4, '#2c4e78')], '68%', 'founders')}{legend([('Founders', '68% · 6.8M', '#0c1a2e'), ('Investors', '22% · 2.2M', '#9db8d6'), ('Options', '6% · 580k', '#4a6f97'), ('Open pool', '4% · 420k', '#2c4e78')])}</div></div>
<div class="ap-card"><div class="ap-hrow"><h3>Once the SAFEs convert</h3><em class="ap-mute">At their caps</em></div><div class="ap-dn">{donut([(58.4, '#0c1a2e'), (37.1, '#9db8d6'), (4.5, '#dedede')], '58.4%', 'founders')}{legend([('Founders', '58.4%', '#0c1a2e'), ('Investors', '37.1%', '#9db8d6'), ('Others', '4.5%', '#dedede')])}</div><div class="ap-note sm">After conversion founders keep control. <span class="bl">See rights &amp; positions →</span></div></div></div>
<div class="ap-card ap-tbl"><div class="ap-hrow"><h3>Holders</h3><em class="ap-mute">Bars show each holder's share, fully diluted</em></div><div class="ap-tr th"><span>Holder</span><span>Common</span><span>Options</span><span>Share</span><span>% FD</span></div>{rows}</div>'''
    return shell('Cap table', ('Investors', 'Cap table'), body, compact)


def s_rights(compact=False):
    body = cap_head('Rights & positions') + f'''
<div class="ap-drop"><span><p class="ap-k bl">{ic(P['spark'], 16)} READ WITH AI</p><h2>Drop your side letters. We'll show what each investor can do.</h2><p>AI reads side letters, pro rata letters and investor rights agreements, lists each right in plain words and matches it to the holder. Nothing is saved until you confirm.</p>
<span class="ap-steps"><span><i>1</i>Upload</span><span><i>2</i>AI finds each right</span><span><i>3</i>You confirm, letters filed</span></span></span><span class="ap-dz">{ic(P['upload'], 30)}<b>Drop letters here</b><em>PDF or Word · several at once</em></span></div>
<div class="ap-g3"><div class="ap-card"><h3>Who controls the vote</h3><div class="ap-dn">{donut([(58.4, '#0c1a2e'), (37.1, '#9db8d6'), (4.5, '#dedede')], '58.4%', 'founders', 140)}{legend([('Founders', '58.4%', '#0c1a2e'), ('Investors', '37.1%', '#9db8d6'), ('Others', '4.5%', '#dedede')])}</div><p class="ap-p">Founders keep a majority once the SAFEs convert.</p></div>
<div class="ap-card"><h3>Rights you've granted</h3><div class="ap-dn">{donut([(42, '#9db8d6'), (32, '#2c4e78'), (13, '#b5532a'), (8, '#c9d3df'), (5, '#5d6470')], '24', 'rights', 140)}{legend([('Pro rata', '10', '#9db8d6'), ('Information rights', '8', '#2c4e78'), ('Protective provisions', '3', '#b5532a'), ('MFN', '2', '#c9d3df'), ('Board observer', '1', '#5d6470')])}</div><p class="ap-p">Held by 9 investors · 11 letters</p></div>
<div class="ap-card"><h3>What to watch</h3><div class="ap-w"><em>PRO RATA</em><span>10 investors can buy into the next round before new investors.</span></div><div class="ap-w warn"><em>CAN BLOCK</em><span>Protective provisions: Harbor Lane Capital.</span></div></div></div>'''
    return shell('Cap table', ('Investors', 'Cap table'), body, compact)


def s_model(compact=False):
    seg = [('#2c4e78', 20, 'New investors 20.0%'), ('#dedede', 10, 'Option pool 10.0%'), ('#9db8d6', 21.6, 'Earlier investors and SAFEs 21.6%'), ('#0c1a2e', 46.4, 'Founders 46.4%'), ('#4a6f97', 2, 'Advisors 2.0%')]
    before = [('#9db8d6', 22), ('#0c1a2e', 68), ('#4a6f97', 2), ('#dedede', 8)]
    bar = lambda s: ''.join(f'<i style="width:{p}%;background:{c}"></i>' for c, p, *_ in s)
    body = cap_head('Model a round') + f'''
<div class="ap-card ap-tint"><h3>Your next round</h3><div class="ap-in"><label>Pre-money valuation<span>12,000,000</span></label><label>Raising<span>3,000,000</span></label><label>Option pool after the round (%)<span>10</span></label><label>Lead investor<span>New investors</span></label></div></div>
<div class="ap-kpis">{kpi('Price per share', '$1.12')}{kpi('Post-money', '$15M')}{kpi('New investors get', '2,678,571', 'shares')}{kpi('Pool top-up', '612,000', 'Comes out of the pre-money')}</div>
<div class="ap-card"><h3>Before and after the round</h3><div class="ap-bb"><span>Before</span><span class="ap-stk">{bar(before)}</span><span>After</span><span class="ap-stk">{bar(seg)}</span></div>
<div class="ap-lg2">{''.join(f'<span><i style="background:{c}"></i>{l}</span>' for c, p, l in seg)}</div>
<div class="ap-note warm">Founders go from <b>68.0%</b> to about <b>46.4%</b>. Try a higher pre-money or a smaller pool to see the difference.</div></div>'''
    return shell('Cap table', ('Investors', 'Cap table'), body, compact)


def s_fundraising(compact=False):
    pipes = [('Seed Round', 'SAFE · $12,000,000 cap · close 31 Mar', 76, 0, '$1,900,000 committed of $2,500,000 · 76%', '5 in play', '$1,400,000 closed'),
             ('Angel Round', 'SAFE · $8,000,000 cap · closed', 100, 0, '$550,000 committed of $500,000 · 100%', '0 in play', '$550,000 closed'),
             ('Grant applications', 'Non-dilutive · close 30 Jun', 18, 12, '$90,000 committed of $500,000 · 18%', '3 in play', '$0 closed')]
    rows = ''.join(f'<div class="ap-pp"><span><b>{n}</b><em>{d}</em></span><span><span class="ap-pb"><i style="width:{p}%"></i><i class="lt" style="width:{q}%"></i></span><em>{t}</em></span><span class="r"><b>{a}</b><em>{c}</em></span></div>' for n, d, p, q, t, a, c in pipes)
    body = f'''{tabs(['Fundraising', 'Contacts', 'Updates', 'Investor page'], 'Fundraising')}
<div class="ap-hrow"><h1>Fundraising</h1><span class="ap-btns"><span class="ap-b">Share data room</span><span class="ap-b dk">Create a SAFE</span></span></div>
{tabs(['Overview', 'Pipelines', 'Find investors & grants', 'Data room', 'Deal memo', 'SAFEs', 'NDAs'], 'Overview', 'ap-tabs sm')}
<div class="ap-card ap-pipes"><div class="ap-hrow"><span><em class="ap-mute">3 pipelines</em><p class="ap-tot"><b>$2,540,000</b> committed of $3,500,000 · $1,950,000 closed</p></span><span class="ap-b">All pipelines</span></div>{rows}</div>
<div class="ap-kpis">{kpi('Investors in play', '8', '', 'people')}{kpi('Data room files', '64', '2 data rooms', 'file')}{kpi('Data room views', '212', '', 'bars')}{kpi('Time spent', '3 h 20 min', '', 'clock')}</div>
<div class="ap-g2 w"><div class="ap-card"><div class="ap-hrow"><h3>Recent data room activity</h3><em class="ap-mute">4 people this week</em></div><div class="ap-act"><span class="av">H</span><span><b>partner@harborlane.vc</b><em>Opened 14 files via Investor page · 22 min in total</em><span class="ap-files"><i>Financials 2026</i><i>Cap table</i><i>Deck v5</i></span></span><em>2 h ago</em></div></div>
<div class="ap-card"><h3>Next steps</h3><div class="ap-ns on"><b>Find investors and grants</b><em>Matched to your stage and sector</em></div><div class="ap-ns"><b>Send the Q3 update</b><em>Drafted from your numbers</em></div></div></div>'''
    return shell('Investors', ('Investors', 'Fundraising'), body, compact)


def s_contacts(compact=False):
    people = [('Nadia Brooks', 'nadia@harborlane.vc', 'Harbor Lane Capital', 'Partner', 'Board', '12 Nov 2026'), ('Theo Lindqvist', 'theo@meridianseed.com', 'Meridian Seed Fund', 'Principal', 'Board', '12 Nov 2026'),
              ('Priya Raman', 'priya@atlasangels.org', 'Atlas Angels', 'Lead', 'Investors', '10 Nov 2026'), ('Jonah Mercer', 'jonah@cobaltpartners.com', 'Cobalt Partners', 'Partner', 'Investors', '9 Nov 2026'),
              ('Lena Fischer', 'lena@northfieldvc.com', 'Northfield Ventures', 'Associate', 'Investors', '9 Nov 2026'), ('Marcus Hale', 'marcus@kestrellabs.co', 'Kestrel Labs', 'CFO', 'Executive', '8 Nov 2026'),
              ('Sofia Duarte', 'sofia@bluecrest.capital', 'Bluecrest Capital', 'Partner', 'Investors', '5 Nov 2026'), ('Ade Coker', 'ade@sunroute.vc', 'Sunroute Ventures', 'Analyst', 'Investors', '3 Nov 2026')]
    rows = ''.join(f'<div class="ap-cr"><i class="cb"></i><span class="who"><span class="av">{"".join(w[0] for w in n.split()[:2])}</span><span><b>{n}</b><em>{e}</em></span></span><span class="firm">{f}<em> · {t}</em></span><span><i class="ap-tag">{l}</i></span><span class="ap-mute">{d}</span><span><i class="ap-tag">Subscribed</i></span></div>' for n, e, f, t, l, d in people)
    body = f'''{tabs(['Fundraising', 'Contacts', 'Updates', 'Investor page'], 'Contacts')}
<div class="ap-hrow"><h1>Contacts</h1><span class="ap-btns"><span class="ap-search">Search name, email, firm or title</span><span class="ap-b">Import</span><span class="ap-b dk">New contact</span></span></div>
<div class="ap-chips"><span class="on">All contacts <em>48</em></span><span>Board <em>4</em></span><span>Executive <em>6</em></span><span>Investors <em>38</em></span><span class="add">+ New list</span></div>
<div class="ap-card ap-ctbl"><div class="ap-cr th"><i class="cb"></i><span>Contact</span><span>Firm</span><span>Lists</span><span>Last activity</span><span>Status</span></div>{rows}</div>'''
    return shell('Investors', ('Investors', 'Contacts'), body, compact)


SCREENS = {'dashboard': s_dashboard, 'financials': s_financials, 'stage': s_stage, 'captable': s_captable, 'rights': s_rights,
           'model': s_model, 'fundraising': s_fundraising, 'contacts': s_contacts}


def mac(screen):
    return f'<div class="dv-mac"><div class="dv-lid"><span class="dv-cam"></span><div class="dv-scr" data-w="1440" data-h="900"><div class="dv-in">{SCREENS[screen]()}</div></div></div><div class="dv-base"><i></i></div></div>'


def ipad(screen):
    return f'<div class="dv-ipad"><div class="dv-scr" data-w="1180" data-h="820"><div class="dv-in">{SCREENS[screen](compact=True)}</div></div></div>'


def stage(laptop, tablet, tablet_side='right'):
    """A laptop with a tablet overlapping one corner. The tablet hides on phones so the laptop stays readable."""
    return f'<div class="dv-stage {tablet_side}">{mac(laptop)}<div class="dv-tab">{ipad(tablet)}</div></div>'
