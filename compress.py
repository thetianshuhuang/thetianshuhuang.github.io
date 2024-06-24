from PIL import Image
import os
import yaml


Image.MAX_IMAGE_PIXELS = None
THUMB_SIZE = 320
PHOTO_SIZE = 1 * 1000 * 1000

with open("data/photos.yaml") as f:
    photos = yaml.load(f, Loader=yaml.Loader)["photos"]


def _crop(short, long, target):
    center = int(long * target / 100)
    lower = max(center - short // 2, 0)
    upper = lower + short

    if upper >= long:
        return long - short, long
    else:
        return lower, upper


def _compress(src):
    img = Image.open(os.path.join("raw", src['path']))

    # Thumbnail
    if src.get("thumb") is None:
        cropped = img
    elif img.size[0] < img.size[1]:
        top, bottom = _crop(img.size[0], img.size[1], src['thumb'])
        cropped = img.crop((0, top, img.size[0], bottom))
    else:
        left, right = _crop(img.size[1], img.size[0], src['thumb'])
        cropped = img.crop((left, 0, right, img.size[1]))
    thumb = cropped.resize((THUMB_SIZE, THUMB_SIZE), Image.Resampling.LANCZOS)
    thumb.save(os.path.join("thumbs", src["path"]), 'jpeg', quality=75)

    # Display
    aspect = max(img.size) / min(img.size)
    target_mp = PHOTO_SIZE * aspect
    scale = (target_mp / (img.size[0] * img.size[1])) ** 0.5
    scaled = (int(img.size[0] * scale), int(img.size[1] * scale))
    display = img.resize(scaled, Image.Resampling.LANCZOS)
    display.save(os.path.join("photos", src["path"]), 'jpeg', quality=75)


for src in photos:
    try:
        _compress(src)
        print("Compressed: {}".format(src['path']))
    except FileNotFoundError:
        print("Skipping: {} (source not available)".format(src['path']))
