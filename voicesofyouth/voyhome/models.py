import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from unipath import Path
from easy_thumbnails.files import get_thumbnailer
from ordered_model.models import OrderedModel

from voicesofyouth.core.models import BaseModel
from voicesofyouth.project.models import Project


CONTACT_CHOICES = (
    (1, _('Be a Mapper')),
    (2, _('Questions or suggestions')),
)


def upload_to(instance, filename):
    '''
    Calculate user avatar upload path dynamically.
    '''
    PROJECT_UUID = uuid.uuid5(uuid.NAMESPACE_OID, instance.image.name)
    FILE_UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename)
    FILE_EXT = Path(filename).ext
    return f'home/{PROJECT_UUID}/thumbnail/{FILE_UUID}{FILE_EXT}'


class Slide(OrderedModel, BaseModel):
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        verbose_name = _('Home Slide')
        verbose_name_plural = _('Home Slide')
        db_table = 'home_slide'
        ordering = ('order',)

    def __str__(self):
        return self.image.file

    @property
    def thumbnail(self):
        if self.image:
            return get_thumbnailer(self.image)['home_slide_thumbnail_cropped']

    @property
    def thumbnail_home(self):
        if self.image:
            return get_thumbnailer(self.image)['home_slide_cropped']


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


class Contact(BaseModel):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Name'))
    email = models.EmailField(null=False, blank=False, max_length=255, verbose_name=_('Email'))
    want = models.IntegerField(verbose_name=_('What do you want'), choices=CONTACT_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))
    accepted = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name = _('Contact Form')
        verbose_name_plural = _('Contact Form')
        db_table = 'home_contact'

    def __str__(self):
        return self.name
