from django.db import models
from django.utils.translation import ugettext_lazy as _

from voicesofyouth.core.models import BaseModel
from voicesofyouth.projects.models import Project


class Tag(BaseModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.CharField(max_length=60, null=False, blank=False, verbose_name=_('Name'))

    system_tag = models.BooleanField(default=False, verbose_name=_('System Tag'))

    urgency_score = models.IntegerField(verbose_name=_('Urgency Score'), blank=False, default=0)

    def __str__(self):
        return self.name
