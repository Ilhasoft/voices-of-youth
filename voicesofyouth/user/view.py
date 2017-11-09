from django.shortcuts import render
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.user.forms import MapperFilterForm
from voicesofyouth.user.models import AdminUser
from voicesofyouth.user.models import MapperUser


class AdminView(TemplateView):
    template_name = 'user/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = AdminUser.objects.all()
        return context


class MapperView(TemplateView):
    template_name = 'user/mapper.html'
    form_class = MapperFilterForm

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'filter_form': form}

        if form.is_valid():
            cleaned_data = form.cleaned_data
            project = cleaned_data['project']
            theme = cleaned_data['theme']

            if project and theme and project != theme.project:
                context['mappers'] = []
            elif theme:
                context['mappers'] = theme.mappers_group.user_set.all()
            elif project:
                groups_ids = project.themes.values_list('mappers_group__id')
                context['mappers'] = MapperUser.objects.filter(groups__id__in=groups_ids)
            else:
                context['mappers'] = MapperUser.objects.all()

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mappers'] = MapperUser.objects.all()
        context['projects'] = Project.objects.filter()
        context['filter_form'] = MapperFilterForm()
        return context
