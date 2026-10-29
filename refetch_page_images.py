# -*- coding: utf-8 -*-
"""Re-fetch the brand-guide screenshots and convert them to sRGB.

The originals on zeroheight carry a wide-gamut ICC profile. Downscaling them
with Pillow dropped it, so the browser read P3 numbers as sRGB and BTIS navy
#3B2968 came out bright blue, its teal bright green. Convert through the
embedded profile instead of discarding it.
"""
import os, io, urllib.request
from PIL import Image, ImageCms

ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_W = 900
SRGB = ImageCms.createProfile("sRGB")

IMAGES = {
    "brand-assets/btis-logo/img": {
        "lockup.jpg": "tMpGx3kkEAKooNrbZWB4jA.jpg",
        "brand-1.png": "m1LZPZdnSBMa9sUZ88KDBg.png",
        "brand-2.jpg": "trjW9OSf473-pYDjsJ_mRA.jpg",
        "brand-3.jpg": "DppkaJq3Q6L9VPhrGe7nig.jpg",
        "neutral-1.jpg": "fASAZS02BeCQlb4jeutmYw.jpg",
        "neutral-2.jpg": "7m_p0YHHZnFPX0QOoWtxyQ.jpg",
        "inverse-1.jpg": "HDMN1mtBuSiXwhBBGXYofA.jpg",
        "do-1.png": "dSwl7mDjJkRSYBTyMbRBJg.png",
        "do-2.jpg": "3cikqCkMqfI-wqpt96nPbA.jpg",
        "do-3.jpg": "nNHdLA3IiTGRYa9TOFioKA.jpg",
        "do-4.jpg": "NCi4Nk3tmMCF_kHmwOurPQ.jpg",
        "do-5.jpg": "gnJ-k4C2PLooQhFxPvPCRA.jpg",
        "do-6.jpg": "hCA_S2RnJAwpJ3kuTSPb7A.jpg",
        "do-7.jpg": "-pFbVKVNCUxL05jr0EVogQ.jpg",
        "do-8.jpg": "qZ-2kXznpMkVBrfIAiGiOQ.jpg",
        "do-9.png": "tssANgtwl4XBhx-xzP5l4w.png",
        "do-10.jpg": "HFhfO-94kVRoXsjFQu8mbQ.jpg",
        "do-11.jpg": "lJpEvYfGu_6THTwpzN1TwA.jpg",
        "do-12.jpg": "ndwWkGpDgaEVMx2rDtNg-w.jpg",
        "dont-1.jpg": "COHuRYiTKLJi6Oh5Qt-XZw.jpg",
        "dont-2.jpg": "W7EHl-IMGstFLdAIAnFgfw.jpg",
        "dont-3.jpg": "6NEO3ypc8CzVmPuuryq4uQ.jpg",
        "dont-4.jpg": "pJU-5dAx1WiDVuwFj3d9cQ.jpg",
        "dont-5.jpg": "hDqYvEhgZLPzstTNxh8zHA.jpg",
        "dont-6.jpg": "uYnq6dkKqIDMnrG3tNTc3A.jpg",
        "dont-7.jpg": "Hemkv7zRi55rKLR_lLy9UA.jpg",
        "dont-8.jpg": "emsBLN6uMsWNoseunCTN2g.jpg",
    },
    "brand-assets/norbielink-logo/img": {
        "lockup-dark.png": "a5QhJ-INCnX_SZiWP4h05w.png",
        "lockup-white.png": "UYdOYYkq67cLd_WYGXy8DA.png",
        "brand-1.png": "yyMEoBSelEhVptQl95pPaQ.png",
        "brand-2.png": "kZHBVeToQxZJg-KkFqPK5A.png",
        "neutral-1.png": "uOJ5QCk5BPmJqCPdW4Tb-Q.png",
        "neutral-2.png": "SZm4ESDOcxOQ8nCFv7FOcQ.png",
        "do-1.png": "m8ANwyD3sfuAHybPFXt5qw.png",
        "do-2.png": "H8KztL4kmBCjTf7WtXF7_Q.png",
        "do-3.png": "UPESigPBnpl4XbxTxC1NQg.png",
        "do-4.png": "PlwPn5aUe184SvCSfFKV0g.png",
        "do-5.png": "lgeoRcYA0Z2zHaNJBKEMqg.png",
        "do-6.png": "lLBaKtKyYYBJNEELitI54w.png",
    },
    "brand-assets/characters/img": {
        "norbie-hero.png": "1kXVuJyo1zJ4MS3qragtjA.png",
        "norbie-do-gradient.png": "9rGshdbiLOdjfJKs9Rz6fg.png",
        "norbie-dont-color.png": "jrLqImA1PCf6wXIgXyWSzw.png",
        "norbie-do-dressup.jpg": "dq_MJw_PuOwAdKAnnpUUuw.jpg",
        "norbie-dont-style.jpg": "elg1r6fT0NBmqeE53s04Mw.jpg",
        "ainorbie-hero.jpeg": "JCYSUWpUIU7hPSnjCE2FOg.jpeg",
    },
    "brand-assets/visual-elements/img": {
        "tiles-hero.png": "ZOCaqS3E1Xt88WqNWKPp6w.png",
        "monstera-hero.png": "hptSu4ifEoRVOdEuckpRjQ.png",
        "banana-hero.png": "SSFIdVWISNZ_odV5nlomjw.png",
        "awning-hero.png": "1jAXfVo9Ll-Ov-HSxbav5Q.png",
        "jungle-hero.png": "NrZOtdfMgh9nahX5NPCqOw.png",
    },
}

