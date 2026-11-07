#!/usr/bin/env python3
"""
Build every logo / favicon asset for tianshu.io from params.json.

    pip install cairosvg pillow shapely
    python source/generate.py          # run from the package root

Outputs (relative to the package root):
    svg/      master SVGs (edit-friendly, 100x100 viewBox)
    png/      1024 px renders of each master
    web/      favicon.ico, icon.svg, apple-touch-icon.png, icon-192/512.png,
              icon-maskable-512.png, manifest.webmanifest, head-snippet.html
    mkdocs/   mkdocs.yml snippet, overrides/main.html, logo.svg
    social/   og-image.svg / og-image.png (1200x630)
    preview.png   contact sheet of everything above
"""
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = json.load(open(os.path.join(HERE, "params.json")))
C = P["colors"]


def f(v):
    """Compact number formatting for SVG."""
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------- geometry

def squircle_path(radius, smoothing, w=100.0):
    """Continuous-curvature rounded square (Figma corner-smoothing construction)."""
    budget = w / 2
    R = min(radius, budget)
    if R <= 0.01:
        return f"M0 0 H{f(w)} V{f(w)} H0 Z"
    s = min(smoothing, budget / R - 1)
    p = min((1 + smoothing) * R, budget)
    arc_measure = 90 * (1 - s)
    arc = math.sin(math.radians(arc_measure / 2)) * R * math.sqrt(2)
    alpha = (90 - arc_measure) / 2
    p34 = R * math.tan(math.radians(alpha / 2))
    beta = 45 * s
    c = p34 * math.cos(math.radians(beta))
    d = c * math.tan(math.radians(beta))
    b = (p - arc - c - d) / 3
    a = 2 * b
    A, AB, ABC, BC = f(a), f(a + b), f(a + b + c), f(b + c)
    Cc, D, ARC, RR = f(c), f(d), f(arc), f(R)
    return (
        f"M{f(w - p)} 0 "
        f"c{A} 0 {AB} 0 {ABC} {D} a{RR} {RR} 0 0 1 {ARC} {ARC} c{D} {Cc} {D} {BC} {D} {ABC} "
        f"L{f(w)} {f(w - p)} "
        f"c0 {A} 0 {AB} -{D} {ABC} a{RR} {RR} 0 0 1 -{ARC} {ARC} c-{Cc} {D} -{BC} {D} -{ABC} {D} "
        f"L{f(p)} {f(w)} "
        f"c-{A} 0 -{AB} 0 -{ABC} -{D} a{RR} {RR} 0 0 1 -{ARC} -{ARC} c-{D} -{Cc} -{D} -{BC} -{D} -{ABC} "
        f"L0 {f(p)} "
        f"c0 -{A} 0 -{AB} {D} -{ABC} a{RR} {RR} 0 0 1 {ARC} -{ARC} c{Cc} -{D} {BC} -{D} {ABC} -{D} Z"
    )


def scene(small):
    r, d = P["ramp"], P["duck"]
    x0, x1 = r["x_start"], r["x_end"]
    low, high, drop = r["low"], r["high"], r["drop_x"]
    slope = (high - low) / (drop - x0)
    pts = [(x0, low), (drop, high), (drop, low)]
    if r["after_drop"] and drop < x1 - 1:
        pts.append((x1, low + slope * (x1 - drop)))
    wave = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)

    # region above the waterline: the duck is clipped to it
    lx, ly = pts[-1]
    end_y = ly + slope * (110 - lx) if (r["after_drop"] and drop < x1 - 1) else ly
    line = [(-10, low)] + pts + [(110, end_y)]
    above = "M-10 -10 L110 -10 " + " ".join(f"L{f(x)} {f(y)}" for x, y in reversed(line)) + " Z"

    ang = math.atan(slope)
    px = x0 + d["along"] * (drop - x0)
    py = low + slope * (px - x0)
    cx = px + d["float_height"] * math.sin(ang)
    cy = py - d["float_height"] * math.cos(ang)
    rot = math.degrees(ang) * d["tilt"]
    adj = P["small_size_adjust"]
    size = d["size"] + (adj["size_add"] if small else 0)
    return dict(
        wave=wave,
        above=above,
        duck_t=f"translate({f(cx)} {f(cy)}) rotate({f(rot)}) scale({f(size)}) translate(-48 -66)",
        stroke=P["stroke"] * (adj["stroke_multiplier"] if small else 1),
        eye=adj["eye_radius"] if small else P["full_size_eye_radius"],
    )


