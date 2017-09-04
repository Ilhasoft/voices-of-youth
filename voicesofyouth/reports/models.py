from django.conf import settings as django_settings
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.projects.models import Project
from voicesofyouth.maps.models import Map
from voicesofyouth.themes.models import Theme
from voicesofyouth.tags.models import Tag


STATUS_APPROVED = 1
STATUS_PENDING = 2
STATUS_REJECTED = 3

STATUS_CHOICES = (
    (STATUS_APPROVED, _('Approved')),
    (STATUS_PENDING, _('Pending')),
    (STATUS_REJECTED, _('Rejected')),
)


class Report(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    location = gismodels.PointField(null=False, blank=False, srid=4326)

    sharing = models.BooleanField(default=True, verbose_name=_('Sharing'))

    comments = models.BooleanField(default=True, verbose_name=_('Comments'))

    editable = models.BooleanField(default=True, verbose_name=_('Editable'))

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    visibled = models.BooleanField(default=True, verbose_name=_('Visibled'))

    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return '{} - {} - {}'.format(self.project.name, self.map.name, self.theme.name)


class ReportLanguage(SmartModel):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))

    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))

    def __str__(self):
        return '{} - {} - {}'.format(self.language, self.title, self.description)

    class Meta:
        verbose_name = _('Reports Languages')
        verbose_name_plural = _('Reports Languages')


class ReportTags(SmartModel):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

    class Meta:
        verbose_name = _('Reports Tags')
        verbose_name_plural = _('Reports Tags')


class ReportFavoriteBy(SmartModel):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.report.theme.name, self.created_by.display_name)

    class Meta:
        verbose_name = _('Reports Favorite By')
        verbose_name_plural = _('Reports Favorite By')


class ReportComments(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    body = models.TextField(null=False, blank=False, verbose_name=_('Body'))

    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return '{} - {}'.format(self.project.name, self.report.theme.name)

    class Meta:
        verbose_name = _('Reports Comments')
        verbose_name_plural = _('Reports Comments')
