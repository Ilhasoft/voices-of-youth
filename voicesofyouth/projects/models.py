from django.conf import settings as django_settings
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.utils.text import slugify
from django.contrib.auth.models import Group

from voicesofyouth.core.models import BaseModel
from voicesofyouth.core.models import LOCAL_ADMIN_GROUP_TEMPLATE


__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


USER_ADMIN = 1
USER_MAPPER = 2

USER_CHOICES = (
    (USER_ADMIN, _('Local Administrator')),
    (USER_MAPPER, _('Mapper')),
)


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
        local_admin_group: Vinculate the local admin group for that project. This field is managed by the system.
    """
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    path = models.CharField(max_length=100,
                            null=True,
                            blank=True,
                            unique=True,
                            verbose_name=_('URL Path'))
    language = models.CharField(max_length=90,
                                choices=django_settings.LANGUAGES,
                                default='en',
                                verbose_name=_('Language'))
    window_title = models.CharField(max_length=256,
                                    null=True,
                                    blank=True,
                                    verbose_name=_('Window Title'))
    local_admin_group = models.OneToOneField(Group, related_name='project_local_admin', null=True, blank=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name


class ProjectRegion(BaseModel):
    """
    Define a region where themes can be created.

    Attributes:
         project: Project linked.
         region: Delimit the geo location where themes can be created.
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    region = gismodels.PolygonField()

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        db_table = 'projects_region'

    def __str__(self):
        return self.project.name


class ProjectTranslation(BaseModel):
    """
    Translations for some fields in project.

    Attributes:
        language: Language
        name: Translation for the Project model field name in the language selected.
        window_title: Translation for the Project model field window_title in the language selected.
    """
    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Project Title'))
    window_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Window Title'))

    class Meta:
        verbose_name = _('Project Languages')
        verbose_name_plural = _('Projects Languages')
        db_table = 'projects_languages'

    def __str__(self):
        return f'{self.name}({self.language})'


class ProjectUsers(BaseModel):
    """
    contrib.auth.models.Group.name.max_length = 80
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_users')
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.IntegerField(verbose_name=_('Type'), choices=USER_CHOICES)

    class Meta:
        verbose_name = _('Projects Users')
        verbose_name_plural = _('Projects Users')
        db_table = 'projects_project_users'

    def __str__(self):
        return '{} - {}'.format(self.project.name, self.user.display_name)


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