def knockout_paths(eye_r):
    """Duck silhouette with the eye cut out, as plain SVG paths (no <mask> needed).
    Returns (body_path, beak_path) in the duck's local coordinates."""
    from shapely.geometry import Polygon, Point
    from shapely import affinity
    tail = Polygon([(14, 48), (34, 58), (30, 70)]).buffer(2, join_style="round", quad_segs=16)
    body = affinity.scale(Point(48, 66).buffer(1, quad_segs=64), 30, 17)
    head = Point(66, 40).buffer(15, quad_segs=64)
    beak = Polygon([(78, 35), (92, 41), (78, 47)]).buffer(1.5, join_style="round", quad_segs=16)
    eye = Point(70, 36).buffer(eye_r, quad_segs=32)
    silhouette = tail.union(body).union(head).difference(eye)
    beak_only = beak.difference(eye)

    def to_d(geom):
        polys = getattr(geom, "geoms", [geom])
        out = []
        for poly in polys:
            for ring in [poly.exterior, *poly.interiors]:
                xs = list(ring.coords)
                out.append("M" + " L".join(f"{f(x)} {f(y)}" for x, y in xs[:-1]) + " Z")
        return " ".join(out)
    return to_d(silhouette), to_d(beak_only)


# ---------------------------------------------------------------- SVG builder

def mark_svg(*, small=False, tile="squircle", duck=None, beak=None, wave=None,
             tile_color=None, knockout_eye=False, inset=1.0, size_px=None, uid="m"):
    """tile: 'squircle' | 'square' | None.  inset < 1 shrinks the artwork (maskable icons)."""
    s = scene(small)
    duck = duck or C["duck"]
    beak = beak or C["beak"]
    wave = wave or C["wave"]
    tile_color = tile_color or C["tile"]
    tile_d = squircle_path(P["corner"]["radius"], P["corner"]["smoothing"]) if tile == "squircle" \
        else "M0 0 H100 V100 H0 Z"

    defs = [f'<clipPath id="{uid}-water"><path d="{s["above"]}"/></clipPath>']
    if tile:
        defs.append(f'<clipPath id="{uid}-tile"><path d="{tile_d}"/></clipPath>')

    duck_parts = (
        f'<path d="M14 48 L34 58 L30 70 Z" fill="{duck}" stroke="{duck}" stroke-width="4" stroke-linejoin="round"/>'
        f'<ellipse cx="48" cy="66" rx="30" ry="17" fill="{duck}"/>'
        f'<circle cx="66" cy="40" r="15" fill="{duck}"/>'
        f'<path d="M78 35 L92 41 L78 47 Z" fill="{beak}" stroke="{beak}" stroke-width="3" stroke-linejoin="round"/>'
    )
    if knockout_eye:
        body_d, beak_d = knockout_paths(s["eye"])
        duck_parts = (f'<path d="{body_d}" fill="{duck}" fill-rule="evenodd"/>'
                      f'<path d="{beak_d}" fill="{beak}" fill-rule="evenodd"/>')
    else:
        duck_parts += f'<circle cx="70" cy="36" r="{f(s["eye"])}" fill="{tile_color}"/>'
    duck_g = (f'<g clip-path="url(#{uid}-water)"><g transform="{s["duck_t"]}">'
              f'{duck_parts}</g></g>')
    wave_p = (f'<path d="{s["wave"]}" fill="none" stroke="{wave}" stroke-width="{f(s["stroke"])}" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')

    art = duck_g + wave_p
    if tile:
        art = f'<g clip-path="url(#{uid}-tile)">{art}</g>'
    if inset != 1.0:
        off = 50 * (1 - inset)
        art = f'<g transform="translate({f(off)} {f(off)}) scale({f(inset)})">{art}</g>'
    bg = f'<path d="{tile_d}" fill="{tile_color}"/>' if tile else ""
    wh = f' width="{size_px}" height="{size_px}"' if size_px else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"{wh}>'
            f'<title>{P["site"]["name"]}</title><defs>{"".join(defs)}</defs>{bg}{art}</svg>\n')


