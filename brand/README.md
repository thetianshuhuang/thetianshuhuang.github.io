# tianshu.io mark — duck riding the ramp

Everything here is generated from `source/params.json` by `source/generate.py`.
To revise the mark, change the numbers (ramp, duck position/size/tilt, stroke,
corner radius and smoothing, colours) and rebuild:

    pip install cairosvg pillow shapely
    python source/generate.py

## Folders

- `svg/` — editable masters, 100×100 viewBox
  - `mark-full` — primary mark, smooth (continuous-curvature) corners
  - `mark-small` — simplified for 16–32 px (heavier wave, slightly larger duck)
  - `mark-full-square` — full-bleed square; for platforms that round corners themselves
  - `mark-maskable` — square with the art inside the central 80% (Android safe zone)
  - `mark-notile-on-light` / `-on-dark` — no tile, eye knocked out
  - `mark-mono-dark` / `-light` — single colour
- `png/` — 1024 px renders of each master
- `web/` — what the site serves: `favicon.ico` (16/32/48), `icon.svg`,
  `apple-touch-icon.png` (180, square — iOS rounds it), `icon-192.png`,
  `icon-512.png`, `icon-maskable-512.png`, `manifest.webmanifest`, `head-snippet.html`
- `mkdocs/` — `logo.svg` for the header, `mkdocs-snippet.yml`, `overrides/main.html`
- `social/` — 1200×630 link-preview image (not used on the site)
- `preview.png` — contact sheet of the set

## Where it lives on the site

Only `svg/`, `source/` and `preview.png` are kept here; rebuilding also
recreates `png/`, `web/`, `mkdocs/` and `social/` in this folder. To update
the site after a rebuild, copy:

- `web/*` except `head-snippet.html` → `docs/` (served from the site root)
- `mkdocs/logo.svg` → `docs/assets/logo.svg` (header logo)

The `<head>` tags live in `overrides/main.html`; `theme.logo` and
`theme.favicon` are set in `mkdocs.yml`.

## Notes

- Favicon-size uses (`favicon.ico`, `icon.svg`, header logo) use the simplified small version.
- On light backgrounds the no-tile version uses a deeper gold (`wave_on_light`) so the wave stays visible on white.
- Colours: tile `#141A2E`, duck `#FFF8EE`, wave/beak `#F2B300`.
