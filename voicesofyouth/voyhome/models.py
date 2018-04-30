import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from unipath import Path
from easy_thumbnails.files import get_thumbnailer

from voicesofyouth.core.models import BaseModel


def upload_to(instance, filename):
    '''
    Calculate user avatar upload path dynamically.
    '''
    PROJECT_UUID = uuid.uuid5(uuid.NAMESPACE_OID, instance.image.name)
    FILE_UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename)
    FILE_EXT = Path(filename).ext
    return f'home/{PROJECT_UUID}/thumbnail/{FILE_UUID}{FILE_EXT}'


class Slide(BaseModel):
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        verbose_name = _('Home Slide')
        verbose_name_plural = _('Home Slide')
        db_table = 'home_slide'

    def __str__(self):
        return self.image.file

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnailer(self.image)['home_slide_thumbnail_cropped']

    def get_absolute_url(self):
        return f'not-implemented/{self.id}'


class About(BaseModel):
    image = models.ImageField(upload_to=upload_to)
    about_project = models.TextField(null=False, blank=False, verbose_name=_('About The Project'))
    about_voy = models.TextField(null=False, blank=False, verbose_name=_('About VoY'))

    class Meta:
        verbose_name = _('About')
        verbose_name_plural = _('About')
        db_table = 'home_about'

    def __str__(self):
        return self.about_project

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnailer(self.image)['home_about_thumbnail_cropped']

    def get_absolute_url(self):
        return f'not-implemented/{self.id}'
