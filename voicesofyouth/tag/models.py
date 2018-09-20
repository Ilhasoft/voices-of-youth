from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from taggit.managers import _TaggableManager
from taggit.models import Tag


Tag._meta.ordering = ['name']


class InvalidTag(Exception):
    pass


class _ReportTaggableManager(_TaggableManager):
    def _to_tag_model_instances(self, tags):
        tag_objs = super(_ReportTaggableManager, self)._to_tag_model_instances(tags)
        instance = self.instance
        ct_project = ContentType.objects.get_for_model(instance.theme.project._meta.model)
        ct_theme = ContentType.objects.get_for_model(instance.theme._meta.model)
        qs_tags = Tag.objects.filter(Q(taggit_taggeditem_items__content_type=ct_theme,
                                       taggit_taggeditem_items__object_id=instance.theme.id) |
                                     Q(taggit_taggeditem_items__content_type=ct_project,
                                       taggit_taggeditem_items__object_id=instance.theme.project.id))
        for tag in tag_objs:
            if not qs_tags.filter(taggit_taggeditem_items__tag__name=tag).exists():
                raise InvalidTag()
        return tag_objs
