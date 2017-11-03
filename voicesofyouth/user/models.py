import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from unipath import Path

from voicesofyouth.core.utils import resize_image

__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'

DEFAULT_AVATAR = 1
AVATAR_FILE_EXTENSION = '.png'
AVATARS = (
    (1, f'{settings.MEDIA_URL}users/avatars/group-1{AVATAR_FILE_EXTENSION}'),
    (2, f'{settings.MEDIA_URL}users/avatars/group-2{AVATAR_FILE_EXTENSION}'),
    (3, f'{settings.MEDIA_URL}users/avatars/group-3{AVATAR_FILE_EXTENSION}'),
    (4, f'{settings.MEDIA_URL}users/avatars/group-4{AVATAR_FILE_EXTENSION}'),
    (5, f'{settings.MEDIA_URL}users/avatars/group-5{AVATAR_FILE_EXTENSION}'),
    (6, f'{settings.MEDIA_URL}users/avatars/group-6{AVATAR_FILE_EXTENSION}'),
    (7, f'{settings.MEDIA_URL}users/avatars/group-7{AVATAR_FILE_EXTENSION}'),
    (8, f'{settings.MEDIA_URL}users/avatars/group-8{AVATAR_FILE_EXTENSION}'),
    (9, f'{settings.MEDIA_URL}users/avatars/group-9{AVATAR_FILE_EXTENSION}'),
    (10, f'{settings.MEDIA_URL}users/avatars/group-10{AVATAR_FILE_EXTENSION}'),
    (11, f'{settings.MEDIA_URL}users/avatars/group-11{AVATAR_FILE_EXTENSION}'),
    (12, f'{settings.MEDIA_URL}users/avatars/group-12{AVATAR_FILE_EXTENSION}'),
    (13, f'{settings.MEDIA_URL}users/avatars/group-13{AVATAR_FILE_EXTENSION}'),
    (14, f'{settings.MEDIA_URL}users/avatars/group-14{AVATAR_FILE_EXTENSION}'),
    (15, f'{settings.MEDIA_URL}users/avatars/group-15{AVATAR_FILE_EXTENSION}'),
    (16, f'{settings.MEDIA_URL}users/avatars/group-16{AVATAR_FILE_EXTENSION}'),
    (17, f'{settings.MEDIA_URL}users/avatars/group-17{AVATAR_FILE_EXTENSION}'),
    (18, f'{settings.MEDIA_URL}users/avatars/group-18{AVATAR_FILE_EXTENSION}'),
    (19, f'{settings.MEDIA_URL}users/avatars/group-19{AVATAR_FILE_EXTENSION}'),
    (20, f'{settings.MEDIA_URL}users/avatars/group-20{AVATAR_FILE_EXTENSION}'),
    (21, f'{settings.MEDIA_URL}users/avatars/group-21{AVATAR_FILE_EXTENSION}'),
    (22, f'{settings.MEDIA_URL}users/avatars/group-22{AVATAR_FILE_EXTENSION}'),
    (23, f'{settings.MEDIA_URL}users/avatars/group-23{AVATAR_FILE_EXTENSION}'),
)


class VoyUser(AbstractUser):
    '''
    Attributes:
        language: Default language of user.
        avatar: User avatar.
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = models.IntegerField(choices=AVATARS, default=DEFAULT_AVATAR)

    @property
    def is_mapper(self):
        return self.groups.filter(name__contains='- mappers').exists()

# We put this code here to centralize all references to User model.
User = get_user_model()
