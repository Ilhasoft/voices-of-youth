import os
import uuid

from datetime import datetime

from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.projects.models import Project
from voicesofyouth.reports.models import Report


MEDIA_TYPES = (
    ('link', _('Link')),
    ('image', _('Image')),
    ('video', _('Video')),
)


def unique_filename(filename):
    filename, ext = os.path.splitext(filename)
    fn = ('%s' % uuid.uuid4()).split('-')
    return '%s%s%s' % (fn[-1], fn[-2], ext)


def get_content_file_path(instance, filename):
    filename = unique_filename(filename)
    now = datetime.now()
    return os.path.join('content/%d/%d/%d/' % (now.year, now.month, now.day), filename)


class Media(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))

    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))

    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, verbose_name=_('Type'))

    url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('URL'))

    file = models.FileField(upload_to=get_content_file_path, blank=True, verbose_name=_('File'))

    screenshot = models.FileField(upload_to=get_content_file_path, blank=True, verbose_name=_('Screenshot'))

    extra = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Extra'))

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    visibled = models.BooleanField(default=True, verbose_name=_('Visibled'))

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.description, self.media_type)
