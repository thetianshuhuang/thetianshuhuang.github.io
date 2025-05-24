"""Compress / downsample images."""

import os

import tyro
import yaml
from PIL import Image
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None


def _crop(short, long, target):
    center = int(long * target / 100)
    lower = max(center - short // 2, 0)
    upper = lower + short

    if upper >= long:
        return long - short, long
    else:
        return lower, upper


def _compress(
    src, thumb_size: int = 320, photo_size: int = 1000 * 1000
) -> None:
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
    thumb = cropped.resize((thumb_size, thumb_size), Image.Resampling.LANCZOS)
    thumb.save(os.path.join("thumbs", src["path"]), 'jpeg', quality=75)

    # Display
    aspect = max(img.size) / min(img.size)
    target_mp = photo_size * aspect
    scale = (target_mp / (img.size[0] * img.size[1])) ** 0.5
    scaled = (int(img.size[0] * scale), int(img.size[1] * scale))
    display = img.resize(scaled, Image.Resampling.LANCZOS)
    display.save(os.path.join("photos", src["path"]), 'jpeg', quality=75)


def compress(
    index: str = "data/photos.yaml",
    thumb: int = 320,
    photo: int = 1000 * 1000,
    overwrite: bool = False
) -> None:
    """Compress / downsample images, and generate thumbnails.

    Args:
        index: photo index file.
        thumb: thumbnail width/height, in pixels; thumbnails are always square.
        photo: compressed photo size, in total pixels.
        overwrite: whether to re-compress existing images.
    """
    with open(index) as f:
        photo_index = yaml.load(f, Loader=yaml.Loader)["photos"]

    skipped, na, success = [], [], []
    photos = sum(photo_index.values(), [])
    for src in tqdm(photos):
        if overwrite or not os.path.exists(os.path.join("thumbs", src['path'])):
            try:
                _compress(src, thumb_size=thumb, photo_size=photo)
                success.append(src['path'])
            except FileNotFoundError:
                na.append(src['path'])
        else:
            skipped.append(src['path'])

    if len(success) > 0:
        print(f"Compressed {len(success)} images: {success}")
    if len(skipped) > 0:
        print(f"Skipped {len(skipped)} already-compressed images: {skipped}")
    if len(na) > 0:
        print(f"Source unavailable for {len(na)} images: {na}")


if __name__ == "__main__":
    tyro.cli(compress)
