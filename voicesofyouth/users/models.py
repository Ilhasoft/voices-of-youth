import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField

from unipath import Path

__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


def upload_to(instance, filename):
    '''
    Calculate user avatar upload path dynamically.
    '''
    UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename)
    FILE_EXT = Path(filename).ext
    return f'users/{instance.username}/avatar/{UUID}{FILE_EXT}'


class VoyUser(AbstractUser):
    '''
    Attributes:
        language: Default language of user.
        avatar: User avatar.
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = ResizedImageField(verbose_name=_('Image'),
                               upload_to=upload_to,
                               null=True,
                               blank=True,
                               size=[50, 50],
                               crop=['middle', 'center'])


# We put this code here to centralize all references to User model.
User = get_user_model()
