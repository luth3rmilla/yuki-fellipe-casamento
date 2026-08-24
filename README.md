# Yuki & Fellipe — Wedding Website

Elegant multilingual wedding site (Portuguese · English · 中文).

**Date:** 3 October 2026 · **Venue:** Catembe Gallery Hotel, Maputo

## Local preview

Open `index.html` in a browser, or from this folder:

```bash
npx --yes serve .
```

## RSVP → Excel email every 15 days

Confirmations are sent to a Google Sheet. Every 15 days an Excel file is emailed to **fellipe.theodoro@yahoo.com**.

1. Create a Google Sheet named `Yuki-Fellipe-RSVPs`
2. **Extensions → Apps Script** → paste `scripts/rsvp-apps-script.gs` → Save
3. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Copy the Web App URL into `js/main.js`:

```js
const RSVP_ENDPOINT = "https://script.google.com/macros/s/XXXX/exec";
```

5. In the Apps Script editor, run **`setupTriggerOnce`** once (authorize when asked)

Until the endpoint is set, RSVPs are still saved in the guest’s browser (and the form shows success).

## Special phrases

Edit the bride/groom dedication texts in `js/i18n.js` under `bridePhrase` and `groomPhrase` for `pt`, `en`, and `zh`.

## Deploy on GitHub Pages

```bash
git init
git add .
git commit -m "Add Yuki & Fellipe wedding website"
gh repo create yuki-fellipe-casamento --public --source=. --remote=origin --push
```

Then: **Settings → Pages → Deploy from branch → `main` / root (or `/docs`)**.

Site URL will be: `https://<username>.github.io/yuki-fellipe-casamento/`

## Music

Background track: *Just the Two of Us* (instrumental) — play/pause control in the header.
Browsers often block autoplay until the guest taps the music button.