VARIANTS = {
    # name: (kwargs, description)
    "mark-full": (dict(small=False), "Primary mark, full detail, smooth-cornered tile"),
    "mark-small": (dict(small=True), "Simplified for 16-32 px: heavier stroke, slightly larger duck"),
    "mark-full-square": (dict(small=False, tile="square"), "Full-bleed square tile (platforms that round corners themselves)"),
    "mark-maskable": (dict(small=False, tile="square", inset=0.8), "Square, artwork inside the 80% safe zone (Android maskable)"),
    "mark-notile-on-light": (dict(small=False, tile=None, duck=C["tile"], beak=C["wave_on_light"],
                                  wave=C["wave_on_light"], knockout_eye=True), "No tile, for light backgrounds"),
    "mark-notile-on-dark": (dict(small=False, tile=None, knockout_eye=True), "No tile, for dark backgrounds"),
    "mark-mono-dark": (dict(small=False, tile=None, duck=C["mono_dark"], beak=C["mono_dark"],
                            wave=C["mono_dark"], knockout_eye=True), "One colour, dark on light"),
    "mark-mono-light": (dict(small=False, tile=None, duck=C["mono_light"], beak=C["mono_light"],
                             wave=C["mono_light"], knockout_eye=True), "One colour, light on dark"),
}


def social_svg():
    S = P["site"]
    mark = mark_svg(small=False, uid="og")
    inner = mark.split(">", 1)[1].rsplit("</svg>", 1)[0]  # strip outer <svg>
    inner = inner.replace(f'<title>{S["name"]}</title>', "")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
        f'<rect width="1200" height="630" fill="{C["social_background"]}"/>'
        f'<svg x="100" y="165" width="300" height="300" viewBox="0 0 100 100">{inner}</svg>'
        f'<text x="450" y="300" font-family="Inter, DejaVu Sans, sans-serif" font-weight="700" '
        f'font-size="76" fill="{C["social_text"]}">{S["name"]}</text>'
        f'<text x="452" y="356" font-family="Inter, DejaVu Sans, sans-serif" font-weight="500" '
        f'font-size="26" fill="{C["social_subtext"]}">{S["tagline"]}</text>'
        f'<text x="452" y="402" font-family="Inter, DejaVu Sans, sans-serif" font-weight="500" '
        f'font-size="26" fill="{C["social_subtext"]}">{S["url"]}</text>'
        '</svg>\n'
    )


# ---------------------------------------------------------------- outputs

def write(rel, data, mode="w"):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as fh:
        fh.write(data)
    return path


