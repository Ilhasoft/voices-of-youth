from django.conf import settings as django_settings
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel


class Project(SmartModel):

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name'))

    path = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Path'))

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    def __str__(self):
        return self.name


class Setting(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    location = gismodels.PolygonField(null=False, blank=False)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')


class SettingLanguage(SmartModel):

    settings = models.ForeignKey(Setting)

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Project Title'))

    description = models.TextField(null=True, blank=True, verbose_name=_('Project Description'))

    window_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Window Title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Settings Languages')
        verbose_name_plural = _('Settings Languages')
        db_table = 'projects_setting_languages'
