import tempfile

from PIL import Image


def create_fake_image():
    '''
    Generate a fake image for test purpose only.
    '''
    img = Image.new('RGB', (100, 100), 255)
    tmp_img = tempfile.NamedTemporaryFile(suffix='.jpg')
    img.save(tmp_img)
    tmp_img.seek(0)
    return tmp_img
