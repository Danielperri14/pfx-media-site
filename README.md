# PFX Media — website

Single static page: `index.html` + `assets/`. No build step. Open `index.html` in a browser.

**Status (27 Sep 2026):** first version built from the positioning brief. Live hosting and domain not yet set up.

- Copy/structure: hero (30 days of content / one shoot), PFX Content Day offer, "Need something else?" secondary
  path, Two specialists (Felix + Daniel with portraits), Our work grid (7 PLACEHOLDER tiles), contact, footer.
- Contact: pfxmedia1@gmail.com. Booking buttons open Calendly popup: https://calendly.com/pfxmedia1/30min
- Portraits: `tools/portraits.py` rebuilds `assets/daniel.jpg` / `assets/felix.jpg` from the studio shots on the
  PortableSSD (`PB ALL Assets/PFP: Photos/Photos/`).
- Logo: `assets/pfx-logo.png` (275px badge) and `assets/pfx-wordmark.png` cropped from it. A larger file would be sharper.

**Still to do:** replace the 7 work tiles (poster frame + link + client name each; set `--ph` to the poster and the
`href` to the video), choose hosting (NOT Phillip's Vercel team — PFX is separate from BNB), buy a domain
(pfxmedia.com / .com.au / pfx.media are taken; pfxmedia.co ≈ US$30/yr and pfxmedia.au were available on 27 Sep 2026).
