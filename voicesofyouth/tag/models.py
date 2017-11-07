from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query_utils import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from taggit.managers import _TaggableManager
from taggit.models import CommonGenericTaggedItemBase
from taggit.models import TaggedItemBase


class InvalidTag(Exception):
    pass


class Tag(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)
    urgency_score = models.IntegerField(verbose_name=_('Urgency Score'), default=0)

    @cached_property
    def name(self):
        return self.tag.name


class _ReportTaggableManager(_TaggableManager):
    def _to_tag_model_instances(self, tags):
        tag_objs = super(_ReportTaggableManager, self)._to_tag_model_instances(tags)
        instance = self.instance
        ct_project = ContentType.objects.get_for_model(instance.theme.project._meta.model)
        ct_theme = ContentType.objects.get_for_model(instance.theme._meta.model)
        qs_tags = Tag.objects.filter(Q(content_type=ct_theme, object_id=instance.theme.id) |
                                     Q(content_type=ct_project, object_id=instance.theme.project.id))
        for tag in tag_objs:
            if not qs_tags.filter(tag__name=tag).exists():
                raise InvalidTag()
        return tag_objs
