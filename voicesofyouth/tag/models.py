from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from taggit.models import CommonGenericTaggedItemBase
from taggit.models import TaggedItemBase


class Tag(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)
    urgency_score = models.IntegerField(verbose_name=_('Urgency Score'), default=0)

    @cached_property
    def name(self):
        return self.tag.name
