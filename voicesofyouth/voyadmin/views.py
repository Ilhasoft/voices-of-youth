from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project


class CoreView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
