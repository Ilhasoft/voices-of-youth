from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.gis.geos import GEOSGeometry
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.theme.forms import ThemeForm


class ThemeView(TemplateView):
    template_name = 'theme/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs['project']

        context['project'] = get_object_or_404(Project, pk=project_id)
        context['themes'] = Theme.objects.filter(project=context['project'])

        return context


class AddThemeView(TemplateView):
    template_name = 'theme/form.html'

    def post(self, request, *args, **kwargs):
        project_id = kwargs['project']
        context = self.get_context_data()
        context['project'] = get_object_or_404(Project, pk=project_id)

        form = ThemeForm(data=request.POST, project=context['project'])
        context['selected_tags'] = request.POST.getlist('tags')

        if request.POST.get('boundary') == '':
            messages.error(request, _('Set a boundary'))

        if form.is_valid():
            boundary = 'POLYGON(( {0}))'.format(form.cleaned_data.get('boundary')[:-1])

            theme = Theme(
                project=Project.objects.get(id=project_id),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                color=form.cleaned_data.get('color')[1:],
                bounds=GEOSGeometry(boundary, srid=4326),
                visible=form.cleaned_data.get('visible'),
                start_at=form.cleaned_data.get('start_at'),
                end_at=form.cleaned_data.get('end_at'),
                created_by=request.user,
                modified_by=request.user
            )
            theme.save()
            theme.tags.add(*[tag for tag in form.cleaned_data.get('tags')])
            theme.mappers_group.user_set.add(*form.cleaned_data.get('mappers_group'))

            messages.success(request, _('Theme created'))
            return redirect(reverse('voy-admin:themes:index', kwargs={'project': theme.project.id}))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddThemeView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project']

        context['project'] = get_object_or_404(Project, pk=project_id)
        context['data_form'] = ThemeForm(data=self.request.POST, project=context['project']) if self.request.method == 'POST' else ThemeForm(project=context['project'])

        return context


class EditThemeView(TemplateView):
    template_name = 'theme/form.html'

    '''def post(self, request, *args, **kwargs):
        project_id = kwargs['project']
        context = self.get_context_data()
        context['project'] = get_object_or_404(Project, pk=project_id)

        form = ThemeForm(data=request.POST, project=context['project'])
        context['selected_tags'] = request.POST.getlist('tags')

        if request.POST.get('boundary') == '':
            messages.error(request, _('Set a boundary'))

        if form.is_valid():
            boundary = 'POLYGON(( {0}))'.format(form.cleaned_data.get('boundary')[:-1])

            theme = Theme(
                project=Project.objects.get(id=project_id),
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                color=form.cleaned_data.get('color')[1:],
                bounds=GEOSGeometry(boundary, srid=4326),
                visible=form.cleaned_data.get('visible'),
                start_at=form.cleaned_data.get('start_at'),
                end_at=form.cleaned_data.get('end_at'),
                created_by=request.user,
                modified_by=request.user
            )
            theme.save()
            theme.tags.add(*[tag for tag in form.cleaned_data.get('tags')])
            theme.mappers_group.user_set.add(*form.cleaned_data.get('mappers_group'))

            messages.success(request, _('Theme created'))
            return redirect(reverse('voy-admin:themes:index', kwargs={'project': theme.project.id}))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddThemeView, self).render_to_response(context)'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = self.kwargs['theme']

        try:
            theme = get_object_or_404(Theme, pk=theme_id)

            data = {
                'name': theme.name,
                'description': theme.description,
                'mappers_group': theme.mappers_group,
                'visible': theme.visible,
                'start_at': theme.start_at.strftime('%d/%m/%Y'),
                'end_at': theme.end_at.strftime('%d/%m/%Y'),
                'color': theme.color,
                'tags': theme.tags.names(),
                'boundary': theme.coordinates
            }

            context['editing'] = True
            context['project'] = theme.project
            context['selected_tags'] = theme.tags.names()
            context['selected_mappers'] = theme.mappers_group.user_set.all().values_list('id', 'username')
            context['data_form'] = ThemeForm(initial=self.request.POST, project=context['project']) if self.request.method == 'POST' else ThemeForm(initial=data, project=context['project'])
        except Exception:
            return HttpResponse(status=500)

        return context
