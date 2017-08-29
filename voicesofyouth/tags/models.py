from django.db import models
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

from voicesofyouth.countries.models import Country


class Tag(SmartModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    name = models.CharField(max_length=60, null=False, blank=False, verbose_name=_('Name'))

    system_tag = models.BooleanField(default=False, verbose_name=_('Enabled'))

    urgency_score = models.IntegerField(verbose_name=_('Urgency Score'), blank=False, default=0)
