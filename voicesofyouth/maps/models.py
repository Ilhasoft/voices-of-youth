from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _

from voicesofyouth.core.models import BaseModel
from voicesofyouth.projects.models import Project


class Map(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='maps')
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name'))
    bounds = gismodels.PolygonField(null=False, blank=False)

    def __str__(self):
        return self.name

    def get_themes(self):
        return self.map_themes.all().filter(map__id=self.id)
