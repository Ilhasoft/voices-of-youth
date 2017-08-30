from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.countries.models import Country


class Boundary(SmartModel):

    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))

    bounds = gismodels.PolygonField(verbose_name=_('Boundary'))

    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
