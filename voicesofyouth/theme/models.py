import random

from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models as gismodels
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from voicesofyouth.core.models import BaseModel
from voicesofyouth.core.models import MAPPER_GROUP_TEMPLATE
from voicesofyouth.project.models import Project
from voicesofyouth.tag.models import Tag
from voicesofyouth.translation.fields import CharFieldTranslatable
from voicesofyouth.translation.fields import TextFieldTranslatable
from voicesofyouth.translation.models import Translation


class Theme(BaseModel):
    """
    Themes is used to create a study around a theme.

    Theme cannot be created outside of project boundaries.

    Attributes:
        project: Project related to this theme.
        bounds: Boundary for this theme.
        name: Theme name
        mappers_group: Group of mappers.
        description: Description of theme.
        tags: Tags of the theme.
        color: Color used for this theme in front end.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='themes')
    bounds = gismodels.PolygonField()
    name = CharFieldTranslatable(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    mappers_group = models.OneToOneField(Group,
                                         related_name='theme_mappers',
                                         null=True,
                                         blank=True,
                                         limit_choices_to={'name__icontains': '- mappers'})
    description = TextFieldTranslatable(null=True, blank=True)
    tags = TaggableManager(through=Tag, blank=True)
    color = models.CharField(max_length=6,
                             validators=[MinLengthValidator(6), ],
                             null=True,
                             blank=True)
    translations = GenericRelation(Translation)

    class Meta:
        ordering = ('name', )
        unique_together = ('project', 'name')

    def __str__(self):
        return f'{self.name}({self.project})'

    @property
    def reports(self):
        queryset = self.theme_reports.filter(theme=self, visibled=True).filter(status=1)
        return queryset

    @property
    def reports_count(self):
        return self.reports.count()


###############################################################################
# Signals handlers
###############################################################################

@receiver(pre_save, sender=Theme)
def generate_color(sender, instance, **kwargs):
    if not instance.color:
        instance.color = '%06x' % random.randint(0, 0xFFFFFF)

@receiver(post_save, sender=Theme)
def create_theme_mapper_group(sender, instance, **kwargs):
    """
    Creates a group for mappers and associates it with the theme(instance)
    """
    if not instance.mappers_group:
        # We cant use instance.name because group name cannot have more than 80 characters.
        instance.mappers_group = Group.objects.get_or_create(name=f'Theme({instance.id}) - mappers')[0]
        for perm in Group.objects.get(name=MAPPER_GROUP_TEMPLATE).permissions.all():
            instance.mappers_group.permissions.add(perm)
        instance.save()

@receiver(m2m_changed, sender=Group.permissions.through)
def change_group_permission(instance, action, model, pk_set, **_):
    """
    When we change the template mappers group permissions, replicate to all themes.mappers_group.
    """
    for theme in Theme.objects.filter(mappers_group__isnull=False):
        if action == 'post_add' and not theme.mappers_group.permissions.filter(id__in=pk_set).exists():
            theme.mappers_group.permissions.add(*model.objects.filter(id__in=pk_set))
        elif action == 'post_remove' and theme.mappers_group.permissions.filter(id__in=pk_set).exists():
            theme.mappers_group.permissions.remove(*model.objects.filter(id__in=pk_set))
