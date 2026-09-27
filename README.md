# PFX Media — website

Single static page: `index.html` + `assets/`. No build step.

**Live:** https://pfxmedia.au (GitHub Pages, repo `Danielperri14/pfx-media-site`, branch `main`).
Pushing to `main` redeploys in about a minute. Preview locally with any static server that
supports range requests (e.g. `npx http-server -p 8765 -c-1`); plain `python -m http.server`
breaks video seeking.

**Domain:** pfxmedia.au, registered at VentraIP, DNS Hosting. Records: 4 × A to GitHub Pages
(185.199.108–111.153) and CNAME `www` → `danielperri14.github.io`. HTTPS enforced. The `CNAME`
file in the repo must stay.

**Contact:** pfxmedia1@gmail.com · Calendly https://calendly.com/pfxmedia1/30min ·
Instagram https://www.instagram.com/pfx.media/

## Work grid
Each tile in `#work` has: `href` (fallback link), `data-yt` (YouTube id) or `data-video`
(self-hosted mp4), `data-ratio` (the video's shape), `data-preview` (silent loop cut to the
tile's shape, in `assets/work/`) and `--ph` (poster = the loop's first frame). Bump the `?v=`
number when replacing a loop so browsers fetch the new one.

## Results
Screenshots in `assets/results/`, cropped to the stat cards. Keep the `width`/`height`
attributes on each `<img>` in step with the file, or the strip jumps while loading.

## Other
- `assets/share.jpg` is the link-preview image (1200×630); regenerate if the headline changes.
- `tools/portraits.py` rebuilds the team portraits from the PortableSSD studio shots.
- Logo: `assets/pfx-wordmark.png` is the transparent wordmark keyed out of `pfx-logo.png`
  (275px source, so a larger original would be sharper).
