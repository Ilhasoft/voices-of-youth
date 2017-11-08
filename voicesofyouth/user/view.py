from django.views.generic.base import TemplateView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mappers'] = MapperUser.objects.all()
        return context
