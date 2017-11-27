from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from voicesofyouth.project.models import Project
from voicesofyouth.voyadmin.forms import LoginForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class LoginView(TemplateView):
    template_name = 'login.html'

    @property
    def _redirect_url(self):
        return self.request.GET.get('next') or reverse('voy-admin:dashboard')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self._redirect_url)
        else:
            return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                url = self._redirect_url
                return redirect(url)
            else:
                form.add_error('username', _('Check your username and retype the password.'))

        return render(request, self.template_name, context={'form': form})

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(reverse('voy-admin:login'))
