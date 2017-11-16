from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from voicesofyouth.project.models import Project
from voicesofyouth.project.forms import ProjectForm


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

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ProjectForm(data=request.POST)

        if form.is_valid():
            project = Project(
                name=form.cleaned_data.get('name'),
                path=form.cleaned_data.get('path')
            )
            project.save()
            messages.success(request, _('Project created'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddProjectView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ProjectForm(data=self.request.POST) if self.request.method == 'POST' else ProjectForm()
        return context
