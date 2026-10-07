# finvry.com

Marketing site for Finvry: the home page (`index.html`) and pricing (`pricing/index.html`), sharing `styles.css`.
Plain HTML and CSS, no build step needed (`build.py` regenerates both pages from `_parts.py` if you prefer editing there).

- Typeface: Instrument Sans, the same as app.finvry.com. Square corners throughout.
- Videos are the ones used on theaidigroup.com (R2 links in `build.py`/`index.html`); replace them with Finvry clips when ready.
- Links: app sign-in and sign-up, API docs (app.finvry.com/developers), status (app.finvry.com/status), terms and privacy.
- Deploys to DigitalOcean App Platform as a static site (`.do/app.yaml`) on every push to `main`.
