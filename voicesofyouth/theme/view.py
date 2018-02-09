import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.gis.geos import GEOSGeometry

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.theme.models import THEMES_COLORS
from voicesofyouth.theme.forms import ThemeForm
from voicesofyouth.theme.forms import ThemeTranslationForm


class ThemeView(LoginRequiredMixin, TemplateView):
    template_name = 'theme/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = self.request.user

        if user.is_local_admin and context['project'] not in user.projects:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:projects:index'))

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs['project']

        context['project'] = get_object_or_404(Project, pk=project_id)
        context['themes'] = Theme.objects.filter(project=context['project'])

        return context


class AddThemeView(LoginRequiredMixin, TemplateView):
    template_name = 'theme/form.html'

    def post(self, request, *args, **kwargs):
        project_id = kwargs['project']
        project = get_object_or_404(Project, pk=project_id)

        form = ThemeForm(data=request.POST, project=project)

        if form.is_valid():
            theme = Theme(
                project=Project.objects.get(id=project_id),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                color=form.cleaned_data.get('color')[1:],
                bounds=form.cleaned_data.get('bounds'),
                visible=form.cleaned_data.get('visible'),
                start_at=form.cleaned_data.get('start_at'),
                end_at=form.cleaned_data.get('end_at'),
                allow_links=form.cleaned_data.get('allow_links'),
                created_by=request.user,
                modified_by=request.user
            )
            theme.save()
            theme.tags.add(*form.cleaned_data.get('tags'))
            theme.mappers_group.user_set.add(*form.cleaned_data.get('mappers_group'))

            for translation in form.cleaned_data.get('translations'):
                translation.object_id = theme.id
                translation.save()

            messages.success(request, _('Theme created'))
            return redirect(reverse('voy-admin:themes:index', kwargs={'project': theme.project.id}))
        else:
            context = self.get_context_data()
            context['selected_tags'] = request.POST.getlist('tags')
            context['selected_mappers'] = request.POST.getlist('mappers_group')
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

        context['project'] = get_object_or_404(Project, pk=project_id)
        context['project_bounds'] = json.loads(GEOSGeometry(context['project'].bounds).json)['coordinates']
        context['data_form'] = ThemeForm(project=context['project'])
        context['colors'] = THEMES_COLORS
        context['translate_data_form'] = ThemeTranslationForm(prefix='translate')

        return context


class EditThemeView(LoginRequiredMixin, TemplateView):
    template_name = 'theme/form.html'

    def post(self, request, *args, **kwargs):
        theme_id = kwargs['theme']

        theme = get_object_or_404(Theme, pk=theme_id)
        project = get_object_or_404(Project, pk=theme.project.pk)

        form = ThemeForm(request.POST, project=project)

        if form.is_valid():
            theme.name = form.cleaned_data.get('name')
            theme.description = form.cleaned_data.get('description')
            theme.color = form.cleaned_data.get('color')[1:]
            theme.bounds = form.cleaned_data.get('bounds')
            theme.visible = form.cleaned_data.get('visible')
            theme.start_at = form.cleaned_data.get('start_at')
            theme.end_at = form.cleaned_data.get('end_at')
            theme.allow_links = form.cleaned_data.get('allow_links')

            theme.tags.remove(*theme.tags.all())
            theme.tags.add(*form.cleaned_data.get('tags'))

            theme.mappers_group.user_set.remove(*theme.mappers_group.user_set.all())
            theme.mappers_group.user_set.add(*form.cleaned_data.get('mappers_group'))
            theme.save()

            theme.translations.all().delete()
            for translation in form.cleaned_data.get('translations'):
                translation.object_id = theme.id
                translation.save()

            messages.success(request, _('Theme edited'))
            return redirect(reverse('voy-admin:themes:index', kwargs={'project': theme.project.id}))
        else:
            context = self.get_context_data()
            context['selected_tags'] = request.POST.getlist('tags')
            context['selected_mappers'] = request.POST.getlist('mappers_group')
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
        theme_id = self.kwargs['theme']
        theme = get_object_or_404(Theme, pk=theme_id)

        start_at = None
        end_at = None

        if theme.start_at is not None:
            start_at = theme.start_at.strftime('%d/%m/%Y')

        if theme.end_at is not None:
            end_at = theme.end_at.strftime('%d/%m/%Y')

        data = {
            'name': theme.name,
            'description': theme.description,
            'mappers_group': theme.mappers_group,
            'visible': theme.visible,
            'start_at': start_at,
            'end_at': end_at,
            'color': theme.color,
            'tags': theme.tags.names(),
            'bounds': theme.bounds,
            'allow_links': theme.allow_links,
            'translations': theme.translations.all()
        }

        context['editing'] = True
        context['project'] = theme.project
        context['selected_tags'] = theme.tags.names()
        context['selected_mappers'] = theme.mappers_group.user_set.all().values_list('id', 'username')
        context['project_bounds'] = json.loads(GEOSGeometry(context['project'].bounds).json)['coordinates']
        context['data_form'] = ThemeForm(initial=data, project=context['project'])
        context['colors'] = THEMES_COLORS
        context['translate_data_form'] = ThemeTranslationForm(prefix='translate')

        return context
