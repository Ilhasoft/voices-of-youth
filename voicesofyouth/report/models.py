import os
import uuid
from datetime import datetime

from django.contrib.gis.db import models as gismodels
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from voicesofyouth.core.models import BaseModel
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme
from voicesofyouth.users.models import User

STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3

STATUS_CHOICES = (
    (STATUS_APPROVED, _('Approved')),
    (STATUS_PENDING, _('Pending')),
    (STATUS_REJECTED, _('Rejected')),
)

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


class Report(BaseModel):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='reports')
    location = gismodels.PointField(null=False, blank=False)
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True)
    can_receive_comments = models.BooleanField(default=True, verbose_name=_('Can receive comments'))
    editable = models.BooleanField(default=True, verbose_name=_('Editable'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=STATUS_PENDING)
    tags = TaggableManager(through=Tag, blank=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return '{} - {}'.format(self.theme.project.name, self.theme.name)

    @property
    def project(self):
        return self.theme.project


class ReportComment(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=False, blank=False, verbose_name=_('Comment'))
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=STATUS_PENDING)
    author = models.ForeignKey(User)
    creation_timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Reports Comments')
        verbose_name_plural = _('Reports Comments')
        db_table = 'report_reports_comments'


class ReportMedia(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='medias')
    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))
    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, verbose_name=_('Type'))
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('URL'))
    file = models.FileField(upload_to=get_content_file_path, blank=True, verbose_name=_('File'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.description, self.media_type)

    class Meta:
        verbose_name = _('Report Media')
        verbose_name_plural = _('Reports Medias')
        db_table = 'report_report_medias'
