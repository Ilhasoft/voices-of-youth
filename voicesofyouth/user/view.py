from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.user.forms import AdminFilterForm
from voicesofyouth.user.forms import AdminForm
from voicesofyouth.user.forms import MapperFilterForm
from voicesofyouth.user.forms import MapperForm
from voicesofyouth.user.forms import UserResetPasswordForm
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import AdminUser
from voicesofyouth.user.models import DEFAULT_AVATAR
from voicesofyouth.user.models import MapperUser
from voicesofyouth.voyadmin.utils import get_paginator


def search_user(search_by, qs=None):
    filter = (Q(username__icontains=search_by) |
              Q(first_name__icontains=search_by) |
              Q(last_name__icontains=search_by))
    if qs is None:
        return MapperUser.objects.filter(filter)
    else:
        return qs.filter(filter)


def search_admin(search_by, qs=None):
    filter = (Q(username__icontains=search_by) |
              Q(first_name__icontains=search_by) |
              Q(last_name__icontains=search_by))
    if qs is None:
        return AdminUser.objects.filter(filter)
    else:
        return qs.filter(filter)


def _add_admin(request, admin=None):
    admin = admin or AdminUser()
    form = AdminForm(request.POST)
    error = None
    saved = False
    try:
        saved = form.save(admin)
        if not saved:
            messages.error(request, 'Somethings wrong happened when save the admin user. Please try again!')
        else:
            messages.info(request, 'Admin saved successfully!')
    except IntegrityError as exc:
        error = str(exc).split('\n')[0]
        messages.error(request, error)
    return saved, form, error


class AdminListView(LoginRequiredMixin, TemplateView):
    template_name = 'user/admins_list.html'

    def post(self, request):
        delete = request.POST.get('deleteUsers')
        current_user = request.user
        if delete:
            try:
                if not current_user.is_superuser:
                    return HttpResponseForbidden('Only a global admin can delete admins.')
                else:
                    # The current admin cannot delete yourself.
                    AdminUser.objects.filter(id__in=delete.split(',')).exclude(id=current_user.id).delete()
            except Exception as exc:
                return HttpResponse(str(exc), status=500)
            return HttpResponse("Admin users deleted!")
        else:
            saved, form, error = _add_admin(request)
            if error or not saved:
                context = self.get_context_data()
                context['form_add_admin'] = form
                context['open_modal'] = True
                return render(request, self.template_name, context)

        return self.get(request)

    def get(self, request):
        context = self.get_context_data(request=request)

        user = self.request.user
        if user.is_local_admin:
            messages.error(request, _('Access denied'))
            return redirect(reverse('voy-admin:dashboard'))

        qs = AdminUser.objects.all()
        page = request.GET.get('page')
        search = request.GET.get('search')

        if not isinstance(qs, list):
            qs = qs.order_by('first_name')
            if search:
                qs = search_admin(search, qs)
        elif search:
            qs = search_admin(search)

        context['users'] = get_paginator(qs, page)

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = AdminUser.objects.all()
        context['search_form'] = AdminFilterForm(self.request.GET)
        context['form_add_user'] = AdminForm()
        context['default_avatar'] = AVATARS[DEFAULT_AVATAR][1]
        context['modal_add_title'] = "Add admin"
        context['title'] = "Admins"
        context['avatars'] = AVATARS
        context['post_add_user_url'] = reverse('voy-admin:users:admins_list')
        context['search_form_url'] = reverse('voy-admin:users:admins_list')
        context['delete_users_url'] = reverse('voy-admin:users:admins_list')
        context['list_users_url'] = reverse('voy-admin:users:admins_list')
        context['button_add_new_user'] = True
        return context


class AdminDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user/admin_detail.html'

    def post(self, request, admin_id, *args, **kwargs):
        admin = get_object_or_404(AdminUser, pk=admin_id)

        if request.POST.get('reset_password'):
            form = UserResetPasswordForm(request.POST)
            if (form.is_valid()):
                admin.set_password(form.cleaned_data.get('password'))
                admin.save()
                messages.success(request, 'Password saved with success!')
        else:
            saved, form, error = _add_admin(request, admin)
            if error or not saved:
                context = self.get_context_data(admin_id=admin.id)
                context['form_edit_admin'] = form
                context['open_modal'] = True
                return render(request, self.template_name, context)

        return self.get(request, admin_id=admin.id)

    def get_context_data(self, admin_id, **kwargs):
        context = super().get_context_data(**kwargs)

        admin = get_object_or_404(AdminUser, pk=admin_id)
        data = {
            'username': admin.username,
            'name': admin.get_full_name(),
            'email': admin.email,
            'avatars': admin.avatar
        }
        context['voy_user'] = admin
        context['user_delete_url'] = reverse('voy-admin:users:admin_detail', args=(admin.id, ))
        context['form_edit_user'] = AdminForm(initial=data)
        context['form_add_user'] = AdminForm()
        context['selected_themes'] = admin.themes.values_list('id', flat=True)
        context['form_edit_user_theme'] = admin.themes.all()
        context['users_list_url'] = reverse('voy-admin:users:admins_list')
        context['post_add_user_url'] = reverse('voy-admin:users:admins_list')
        context['button_add_new_user'] = False
        context['form_reset_password_user'] = UserResetPasswordForm()

        return context


