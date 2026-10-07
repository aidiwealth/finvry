R2 = 'https://pub-f138f42d66b748108ebf7432c7314665.r2.dev/'
HEAD = lambda title, desc, r='': f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta name="theme-color" content="#0c1a2e">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}styles.css">
</head>
<body>'''
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" fill="currentColor"/><path d="M20 14h26v7H28v8h15v7H28v14h-8z" fill="#0c1a2e" style="fill:var(--logo-ink,#0c1a2e)"/><rect x="44" y="43" width="7" height="7" fill="#5fa8d3"/></svg>'
def NAV(solid=False, r=''):
    btn = 'dark' if solid else 'light'
    return f'''<header class="hd{' solid' if solid else ''}"><div class="w">
  <a class="brand" href="{r}index.html" style="--logo-ink:{'#fff' if solid else '#0c1a2e'}">{LOGO}Finvry</a>
  <nav class="menu" aria-label="Main"><a href="{r}index.html#product">Product</a><a href="{r}pricing/index.html">Pricing</a><a href="https://app.finvry.com/developers">API</a><a href="https://app.finvry.com/login">Sign in</a><a class="btn {btn}" href="https://app.finvry.com/start">Start free</a></nav>
</div></header>'''
def FOOT(r=''): return f'''<footer class="ft"><div class="w">
  <div><a class="brand" href="{r}index.html" style="--logo-ink:#0c1a2e">{LOGO}Finvry</a><p style="max-width:320px;margin:0">The OS for every founder: investor metrics, fundraising, requirements and engagement in one place.</p></div>
  <div><h4>Product</h4><a href="{r}index.html#product">Overview</a><a href="{r}pricing/index.html">Pricing</a><a href="https://app.finvry.com/start">Start free</a><a href="https://app.finvry.com/login">Sign in</a></div>
  <div><h4>Developers</h4><a href="https://app.finvry.com/developers">API documentation</a><a href="https://app.finvry.com/status">Status</a></div>
  <div><h4>Legal</h4><a href="https://app.finvry.com/legal/terms">Terms</a><a href="https://app.finvry.com/legal/privacy">Privacy</a><a href="mailto:hello@finvry.com">Contact</a></div>
  <div class="legal"><span>&copy; <span class="yr">2026</span> Finvry. All rights reserved.</span><span>Finvry provides software. It does not provide legal, tax or investment advice.</span></div>
</div></footer>'''
