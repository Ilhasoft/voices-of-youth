from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.projects.models import Project


class Map(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name'))

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    bounds = gismodels.PolygonField(null=False, blank=False)
