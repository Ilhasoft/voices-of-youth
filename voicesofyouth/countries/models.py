from django.conf import settings as django_settings
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel


class Country(SmartModel):

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name'))

    path = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Path'))

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')


class Setting(SmartModel):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    location = gismodels.PointField(null=False, blank=False, srid=4326)


class SettingLanguage(SmartModel):

    settings = models.ForeignKey(Setting)

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    project_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Project Title'))

    project_description = models.TextField(null=True, blank=True, verbose_name=_('Project Description'))

    window_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Window Title'))
