from django.db import models
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.projects.models import Project


class Tag(SmartModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.CharField(max_length=60, null=False, blank=False, verbose_name=_('Name'))

    system_tag = models.BooleanField(default=False, verbose_name=_('Enabled'))

    urgency_score = models.IntegerField(verbose_name=_('Urgency Score'), blank=False, default=0)
