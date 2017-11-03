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


def upload_to(instance, filename):
    '''
    Calculate user avatar upload path dynamically.
    '''
    filename = Path(filename)
    UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename.name)
    return f'users/{instance.username}/avatar/{UUID}{filename.ext}'


class VoyUser(AbstractUser):
    '''
    Attributes:
        language: Default language of user.
        avatar: User avatar.
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = models.ImageField(verbose_name=_('Avatar'),
                               upload_to=upload_to,
                               null=True,
                               blank=True)

    @property
    def is_mapper(self):
        return self.groups.filter(name__contains='- mappers').exists()

# We put this code here to centralize all references to User model.
User = get_user_model()


@receiver(post_save, sender=VoyUser)
def resize_avatar(sender, instance, **kwargs):
    if instance.avatar:
        size = 50, 50
        resize_image(instance.avatar.file.name, size)