class MappersListView(LoginRequiredMixin, TemplateView):
    template_name = 'user/mappers_list.html'
    form_class = MapperFilterForm

    def post(self, request):
        if hasattr(request.POST, 'deleteUsers'):
            delete = request.POST.pop('deleteUsers')
            try:
                MapperUser.objects.filter(id__in=delete.split(',')).delete()
            except Exception:
                return HttpResponse(status=500)
            return HttpResponse("Users deleted!")
        else:
            form = MapperForm(request.POST)
            if form.is_valid():
                mapper = MapperUser()
                form.save(mapper, request.POST.getlist('themes'))
                messages.success(request, 'Mapper saved with success!')
            else:
                messages.error(request, form.errors)

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

            if project and theme:
                qs = MapperUser.objects.filter(groups=theme.mappers_group)
            elif theme:
                qs = theme.mappers_group.user_set.all()
            elif project:
                groups_ids = project.themes.values_list('mappers_group__id')
                qs = MapperUser.objects.filter(groups__id__in=groups_ids)
            else:
                qs = MapperUser.objects.all()

            if not isinstance(qs, list):
                qs = qs.order_by('first_name')
                if search:
                    qs = search_user(search, qs)
            elif search:
                qs = search_user(search)

            context['users'] = get_paginator(qs, page)

        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = MapperUser.objects.all()
        context['projects'] = Project.objects.filter()
        context['filter_form'] = self.form_class(request.GET)
        context['search_form'] = self.form_class(request.GET)
        context['form_add_user'] = MapperForm()
        context['default_avatar'] = AVATARS[DEFAULT_AVATAR][1]
        context['modal_add_title'] = "Add mapper"
        context['title'] = "Mappers"
        context['avatars'] = AVATARS
        context['post_add_user_url'] = reverse('voy-admin:users:mappers_list')
        context['search_form_url'] = reverse('voy-admin:users:mappers_list')
        context['delete_users_url'] = reverse('voy-admin:users:mappers_list')
        context['list_users_url'] = reverse('voy-admin:users:mappers_list')
        context['button_add_new_user'] = True
        return context


class MapperDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user/mapper_detail.html'
    form_filter_class = MapperFilterForm

    def _search_mapper(self, filter_form):
        if filter_form.is_valid():
            cleaned_data = filter_form.cleaned_data
            if cleaned_data['search']:
                return MappersListView.as_view()(self.request)

    def _delete(self, request, mapper):
        mapper.delete()
        messages.success(request, _('Mapper deleted with success!'))
        return HttpResponse(status=200)

    def delete(self, request, *_, **kwargs):
        mapper_id = kwargs.get('mapper_id', 0)
        mapper = get_object_or_404(MapperUser, pk=mapper_id)
        return self._delete(request, mapper)

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
        elif request.POST.get('reset_password'):
            form = UserResetPasswordForm(request.POST)
            if (form.is_valid()):
                mapper.set_password(form.cleaned_data.get('password'))
                mapper.save()
                messages.success(request, 'Password saved with success!')
        else:
            form = MapperForm(request.POST)

            if form.save(mapper, request.POST.getlist('themes')):
                messages.success(request, 'Mapper saved with success!')
            else:
                messages.error(request, 'Somethings wrong happened when save the mapper. Please try again!')
                context = self.get_context_data(request, mapper.id)
                context['user'] = mapper
                context['form_edit_user'] = form
                return render(request, self.template_name, context)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, request, mapper_id, **kwargs):
        context = super().get_context_data(**kwargs)

        mapper = get_object_or_404(MapperUser, pk=mapper_id)
        data = {
            'username': mapper.username,
            'name': mapper.get_full_name(),
            'email': mapper.email,
            'projects': mapper.projects.all(),
            'themes': mapper.themes.all(),
            'avatars': mapper.avatar
        }

        context['filter_form'] = self.form_filter_class(request.GET)
        context['voy_user'] = mapper
        context['user_delete_url'] = reverse('voy-admin:users:mapper_detail', args=(mapper.id, ))
        context['form_edit_user'] = MapperForm(initial=data)
        context['form_edit_user_theme'] = mapper.themes.all()
        context['form_add_user'] = MapperForm()
        context['selected_themes'] = mapper.themes.values_list('id', flat=True)
        context['users_list_url'] = reverse('voy-admin:users:mappers_list')
        context['button_add_new_user'] = False
        context['form_reset_password_user'] = UserResetPasswordForm()

        return context