def main():
    try:
        import cairosvg
        from PIL import Image
    except ImportError:
        sys.exit("Needs: pip install cairosvg pillow shapely")

    def png(svg, px, bg=None):
        out = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px,
                               background_color=bg)
        return Image.open(io.BytesIO(out)).convert("RGBA")

    # masters
    os.makedirs(os.path.join(ROOT, "png"), exist_ok=True)
    for name, (kw, _) in VARIANTS.items():
        svg = mark_svg(uid=name, **kw)
        write(f"svg/{name}.svg", svg)
        png(svg, 1024).save(os.path.join(ROOT, f"png/{name}-1024.png"))

    # web
    small = mark_svg(small=True, uid="fav")
    write("web/icon.svg", small)
    ico_imgs = [png(small, s) for s in (16, 32, 48)]
    ico_imgs[-1].save(os.path.join(ROOT, "web/favicon.ico"), format="ICO",
                      sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico_imgs[:-1])
    png(mark_svg(small=False, tile="square", uid="apple"), 180, bg=C["tile"]).convert("RGB") \
        .save(os.path.join(ROOT, "web/apple-touch-icon.png"))
    full = mark_svg(small=False, uid="full")
    png(full, 192).save(os.path.join(ROOT, "web/icon-192.png"))
    png(full, 512).save(os.path.join(ROOT, "web/icon-512.png"))
    png(mark_svg(small=False, tile="square", inset=0.8, uid="mask"), 512, bg=C["tile"]).convert("RGB") \
        .save(os.path.join(ROOT, "web/icon-maskable-512.png"))
    S = P["site"]
    write("web/manifest.webmanifest", json.dumps({
        "name": S["name"],
        "short_name": S["short_name"],
        "icons": [
            {"src": "icon-192.png", "type": "image/png", "sizes": "192x192"},
            {"src": "icon-512.png", "type": "image/png", "sizes": "512x512"},
            {"src": "icon-maskable-512.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable"},
        ],
        "theme_color": C["tile"],
        "background_color": C["tile"],
        "display": "browser",
    }, indent=2, ensure_ascii=False) + "\n")
    write("web/head-snippet.html", f"""<!-- Favicons for {S['url']}: place the files from web/ at your site root -->
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="{C['tile']}">
<!-- Social preview (optional): put social/og-image.png at /assets/og-image.png -->
<meta property="og:image" content="https://{S['url']}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
""")

    # mkdocs
    write("mkdocs/logo.svg", small)
    write("mkdocs/mkdocs-snippet.yml", """# Merge into mkdocs.yml (Material theme).
# Copy web/* into docs/ (so they are served from the site root),
# mkdocs/logo.svg to docs/assets/logo.svg, and social/og-image.png to docs/assets/og-image.png.
theme:
  name: material
  logo: assets/logo.svg
  favicon: favicon.ico
  custom_dir: overrides   # if you already have a custom_dir, merge overrides/main.html into it
""")
    write("mkdocs/overrides/main.html", f"""{{% extends "base.html" %}}

{{% block extrahead %}}
  {{{{ super() }}}}
  <link rel="icon" href="{{{{ 'icon.svg' | url }}}}" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{{{{ 'apple-touch-icon.png' | url }}}}">
  <link rel="manifest" href="{{{{ 'manifest.webmanifest' | url }}}}">
  <meta name="theme-color" content="{C['tile']}">
  <meta property="og:image" content="https://{S['url']}/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
{{% endblock %}}
""")

    # social
    og = social_svg()
    write("social/og-image.svg", og)
    og_png = cairosvg.svg2png(bytestring=og.encode(), output_width=1200, output_height=630)
    write("social/og-image.png", og_png, mode="wb")

    # preview sheet
    sheet = Image.new("RGB", (1400, 760), "#F4F3EF")
    x = 40
    for name in VARIANTS:
        dark = name.endswith("on-dark") or name.endswith("mono-light")
        cell = Image.new("RGB", (150, 150), "#1E1E20" if dark else "#FFFFFF")
        im = Image.open(os.path.join(ROOT, f"png/{name}-1024.png")).resize((130, 130), Image.LANCZOS)
        cell.paste(im, (10, 10), im)
        sheet.paste(cell, (x, 40))
        x += 168
    for i, (bgc, y) in enumerate((("#FFFFFF", 240), ("#1E1E20", 340))):
        row = Image.new("RGB", (1320, 80), bgc)
        xx = 20
        for s in (64, 48, 32, 16):
            svg = full if s > 32 else small
            im = png(svg, s)
            row.paste(im, (xx, 40 - s // 2), im)
            xx += s + 40
        sheet.paste(row, (40, y))
    og_im = Image.open(io.BytesIO(og_png)).convert("RGB").resize((600, 315), Image.LANCZOS)
    sheet.paste(og_im, (40, 440))
    sheet.save(os.path.join(ROOT, "preview.png"))
    print("Built assets into", ROOT)


if __name__ == "__main__":
    main()