# The icon canvas is 1:1 and mostly empty, so it is trimmed and re-padded.
ICON = ("brand-assets/norbielink-logo/img/icon.png", "Mr0xzAlpYAvCEbxnma301g.png")


def to_srgb(im):
    """Convert through the embedded profile.

    Several of these JPEGs are CMYK with a U.S. Web Coated (SWOP) v2 profile.
    Pillow's plain .convert("RGB") does a naive inversion on those, which is
    what turned BTIS navy into bright blue. The image has to stay in its own
    mode until the transform runs."""
    icc = im.info.get("icc_profile")
    if not icc:
        return (im.convert("RGB") if im.mode == "CMYK" else im), False
    if im.mode == "P":
        im = im.convert("RGBA")
    out = "RGBA" if im.mode in ("RGBA", "LA") else "RGB"
    try:
        return ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                         SRGB, outputMode=out), True
    except Exception as e:
        print("   profile conversion failed (%s, %s): %s" % (im.mode, len(icc), e))
        return (im.convert("RGB") if im.mode == "CMYK" else im), False


def fetch(uid):
    url = "https://zeroheight.com/uploads/" + uid
    with urllib.request.urlopen(url) as r:
        return Image.open(io.BytesIO(r.read()))


def save(im, path):
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    full = os.path.join(ROOT, path)
    if path.lower().endswith(".png"):
        im.save(full, optimize=True)
    else:
        im.convert("RGB").save(full, "JPEG", quality=72, optimize=True, progressive=True)
    return im.size


converted = 0
for folder, files in IMAGES.items():
    for name, uid in files.items():
        im = fetch(uid)
        im, did = to_srgb(im)
        converted += did
        size = save(im, os.path.join(folder, name))
        print("%-46s %s %s" % (os.path.join(folder, name), size, "→sRGB" if did else ""))

im = fetch(ICON[1])
im, did = to_srgb(im)
converted += did
im = im.convert("RGBA")
box = im.split()[3].getbbox()
my = int((box[3] - box[1]) * 0.22)
crop = im.crop((box[0], max(0, box[1] - my), box[2], min(im.height, box[3] + my)))
if crop.width > MAX_W:
    crop = crop.resize((MAX_W, round(crop.height * MAX_W / crop.width)), Image.LANCZOS)
tw = int(crop.height * 1.8)
canvas = Image.new("RGBA", (tw, crop.height), (0, 0, 0, 0))
canvas.paste(crop, ((tw - crop.width) // 2, 0), crop)
canvas.save(os.path.join(ROOT, ICON[0]), optimize=True)
print("%-46s %s %s" % (ICON[0], canvas.size, "→sRGB" if did else ""))
print("colour-managed:", converted)
