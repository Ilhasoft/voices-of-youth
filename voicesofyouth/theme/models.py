from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as gismodels
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query_utils import Q
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
from voicesofyouth.theme.utils import generate_pin
from voicesofyouth.translation.fields import CharFieldTranslatable
from voicesofyouth.translation.fields import TextFieldTranslatable
from voicesofyouth.translation.models import Translation


THEMES_COLORS = [
    'ce6c9d',
    'f08ea5',
    'fea954',
    '559ee6',
    '5bc0e5',
    '72c3b1',
    'ae74e1',
    '9f7de3',
    '8978e9',
    'd163e9',
    '62ae7e',
    '9fcb73',
    'b8ca77',
    'c29267',
    'ea8064',
    'd6bd7d',
    '606b76',
    '8f9aa8',
    '9bb7da'
]


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
        visible: Visible to users.
        allow_links: Allow mappers to add links to reports.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='themes')
    bounds = gismodels.PolygonField(blank=True)
    name = CharFieldTranslatable(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    allow_links = models.BooleanField(default=True, verbose_name=_('Allow mappers to add links to reports'))
    mappers_group = models.OneToOneField(Group,
                                         related_name='theme_mappers',
                                         null=True,
                                         blank=True,
                                         limit_choices_to={'name__icontains': '- mappers'})
    description = TextFieldTranslatable(null=True, blank=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    color = models.SmallIntegerField(null=False, blank=False)
    translations = GenericRelation(Translation)

    class Meta:
        ordering = ('name', )
        unique_together = ('project', 'name')

    def __str__(self):
        return f'{self.name} ({self.project})'

    @property
    def all_tags(self):
        ct_project = ContentType.objects.get_for_model(self.project._meta.model)
        ct_theme = ContentType.objects.get_for_model(self._meta.model)
        return Tag.objects.filter(Q(taggit_taggeditem_items__content_type=ct_theme,
                                    taggit_taggeditem_items__object_id=self.id) |
                                  Q(taggit_taggeditem_items__content_type=ct_project,
                                    taggit_taggeditem_items__object_id=self.project.id)).distinct()

    @property
    def reports(self):
        queryset = self.theme_reports.filter(theme=self, visibled=True).filter(status=1)
        return queryset

    @property
    def reports_count(self):
        return self.reports.approved().count()

    @property
    def coordinates(self):
        return [[bound[1], bound[0]] for bound in self.bounds.coords[0]]

    def get_absolute_url(self):
        return f'not-implemented/{self.id}'

    @property
    def get_color(self):
        if self.color:
            return THEMES_COLORS[self.color]


###############################################################################
# Signals handlers
###############################################################################
@receiver(pre_save, sender=Theme)
def generate_color(sender, instance, **kwargs):
    if not instance.color:
        instance.color = 1
    generate_pin(instance.color, THEMES_COLORS[instance.color])


@receiver(pre_save, sender=Theme)
def set_theme_area(sender, instance, **kwargs):
    """
    Set theme bounds with project bounds if theme bounds is empty.
    """
    if instance.bounds is None:
        instance.bounds = instance.project.bounds


@receiver(pre_save, sender=Theme)
def validate_theme_local_admin(sender, instance, **kwargs):
    """
    Check if user is a local admin of project.
    """
    user = instance.created_by
    if not user.is_global_admin and not instance.project.local_admin_group.user_set.filter(id=user.id).exists():
        raise ValidationError(_('You don\'t have permission to create themes in this project.'))


@receiver(pre_save, sender=Theme)
def validate_theme_area(sender, instance, **kwargs):
    """
    Check if theme bounds is inside the project bounds area.
    """
    if not instance.project.bounds.contains(instance.bounds):
        raise ValidationError(_('You cannot create a theme outside of project bounds.'))


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
