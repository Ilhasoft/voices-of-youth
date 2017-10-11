from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from voicesofyouth.core.models import BaseModel
from voicesofyouth.projects.models import Project
from voicesofyouth.maps.models import Map
from voicesofyouth.tags.models import Tag
from voicesofyouth.users.models import User


class Theme(BaseModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='map_themes')

    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name'))

    visibled = models.BooleanField(default=True, verbose_name=_('Visibled'))

    cover = models.ImageField(upload_to='cover', null=True, blank=True, verbose_name=_('Cover'))

    mappers = models.ManyToManyField(User, limit_choices_to={'groups__name__iexact': 'super admin'})

    def __str__(self):
        return self.name

    def get_languages(self):
        return self.theme_language.all().filter(theme=self.id)

    def get_tags(self):
        queryset = self.theme_tags.all().filter(theme=self.id)
        return map(lambda tag: tag.tag, queryset)

    def get_total_reports(self):
        return self.theme_reports.all().filter(theme=self.id).count()

    def get_reports(self, limit):
        queryset = self.theme_reports.all().filter(theme=self.id).filter(visibled=True).filter(status=1)

        if limit is not None:
            return queryset[:limit]

        return queryset


class ThemeLanguage(BaseModel):

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme_language')

    language = models.CharField(max_length=90, choices=django_settings.LANGUAGES, default='en')

    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))

    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Themes Languages')
        verbose_name_plural = _('Themes Languages')
        db_table = 'themes_theme_languages'


class ThemeTags(BaseModel):

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='theme_tags')

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.theme.name, self.tag.name)

    class Meta:
        verbose_name = _('Themes Tags')
        verbose_name_plural = _('Themes Tags')
        db_table = 'themes_theme_tags'


class ThemeFavoriteBy(BaseModel):

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.theme.name, self.created_by.display_name)

    class Meta:
        verbose_name = _('Themes Favorite By')
        verbose_name_plural = _('Themes Favorite By')
        db_table = 'themes_theme_favorite_by'
