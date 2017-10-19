import shutil
import tempfile

from PIL import Image
from PIL import ImageOps
from unipath import Path


def resize_image(img, size, img_format='PNG', quality=100):
    with tempfile.TemporaryDirectory() as tmpdirname:
        img = Path(img)
        temp_img = Path(tmpdirname).child(img.name)
        shutil.copy(img, temp_img)

        im = Image.open(temp_img)
        im_size = im.size
        if im_size != size:
            thumb = ImageOps.fit(im, size, Image.ANTIALIAS, centering=(0.5, 0.5))
            thumb.save(img, format=img_format, quality=quality)
