import shutil
import uuid
from unittest import mock

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files import File
from model_mommy import mommy

from voicesofyouth.users.models import VoyUser


__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'


class VoyUserTestCase(TestCase):
    def tearDown(self):
        shutil.rmtree('/tmp/users', ignore_errors=True)

    def test_voy_user_is_registered(self):
        '''
        VoyUser has been registered?
        '''
        self.assertEqual(VoyUser, get_user_model())

    def test__str__(self):
        '''
        str(VoyUser) returns the correct value?
        '''
        user = mommy.make(VoyUser, username='fake_username')
        self.assertEqual(str(user), 'fake_username')

    def test_avatar_path(self):
        '''
        The avatar file is saved in correct place?
        '''
        fake_avatar = mock.MagicMock(spec=File)
        fake_avatar.name = 'fake_image.jpg'
        UUID = uuid.uuid5(uuid.NAMESPACE_OID, fake_avatar.name)
        with self.settings(MEDIA_ROOT='/tmp'):
            user = mommy.make(VoyUser, username='fake_username', avatar=fake_avatar)
            self.assertEqual(user.avatar.file.name, f'/tmp/users/{user.username}/avatar/{UUID}.jpg')
