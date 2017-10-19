import shutil
import tempfile

from PIL import Image
from unipath import Path


def resize_image(img, size, img_format='PNG', quality=100):
    with tempfile.TemporaryDirectory() as tmpdirname:
        img = Path(img)
        temp_img = Path(tmpdirname).child(img.name)
        shutil.copy(img, temp_img)

        im = Image.open(temp_img)
        if im.size != size:
            im = im.resize(size)
            im.save(img, format=img_format, quality=quality)
