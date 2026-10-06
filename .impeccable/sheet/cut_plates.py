"""Cut the hardware sprite sheet into plates with a matte derived from the flat background.

Objects are found from their sharp outlines (soft shadows have low gradient), holes filled so
enclosed highlights stay opaque; darker ground around objects becomes a soft black shadow alpha.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SHEET = Image.open(".impeccable/sheet/hardware-sheet.png").convert("RGB")
BG = np.array([196, 193, 188], dtype=float)


def cut(box, shadow=True):
    a = np.asarray(SHEET.crop(box), dtype=float)
    lum = a.mean(axis=2)
    sat = (a.max(axis=2) - a.min(axis=2)) / (a.max(axis=2) + 1)
    g = np.hypot(ndimage.sobel(lum, 0), ndimage.sobel(lum, 1))
    edges = g > 60                                   # sharp object outlines; soft shadows stay below this
    mask = ndimage.binary_fill_holes(ndimage.binary_closing(edges, iterations=3))
    lab, n = ndimage.label(mask)
    keep = lab == (np.argmax(ndimage.sum(mask, lab, range(1, n + 1))) + 1) if n else mask
    core = ((lum < 90) | (sat > 0.3)) & ndimage.binary_dilation(keep, iterations=4)
    obj = ndimage.binary_erosion(ndimage.binary_fill_holes(keep | core), iterations=1)
    soft = ndimage.gaussian_filter(obj.astype(float), 0.7)
    shade = np.clip((BG.mean() - lum - 7) / BG.mean(), 0, 1) * ~obj * 1.5   # darker than ground (past noise) -> black shadow
    alpha = np.maximum(soft, ndimage.gaussian_filter(shade, 1.2)).clip(0, 1) if shadow else soft
    rgb = np.where(obj[..., None], a, 0)
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def place(img, canvas, scale=1.0):
    """Centre img (scaled) on a transparent canvas of the region's aspect."""
    w, h = img.size
    img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    out.paste(img, ((canvas[0] - img.width) // 2, (canvas[1] - img.height) // 2), img)
    return out


def nine_slice(img, size, cut_frac=0.3):
    """Stretch the centre band only, so a square bezel becomes a rectangle with true corners."""
    w, h = img.size
    cx0, cx1 = round(w * cut_frac), round(w * (1 - cut_frac))
    left, mid, right = img.crop((0, 0, cx0, h)), img.crop((cx0, 0, cx1, h)), img.crop((cx1, 0, w, h))
    mid = mid.resize((size[0] - left.width - right.width, h), Image.LANCZOS)
    out = Image.new("RGBA", (size[0], h))
    out.paste(left, (0, 0)); out.paste(mid, (left.width, 0)); out.paste(right, (left.width + mid.width, 0))
    return out.resize(size, Image.LANCZOS)


boxes = {  # sheet pixel boxes (with margin) for each object
    "knob-l": (60, 80, 395, 410), "knob-s": (475, 125, 735, 380), "lever": (850, 110, 1070, 385),
    "screw": (1270, 165, 1440, 335), "lamp-g": (85, 515, 315, 745), "lamp-r": (460, 515, 690, 745),
    "btn-r": (795, 465, 1110, 775), "btn-g": (1180, 465, 1490, 775),
}
# Rotating and switching parts ship without a baked shadow: the page casts one that stays put.
cuts = {k: cut(b, shadow=k in ("screw", "btn-r", "btn-g")) for k, b in boxes.items()}
P = "assets/plates/"
place(cuts["knob-l"], (406, 448)).save(P + "source-knob.png")
place(cuts["knob-s"], (313, 329), 1.15).save(P + "circuit-knob.png")
place(cuts["lever"], (256, 256), 0.95).save(P + "backend-lever.png")
for corner in ("tl", "tr", "bl", "br"):
    place(cuts["screw"], (216, 216), 1.0).save(P + f"screw-{corner}.png")
place(cuts["lamp-g"], (320, 320), 1.2).save(P + "lamp-green.png")
place(cuts["lamp-r"], (320, 320), 1.2).save(P + "lamp-red.png")

# Chassis texture: a clean patch of the comp's ground, mirror-tiled (allowed for textures).
comp = Image.open(".impeccable/mocks/comp-4.png").convert("RGB")
patch = comp.crop((930, 4, 1070, 62))
tile = Image.new("RGB", (patch.width * 2, patch.height * 2))
tile.paste(patch, (0, 0)); tile.paste(patch.transpose(Image.FLIP_LEFT_RIGHT), (patch.width, 0))
tile.paste(patch.transpose(Image.FLIP_TOP_BOTTOM), (0, patch.height))
tile.paste(patch.transpose(Image.ROTATE_180), (patch.width, patch.height))
tex = Image.new("RGB", (462, 258))
for x in range(0, 462, tile.width):
    for y in range(0, 258, tile.height):
        tex.paste(tile, (x, y))
tex.save(P + "chassis.png")
print("plates written")
