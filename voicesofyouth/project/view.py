from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
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
    template_name = 'project/form.html'

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = Project(
                name=form.cleaned_data.get('name'),
                path=form.cleaned_data.get('path'),
                description=form.cleaned_data.get('description'),
                language=form.cleaned_data.get('language'),
                bounds=form.cleaned_data.get('bounds'),
                thumbnail=form.cleaned_data.get('thumbnail'),
                created_by=request.user,
                modified_by=request.user,
            )
            project.save()
            project.tags.add(*form.cleaned_data.get('tags').split(','))
            project.local_admin_group.user_set.add(*form.cleaned_data.get('local_admin'))

            messages.success(request, _('Project created'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            context = self.get_context_data()
            context['data_form'] = form
            messages.error(request, form.non_field_errors())

            return render(request, self.template_name, context)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ProjectForm()
        return context


class EditProjectView(TemplateView):
    template_name = 'project/form.html'

    def post(self, request, *args, **kwargs):
        project_id = kwargs['project']

        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project.name = form.cleaned_data.get('name')
            project.path = form.cleaned_data.get('path')
            project.description = form.cleaned_data.get('description')
            project.language = form.cleaned_data.get('language')
            project.bounds = form.cleaned_data.get('bounds')
            project.thumbnail = form.cleaned_data.get('thumbnail')

            project.tags.remove(*project.tags.all())
            project.tags.add(*form.cleaned_data.get('tags').split(','))

            project.local_admin_group.user_set.remove(*project.local_admin_group.user_set.all())
            project.local_admin_group.user_set.add(*form.cleaned_data.get('local_admin'))
            project.save()

            messages.success(request, _('Project edited'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            context = self.get_context_data()
            context['data_form'] = form
            messages.error(request, form.non_field_errors())

            return render(request, self.template_name, context)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_id = self.kwargs['project']
        project = get_object_or_404(Project, pk=project_id)

        data = {
            'name': project.name,
            'path': project.path,
            'description': project.description,
            'language': project.language,
            'bounds': project.bounds,
            'thumbnail': project.thumbnail,
        }

        context['editing'] = True
        context['selected_tags'] = project.all_tags
        context['selected_local_admins'] = project.local_admin_group.user_set.all().values_list('id', 'username')
        context['data_form'] = ProjectForm(initial=data)

        return context
