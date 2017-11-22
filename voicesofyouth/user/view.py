from django.contrib import messages
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.user.forms import AdminFilterForm
from voicesofyouth.user.forms import AdminForm
from voicesofyouth.user.forms import MapperFilterForm
from voicesofyouth.user.forms import MapperForm
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import AdminUser
from voicesofyouth.user.models import DEFAULT_AVATAR
from voicesofyouth.user.models import MapperUser
from voicesofyouth.voyadmin.utils import get_paginator


def search_user(search_by, qs):
    return qs.filter(Q(username__icontains=search_by) |
                     Q(first_name__icontains=search_by) |
                     Q(last_name__icontains=search_by))


class AdminListView(TemplateView):
    template_name = 'user/admin_list.html'

    def post(self, request):
        # delete = request.POST.get('deleteMappers')
        # if delete:
        #     try:
        #         MapperUser.objects.filter(id__in=delete.split(',')).delete()
        #     except Exception:
        #         return HttpResponse(status=500)
        #     return HttpResponse("Users deleted!")
        # else:
        form = AdminForm(request.POST)
        if form.is_valid():
            admin = AdminUser()
            try:
                form.save(admin)
            except IntegrityError as exc:
                messages.error(request, str(exc).split('\n')[0])
                context = self.get_context_data()
                context['form_add_admin'] = form
                return render(request, self.template_name, context)
        else:
            messages.error(request, 'Somethings wrong happened when save the admin user. Please try again!')
            context = self.get_context_data()
            context['form_add_admin'] = form
            context['open_modal'] = True
            return render(request, self.template_name, context)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = AdminUser.objects.all()
        context['filter_form'] = AdminFilterForm(self.request.GET)
        context['form_add_admin'] = AdminForm()
        context['default_avatar'] = AVATARS[DEFAULT_AVATAR][1]
        return context


class AdminDetailView(TemplateView):
    template_name = 'user/admin_detail.html'


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
        else:
            form = MapperForm(request.POST)
            if form.is_valid():
                mapper = MapperUser()
                form.save(mapper)

        return self.get(request)

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
                qs = qs.order_by('first_name')
                qs = search_user(search, qs)
            context['mappers'] = get_paginator(qs, page)

        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mappers'] = MapperUser.objects.all()
        context['projects'] = Project.objects.filter()
        context['filter_form'] = self.form_class(request.GET)
        context['form_add_mapper'] = MapperForm()
        context['default_avatar'] = AVATARS[DEFAULT_AVATAR][1]
        return context


class MapperDetailView(TemplateView):
    template_name = 'user/mapper_detail.html'
    form_filter_class = MapperFilterForm

    def _search_mapper(self, filter_form):
        if filter_form.is_valid():
            cleaned_data = filter_form.cleaned_data
            if cleaned_data['search']:
                return MappersListView.as_view()(request)

    def _delete(self, request, mapper):
        mapper.delete()
        messages.success(request, _('Mapper deleted with success!'))
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        mapper_id = kwargs.get('mapper_id', 0)
        context = self.get_context_data(request=request, mapper_id=mapper_id)
        filter_form = context['filter_form']

        search = self._search_mapper(filter_form)
        if search:
            return search

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        mapper = get_object_or_404(MapperUser, pk=kwargs.get('mapper_id'))

        if request.POST.get('deleteMapper'):
            return self._delete(request, mapper)

        form = MapperForm(request.POST)

        if form.save(mapper):
            messages.success(request, 'Mapper saved with success!')
        else:
            messages.error(request, 'Somethings wrong happened when save the mapper. Please try again!')
            context = self.get_context_data(request, mapper.id)
            context['mapper'] = mapper
            context['form_edit_mapper'] = form
            return render(request, self.template_name, context)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, request, mapper_id, **kwargs):
        context = super().get_context_data(**kwargs)

        mapper = get_object_or_404(MapperUser, pk=mapper_id)
        data = {
            'username': mapper.username,
            'name': mapper.get_full_name(),
            'email': mapper.email,
            'project': mapper.projects.last(),
            'themes': mapper.themes.all(),
            'avatars': mapper.avatar
        }
        context['filter_form'] = self.form_filter_class(request.GET)
        context['mapper'] = mapper
        context['form_edit_mapper'] = MapperForm(initial=data)
        context['form_add_mapper'] = MapperForm()
        context['selected_themes'] = mapper.themes.values_list('id', flat=True)

        return context
