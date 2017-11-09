import uuid

from django.conf import settings as django_settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models as gismodels
from django.db import models
from django.db.models.query_utils import Q
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from unipath import Path

from voicesofyouth.core.models import BaseModel
from voicesofyouth.core.models import LOCAL_ADMIN_GROUP_TEMPLATE
from voicesofyouth.core.utils import resize_image
from voicesofyouth.tag.models import Tag
from voicesofyouth.translation.fields import CharFieldTranslatable
from voicesofyouth.translation.fields import TextFieldTranslatable
from voicesofyouth.translation.models import Translation

__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


def upload_to(instance, filename):
    '''
    Calculate user avatar upload path dynamically.
    '''
    PROJECT_UUID = uuid.uuid5(uuid.NAMESPACE_OID, instance.name)
    FILE_UUID = uuid.uuid5(uuid.NAMESPACE_OID, filename)
    FILE_EXT = Path(filename).ext
    return f'projects/{PROJECT_UUID}/thumbnail/{FILE_UUID}{FILE_EXT}'


class Project(BaseModel):
    """
    The project can aggregate many types of study themes.

    e.g. We can create a project called Brazil issues, and inside of this we can create many themes,
    like waste issues, health issues and so on.

    Another example is a global climate changes, we create a project called Global Climate
    changes 2017 with one big theme.

    Attributes:
        name: Name of project.
        path: URL path for the project. The default value is slug of name.
        language: Default language. If the user doesn't set the main language we use that language.
        window_title: Title that appear in browser window.
        local_admin_group: Vinculates the local admin group for that project. This field is managed by the system.
    """
    name = CharFieldTranslatable(max_length=100, verbose_name=_('Name'))
    description = TextFieldTranslatable(null=True, blank=True, verbose_name=_('Description'))
    path = models.CharField(max_length=100,
                            null=True,
                            blank=True,
                            unique=True,
                            verbose_name=_('URL Path'))
    language = models.CharField(max_length=90,
                                choices=django_settings.LANGUAGES,
                                default='en',
                                verbose_name=_('Language'))
    window_title = CharFieldTranslatable(max_length=256,
                                         null=True,
                                         blank=True,
                                         verbose_name=_('Window Title'))
    local_admin_group = models.OneToOneField(Group, related_name='project_local_admin', null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_to)
    boundary = gismodels.PolygonField()
    translations = GenericRelation(Translation)
    tags = TaggableManager(through=Tag, blank=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        db_table = 'project_projects'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    @property
    def all_tags(self):
        ct_project = ContentType.objects.get_for_model(self._meta.model)
        ct_theme = ContentType.objects.get_for_model(self.themes.model)
        return Tag.objects.filter(Q(content_type=ct_theme, object_id__in=[i[0] for i in self.themes.values_list('id')]) |
                                  Q(content_type=ct_project, object_id=self.id)).distinct()


###############################################################################
# Signals handlers
###############################################################################

@receiver(pre_save, sender=Project)
def set_project_path(sender, instance, **kwargs):
    """
    If user don't set the project path, we use the slugify version of name.
    """
    if not instance.path:
        instance.path = slugify(instance.name)

@receiver(pre_save, sender=Project)
def set_project_window_title(sender, instance, **kwargs):
    """
    If user don't set the window title, we use the project.name.
    """
    if not instance.window_title:
        instance.window_title = instance.name

@receiver(post_save, sender=Project)
def create_project_local_admin_group(sender, instance, **kwargs):
    """
    Creates a group for local administrators and associates it with the project(instance)
    """
    if not instance.local_admin_group:
        # We cant use instance.name because group name cannot have more than 80 characters.
        instance.local_admin_group = Group.objects.get_or_create(name=f'Project({instance.id}) - local admins')[0]
        for perm in Group.objects.get(name=LOCAL_ADMIN_GROUP_TEMPLATE).permissions.all():
            instance.local_admin_group.permissions.add(perm)
        instance.save()

@receiver(m2m_changed, sender=Group.permissions.through)
def change_group_permission(instance, action, model, pk_set, **_):
    """
    When we change the template local admin group permissions, replicate to all projects.local_admin_group.
    """
    for project in Project.objects.filter(local_admin_group__isnull=False):
        if action == 'post_add' and not project.local_admin_group.permissions.filter(id__in=pk_set).exists():
            project.local_admin_group.permissions.add(*model.objects.filter(id__in=pk_set))
        elif action == 'post_remove' and project.local_admin_group.permissions.filter(id__in=pk_set).exists():
            project.local_admin_group.permissions.remove(*model.objects.filter(id__in=pk_set))

@receiver(post_save, sender=Project)
def resize_thumbnail(sender, instance, **kwargs):
    if instance.thumbnail:
        size = 139, 139
        resize_image(instance.thumbnail.file.name, size)
