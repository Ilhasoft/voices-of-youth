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

    def test_default_avatar(self):
        """
        The default avatar is set correctly?
        """
        with self.settings(MEDIA_ROOT='/tmp'):
            user = mommy.make(VoyUser, username='fake_username')
            self.assertEqual(user.get_avatar_display(), f'/media/users/avatars/group-1.png')

    def test_custom_avatar(self):
        """
        User can set a custom avatar?
        """
        with self.settings(MEDIA_ROOT='/tmp'):
            user = mommy.make(VoyUser, username='fake_username', avatar=20)
            self.assertEqual(user.get_avatar_display(), f'/media/users/avatars/group-20.png')
