from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.user.forms import MapperFilterForm
from voicesofyouth.user.models import AdminUser
from voicesofyouth.user.models import MapperUser
from voicesofyouth.voyadmin.utils import get_paginator


def search_user(search_by, qs):
    return qs.filter(Q(username__icontains=search_by) |
                     Q(first_name__icontains=search_by) |
                     Q(last_name__icontains=search_by))


class AdminView(TemplateView):
    template_name = 'user/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = AdminUser.objects.all()
        return context


class MappersListView(TemplateView):
    template_name = 'user/mappers_list.html'
    form_class = MapperFilterForm

    def post(self, request):
        delete = request.POST.get('deleteMappers')
        if delete:
            try:
                MapperUser.objects.filter(id__in=delete.split(',')).delete()
            except Exception:
                return HttpResponse(status=500)
            return HttpResponse("Users deleted!")

    def get(self, request):
        context = self.get_context_data(request=request)
        filter_form = context['filter_form']

        if filter_form.is_valid():
            cleaned_data = filter_form.cleaned_data
            project = cleaned_data['project']
            theme = cleaned_data['theme']
            search = cleaned_data['search']
            page = request.GET.get('page')

            if project and theme and project != theme.project:
                qs = []
            elif theme:
                qs = theme.mappers_group.user_set.all()
            elif project:
                groups_ids = project.themes.values_list('mappers_group__id')
                qs = MapperUser.objects.filter(groups__id__in=groups_ids)
            else:
                qs = MapperUser.objects.all()

            if not isinstance(qs, list) and search:
                qs = search_user(search, qs)
            context['mappers'] = get_paginator(qs, page)

        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mappers'] = MapperUser.objects.all()
        context['projects'] = Project.objects.filter()
        context['filter_form'] = self.form_class(request.GET)
        return context


class MapperDetailView(TemplateView):
    template_name = 'user/mapper_detail.html'
    form_class = MapperFilterForm

    def get(self, request, *args, **kwargs):
        mapper_id = kwargs.get('mapper_id', 0)
        context = self.get_context_data(request=request)
        context['mapper'] = get_object_or_404(MapperUser, pk=mapper_id)
        filter_form = context['filter_form']

        if filter_form.is_valid():
            cleaned_data = filter_form.cleaned_data
            search = cleaned_data['search']
            if search:
                return MappersListView.as_view()(request)

        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class(request.GET)
        return context
