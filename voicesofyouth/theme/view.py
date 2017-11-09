from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme


class ThemeView(TemplateView):
    template_name = 'theme/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs['project']

        context['project'] = get_object_or_404(Project, pk=project_id)
        context['themes'] = Theme.objects.filter(project=context['project'])

        return context
