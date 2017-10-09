from django.conf import settings as django_settings
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

from voicesofyouth.core.models import BaseModel

USER_ADMIN = 1
USER_MAPPER = 2

USER_CHOICES = (
    (USER_ADMIN, _('Local Administrator')),
    (USER_MAPPER, _('Mapper')),
)


class Project(BaseModel):
    '''
    The project can aggregate many types of study themes.

    For example: We can create a project called Brasil issues, and inside of this we can create many themes, like
    waste issues, health issues.

    Another example is a global climate changes, we create a project called Global Climate Changes with one big theme.

    Args:
        name: Name of project.
        description: Description of project.
        path: URL path for the project. The default value is slug of name.
        language: Default language. If the user doesn't set the main language we use that language.
        window_title: Title that appear in browser window.
    '''
    name = models.CharField(max_length=100, verbose_name=_('Name'), unique=True)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=100,
                            null=True,
                            blank=True,
                            verbose_name=_('URL Path'))
    language = models.CharField(max_length=90,
                                choices=django_settings.LANGUAGES,
                                default='en',
                                verbose_name=_('Language'))
    window_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Window Title'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name


class ProjectRegion(BaseModel):
    '''
    Define a region where themes can be created.

    Attributes:
         project: Project linked.
         location: Used to limit the geo location where themes can be created.
    '''
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    region = gismodels.PolygonField()

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        db_table = 'projects_region'

    def __str__(self):
        return self.project.name


class ProjectLanguage(BaseModel):
    '''
    Translations for some fields in project.

    Attributes:
        language: Language
        name: Translation for the Project model field name in the language selected.
        description: Translation for the Project model field description in the language selected.
        window_title: Translation for the Project model field window_title in the language selected.
    '''
    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Project Title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Project Description'))
    window_title = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('Window Title'))

    class Meta:
        verbose_name = _('Project Languages')
        verbose_name_plural = _('Projects Languages')
        db_table = 'projects_languages'

    def __str__(self):
        return f'{self.name}({self.language})'


class ProjectUsers(BaseModel):
    '''
    contrib.auth.models.Group.name.max_length = 80
    '''
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
    if not instance.path:
        instance.path = slugify(instance.name)
