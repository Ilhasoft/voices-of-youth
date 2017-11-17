from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.gis.geos import GEOSGeometry
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
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            boundary = 'POLYGON(( {0}))'.format(form.cleaned_data.get('boundary')[:-1])

            project = Project(
                name=form.cleaned_data.get('name'),
                path=form.cleaned_data.get('path'),
                description=form.cleaned_data.get('description'),
                language=form.cleaned_data.get('language'),
                boundary=GEOSGeometry(boundary, srid=4326),
                created_by=request.user,
                modified_by=request.user,
                thumbnail=form.cleaned_data.get('thumbnail'),
            )
            project.save()
            project.tags.add(*[tag for tag in form.cleaned_data.get('tags').split(',')])
            project.local_admin_group.user_set.add(*form.cleaned_data.get('local_admin'))

            messages.success(request, _('Project created'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddProjectView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ProjectForm(data=self.request.POST) if self.request.method == 'POST' else ProjectForm()
        return context
