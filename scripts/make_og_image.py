"""Generate assets/og-image.png (1200x630) for social sharing.

Many platforms (Twitter/X, LinkedIn, iMessage) do not render SVG OpenGraph
images, so we ship a raster PNG. Run from the repo root:

    python scripts/make_og_image.py

Re-run only if the branding/colors change.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = os.path.join("assets", "og-image.png")

# Diagonal gradient background (matches og-image.svg: #181b24 -> #2a1a2e).
TOP_LEFT = (0x18, 0x1b, 0x24)
BOT_RIGHT = (0x2a, 0x1a, 0x2e)


def _font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H))
    px = img.load()
    max_d = (W - 1) + (H - 1)
    for y in range(H):
        for x in range(W):
            t = (x + y) / max_d
            px[x, y] = (
                int(TOP_LEFT[0] + (BOT_RIGHT[0] - TOP_LEFT[0]) * t),
                int(TOP_LEFT[1] + (BOT_RIGHT[1] - TOP_LEFT[1]) * t),
                int(TOP_LEFT[2] + (BOT_RIGHT[2] - TOP_LEFT[2]) * t),
            )

    draw = ImageDraw.Draw(img)
    bold = ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]
    reg = ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
    semibold = ["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]

    draw.text((80, 150), "Destination FAANG", font=_font(bold, 84), fill="#ffffff")
    draw.text((84, 270), "DSA \u00b7 System Design \u00b7 Behavioral interview videos",
              font=_font(reg, 40), fill="#99a0b2")
    draw.text((84, 340), "400+ problems \u00b7 filter by company & difficulty",
              font=_font(reg, 34), fill="#cbd2e6")

    pills = [
        ("Google", "#4f9dff", 150),
        ("Amazon", "#34d399", 150),
        ("Microsoft", "#f59e0b", 170),
        ("Meta", "#a78bfa", 120),
        ("Apple", "#f87171", 120),
    ]
    x = 84
    y = 450
    ph = 56
    pill_font = _font(semibold, 30)
    for label, color, w in pills:
        draw.rounded_rectangle([x, y, x + w, y + ph], radius=ph // 2, fill=color)
        bbox = draw.textbbox((0, 0), label, font=pill_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x + (w - tw) / 2 - bbox[0], y + (ph - th) / 2 - bbox[1]),
                  label, font=pill_font, fill="#0b0d12")
        x += w + 18

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
