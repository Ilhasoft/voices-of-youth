from django import template

from voicesofyouth.theme.models import Theme

register = template.Library()

@register.filter
def theme_project_pk(theme):
    if not isinstance(theme, Theme):
        theme = Theme.objects.get(pk=theme)
    return theme.project.pk
