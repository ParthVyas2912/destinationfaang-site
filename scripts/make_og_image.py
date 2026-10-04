"""Generate the Destination Engineer logo and social artwork.

Run from the repo root: python scripts/make_og_image.py
Requires Pillow. SVG and PNG marks share the same original polygon geometry.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1] / "assets"
BRAND = ASSETS / "brand"
BG = "#0b0d13"
LIME = "#e5ff46"
WHITE = "#f4f6ed"
MUTED = "#adb5c5"

D_OUTER = [(104, 140), (202, 140), (268, 206), (268, 306), (202, 372), (104, 372)]
D_INNER = [(150, 188), (184, 188), (220, 224), (220, 288), (184, 324), (150, 324)]
E_ARROW = [
    (300, 140), (408, 140), (408, 188), (348, 188), (348, 230),
    (384, 230), (384, 212), (428, 256), (384, 300), (384, 282),
    (348, 282), (348, 324), (408, 324), (408, 372), (300, 372),
]


def font(size, bold=False):
    names = (
        ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold
        else ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    raise RuntimeError("Install Segoe UI, Arial, or DejaVu Sans to generate brand artwork.")


def path(points):
    return "M" + " L".join(f"{x},{y}" for x, y in points) + " Z"


def svg_mark(background=True, ink=WHITE, accent=LIME):
    circle = f'<circle cx="256" cy="256" r="256" fill="{BG}"/>' if background else ""
    return (
        circle
        + f'<path fill="{ink}" fill-rule="evenodd" d="{path(D_OUTER)} {path(D_INNER)}"/>'
        + f'<path fill="{accent}" d="{path(E_ARROW)}"/>'
    )


def save_svg(destination, width, height, content):
    destination.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
        '<title id="title">Destination Engineer</title>'
        + content + "</svg>\n",
        encoding="utf-8",
    )


def mark(size, background=True):
    scale = 4
    img = Image.new("RGBA", (512 * scale, 512 * scale))
    draw = ImageDraw.Draw(img)
    if background:
        draw.ellipse((0, 0, 512 * scale - 1, 512 * scale - 1), fill=BG)
    for points, color in (
        (D_OUTER, WHITE), (D_INNER, BG if background else (0, 0, 0, 0)), (E_ARROW, LIME)
    ):
        draw.polygon([(x * scale, y * scale) for x, y in points], fill=color)
    return img.resize((size, size), Image.Resampling.LANCZOS)


def text(draw, xy, value, size, color=WHITE, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=color, anchor="lt")


def save_png(img, destination):
    img.save(destination, "PNG", optimize=True)
    print(f"Wrote {destination.relative_to(ASSETS.parent)} ({img.width}x{img.height})")


def main():
    BRAND.mkdir(parents=True, exist_ok=True)
    save_svg(ASSETS / "logo.svg", 512, 512, svg_mark())
    save_svg(BRAND / "mark-transparent.svg", 512, 512, svg_mark(False))
    save_svg(BRAND / "mark-monochrome.svg", 512, 512, svg_mark(False, BG, BG))
    save_png(mark(800), ASSETS / "logo.png")
    save_png(mark(800, False), BRAND / "mark-transparent.png")
    save_png(mark(180), ASSETS / "apple-touch-icon.png")
    save_png(mark(400), BRAND / "linkedin-logo.png")
    save_png(mark(150), BRAND / "youtube-watermark.png")

    og = Image.new("RGB", (1200, 630), BG)
    draw = ImageDraw.Draw(og)
    draw.rectangle((64, 60, 176, 68), fill=LIME)
    og.paste(mark(350, False), (36, 140), mark(350, False))
    text(draw, (412, 155), "DESTINATION", 44, bold=True)
    text(draw, (408, 210), "ENGINEER", 96, LIME, True)
    text(draw, (412, 350), "Beyond interviews.", 34)
    text(draw, (412, 398), "Become a better engineer.", 34)
    text(draw, (68, 540), "DSA  /  SYSTEM DESIGN  /  CAREER GROWTH", 23, MUTED)
    save_png(og, ASSETS / "og-image.png")
    save_svg(
        ASSETS / "og-image.svg", 1200, 630,
        f'<rect width="1200" height="630" fill="{BG}"/>'
        f'<rect x="64" y="60" width="112" height="8" fill="{LIME}"/>'
        f'<g transform="translate(36 140) scale({350 / 512})">{svg_mark(False)}</g>'
        f'<g font-family="Segoe UI, Arial, sans-serif" fill="{WHITE}">'
        '<text x="412" y="191" font-size="44" font-weight="700">DESTINATION</text>'
        f'<text x="408" y="295" font-size="96" font-weight="700" fill="{LIME}">ENGINEER</text>'
        '<text x="412" y="379" font-size="34">Beyond interviews.</text>'
        '<text x="412" y="427" font-size="34">Become a better engineer.</text>'
        f'<text x="68" y="562" font-size="23" fill="{MUTED}">'
        'DSA / SYSTEM DESIGN / CAREER GROWTH</text></g>',
    )

    banner = Image.new("RGB", (2560, 1440), BG)
    draw = ImageDraw.Draw(banner)
    draw.line((240, 400, 2320, 400), fill="#262b39", width=2)
    draw.line((240, 1040, 2320, 1040), fill="#262b39", width=2)
    draw.rectangle((240, 392, 420, 408), fill=LIME)
    banner.paste(mark(350, False), (530, 537), mark(350, False))
    text(draw, (945, 556), "DESTINATION", 54, bold=True)
    text(draw, (940, 624), "ENGINEER", 124, LIME, True)
    text(draw, (945, 778), "Beyond interviews. Become a better engineer.", 36)
    text(draw, (945, 847), "destinationengineer.com", 30, MUTED)
    save_png(banner, BRAND / "youtube-banner.png")

    cover = Image.new("RGB", (1128, 191), BG)
    draw = ImageDraw.Draw(cover)
    draw.rectangle((365, 27, 445, 32), fill=LIME)
    text(draw, (365, 46), "DESTINATION ENGINEER", 44, LIME, True)
    text(draw, (365, 109), "Beyond interviews. Become a better engineer.", 24)
    save_png(cover, BRAND / "linkedin-cover.png")

    wordmark = Image.new("RGBA", (1200, 300))
    wordmark.paste(mark(300, False), (0, 0), mark(300, False))
    draw = ImageDraw.Draw(wordmark)
    text(draw, (325, 62), "DESTINATION", 44, bold=True)
    text(draw, (320, 125), "ENGINEER", 108, LIME, True)
    save_png(wordmark, BRAND / "wordmark.png")


if __name__ == "__main__":
    main()
