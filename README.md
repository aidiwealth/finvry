# finvry.com

Marketing site for Finvry. Plain HTML and CSS; each page is `<folder>/index.html`.

- `site.css` is the design system (classes start with `f-`), loaded after the older `styles.css`, which the Pricing, Compare and Partners sections still use.
- `site.js` runs the mobile menu, the hero AI demo, the "See it work" tabs and the API code tabs.
- `build.py` writes the shared header, closing banner and footer into every page, and the full body of Home, Founders, Startups raising, Finance teams and About. Run `python3 build.py` after editing it. Each page keeps its own `<head>` and the live-data scripts after the footer: country pricing and services (Pricing), perks (Founders), the partner list and form (Partners), and cookie consent.
- Typeface: Instrument Sans, as in app.finvry.com. Square corners, navy and blue, page zoom .82 (set on each page's <html> tag by build.py).
- Videos are on R2 (links in `build.py`); each clip is used once across the site.
- The integration logos are placeholders (`.f-logo`); swap in the real logos when ready.
- Deploys to DigitalOcean App Platform as a static site (`.do/app.yaml`) on every push to `main`.
