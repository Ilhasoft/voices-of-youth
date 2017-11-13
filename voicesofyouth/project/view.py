from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project


class ProjectView(TemplateView):
    template_name = 'project/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')

        if query:
            context['projects'] = Project.objects.filter(name__icontains=query)
        else:
            context['projects'] = Project.objects.all()

        return context


class AddProjectView(TemplateView):
    template_name = 'project/add.html'
