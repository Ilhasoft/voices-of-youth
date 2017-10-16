import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from sorl.thumbnail.fields import ImageField
from unipath import Path


def upload_to(instance, filename):
    UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename)
    FILE_EXT = Path(filename).ext
    return f'users/{instance.username}/avatar/{UUID}{FILE_EXT}'


class VoyUser(AbstractUser):
    '''
    language
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = ImageField(verbose_name=_('Image'), upload_to=upload_to, null=True, blank=True)


# We put this code here to centralize all references to User model.
User = get_user_model()
