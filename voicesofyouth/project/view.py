from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import timezone

from voicesofyouth.project.models import Project
from voicesofyouth.project.forms import ProjectForm
from voicesofyouth.project.forms import ProjectTranslationForm


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        project_filter = {}

        if self.request.GET.get('start_at') and self.request.GET.get('end_at'):
            now = timezone.now()
            start_at = self.request.GET.get('start_at', timezone.datetime(now.year, now.month, 1).strftime('%d/%m/%YT%H:%M:%S'))
            end_at = self.request.GET.get('end_at', now.strftime('%d/%m/%YT%H:%M:%S'))

            date_from = datetime.strptime('{0}-{1}-{2}T00:00:00'.format(start_at[6:10],
                                                                        start_at[3:5],
                                                                        start_at[0:2]),
                                          '%Y-%m-%dT%H:%M:%S')
            date_to = datetime.strptime('{0}-{1}-{2}T23:59:59'.format(end_at[6:10],
                                                                      end_at[3:5],
                                                                      end_at[0:2]),
                                        '%Y-%m-%dT%H:%M:%S')

            project_filter['created_on__gte'] = date_from
            project_filter['created_on__lte'] = date_to

            context['start_at'] = start_at
            context['end_at'] = end_at

        if query:
            project_filter['name__icontains'] = query

        user = self.request.user

        if user.is_global_admin:
            context['projects'] = Project.objects.filter(**project_filter).order_by('-created_on')
        else:
            context['projects'] = user.projects.filter(**project_filter).order_by('-created_on')

        return context


class AddProjectView(LoginRequiredMixin, TemplateView):
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
                enabled=form.cleaned_data.get('enabled'),
                enabled_in_signup_form=form.cleaned_data.get('enabled_in_signup_form'),
                created_by=request.user,
                modified_by=request.user,
            )
            project.save()
            project.tags.add(*form.cleaned_data.get('tags').split(','))
            project.local_admin_group.user_set.add(*form.cleaned_data.get('local_admin'))

            for translation in form.cleaned_data.get('translations'):
                translation.object_id = project.id
                translation.save()

            messages.success(request, _('Project created'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            context = self.get_context_data()
            context['data_form'] = form
            messages.error(request, form.non_field_errors())

            return render(request, self.template_name, context)

        return self.get(request)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:projects:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ProjectForm()
        context['translate_data_form'] = ProjectTranslationForm(prefix='translate')
        return context


class EditProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project/form.html'

    def post(self, request, *args, **kwargs):
        project_id = kwargs['project']

        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(request.POST, request.FILES, on_edit=True)

        if form.is_valid():
            project.name = form.cleaned_data.get('name')
            project.path = form.cleaned_data.get('path')
            project.description = form.cleaned_data.get('description')
            project.language = form.cleaned_data.get('language')
            project.bounds = form.cleaned_data.get('bounds')
            project.enabled = form.cleaned_data.get('enabled')
            project.enabled_in_signup_form = form.cleaned_data.get('enabled_in_signup_form')

            if form.cleaned_data.get('thumbnail'):
                project.thumbnail = form.cleaned_data.get('thumbnail')

            project.tags.remove(*project.tags.all())
            project.tags.add(*form.cleaned_data.get('tags').split(','))

            project.local_admin_group.user_set.remove(*project.local_admin_group.user_set.all())
            project.local_admin_group.user_set.add(*form.cleaned_data.get('local_admin'))
            project.save()

            project.translations.all().delete()
            for translation in form.cleaned_data.get('translations'):
                translation.object_id = project.id
                translation.save()

            messages.success(request, _('Project edited'))
            return redirect(reverse('voy-admin:projects:index'))
        else:
            context = self.get_context_data()
            context['data_form'] = form
            messages.error(request, form.non_field_errors())

            return render(request, self.template_name, context)

        return self.get(request)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user
        if user.is_local_admin and context['project'] not in user.projects:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:projects:index'))

        return render(request, self.template_name, context)

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
            'enabled': project.enabled,
            'enabled_in_signup_form': project.enabled_in_signup_form,
            'translations': project.translations.all()
        }

        context['editing'] = True
        context['selected_tags'] = project.all_tags
        context['selected_local_admins'] = project.local_admin_group.user_set.all().values_list('id', 'username')
        context['data_form'] = ProjectForm(initial=data, on_edit=True)

        context['translate_data_form'] = ProjectTranslationForm(prefix='translate')
        context['project'] = project

        return context
