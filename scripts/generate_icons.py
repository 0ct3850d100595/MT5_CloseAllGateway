"""Generate the CLOSE_ALL PWA icons (build-time tool, not a runtime
dependency - requires Pillow, which is intentionally NOT in
requirements.txt). Run manually whenever the icon design changes:

    python scripts/generate_icons.py

Run from the repo root so the output paths below resolve correctly.
"""
from PIL import Image, ImageDraw

BACKGROUND = (17, 17, 17, 255)   # #111111 - matches confirm.html's body background
RED = (192, 57, 43, 255)         # #c0392b - matches confirm.html's button color
WHITE = (255, 255, 255, 255)

SIZES = {
    "static/icons/icon-192.png": 192,
    "static/icons/icon-512.png": 512,
    "static/icons/apple-touch-icon.png": 180,
}


def make_icon(size):
    img = Image.new("RGBA", (size, size), BACKGROUND)
    draw = ImageDraw.Draw(img)

    circle_margin = size * 0.1
    draw.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        fill=RED,
    )

    stop_size = size * 0.32
    cx, cy = size / 2, size / 2
    draw.rectangle(
        [cx - stop_size / 2, cy - stop_size / 2, cx + stop_size / 2, cy + stop_size / 2],
        fill=WHITE,
    )
    return img


if __name__ == "__main__":
    for path, size in SIZES.items():
        make_icon(size).save(path)
        print(f"wrote {path} ({size}x{size})")
