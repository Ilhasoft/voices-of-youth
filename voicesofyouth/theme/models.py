import random

from django.conf import settings as django_settings
from django.contrib.auth.models import Group
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


class Theme(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bounds = gismodels.PolygonField()
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    mappers_group = models.OneToOneField(Group,
                                         related_name='theme_mappers',
                                         null=True,
                                         blank=True,
                                         limit_choices_to={'name__icontains': '- mappers'})
    description = models.TextField(null=True, blank=True)
    tags = TaggableManager(through=Tag, blank=True)
    color = models.CharField(max_length=6,
                             validators=[MinLengthValidator(6), ],
                             null=True,
                             blank=True)

    class Meta:
        ordering = ('name', )
        unique_together = ('project', 'name')

    def __str__(self):
        return self.name

    @property
    def reports(self):
        queryset = self.theme_reports.filter(theme=self, visibled=True).filter(status=1)
        return queryset

    @property
    def reports_count(self):
        return self.reports.count()


class ThemeTranslation(BaseModel):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = _('Themes Translation')
        verbose_name_plural = _('Themes Translations')
        db_table = 'themes_theme_translation'
        ordering = ('language', )
        unique_together = ('theme', 'language')


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
