import shutil
import uuid

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.test import TestCase
from model_mommy import mommy
from unipath import Path

from voicesofyouth.user.models import VoyUser

__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'


class VoyUserTestCase(TestCase):
    def tearDown(self):
        shutil.rmtree('/tmp/users', ignore_errors=True)

    def test_voy_user_is_registered(self):
        """
        VoyUser has been registered?
        """
        self.assertEqual(VoyUser, get_user_model())

    def test__str__(self):
        """
        str(VoyUser) returns the correct value?
        """
        user = mommy.make(VoyUser, username='fake_username')
        self.assertEqual(str(user), 'fake_username')

    def test_avatar_path(self):
        """
        The avatar file is saved in correct place?
        """
        test_img = Path(__file__).absolute().ancestor(2).child('test', 'assets', 'python.png')
        UUID = uuid.uuid5(uuid.NAMESPACE_OID, test_img.name)
        with self.settings(MEDIA_ROOT='/tmp'), open(test_img, 'rb') as image:
            fake_avatar = ImageFile(image)
            user = mommy.make(VoyUser, username='fake_username', avatar=fake_avatar)
            self.assertEqual(user.avatar.file.name, f'/tmp/users/{user.username}/avatar/{UUID}.png')

    def test_avatar_resize(self):
        """
        The avatar file are resized when saving?
        """
        test_img = Path(__file__).absolute().ancestor(2).child('test', 'assets', 'python.png')
        with self.settings(MEDIA_ROOT='/tmp'), open(test_img, 'rb') as image:
            fake_avatar = ImageFile(image)
            user = mommy.make(VoyUser, username='fake_username', avatar=fake_avatar)
            resized = Image.open(user.avatar.file)
            self.assertEqual(resized.size, (50, 50))
