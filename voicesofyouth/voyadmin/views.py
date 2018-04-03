import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.utils import timezone
from taggit.models import Tag

from voicesofyouth.project.models import Project
from voicesofyouth.report.models import Report
from voicesofyouth.user.models import MapperUser
from voicesofyouth.voyadmin.forms import LoginForm
from voicesofyouth.voyadmin.utils import radial_bar_round_down

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        projects = Project.objects.all() \
            if self.request.user.is_global_admin else \
            self.request.user.projects
        all_reports = Report.objects.filter(theme__project__in=projects)
        last_week = timezone.now() - datetime.timedelta(days=7)
        week_reports = all_reports.filter(created_on__gte=last_week)
        last_month = timezone.now() - datetime.timedelta(days=30)
        monthly_reports = all_reports.filter(created_on__gte=last_month)

        groups_ids = projects.values_list('themes__mappers_group', flat=True)
        all_mappers = MapperUser.objects.filter(groups__id__in=groups_ids)

        week_approved_reports = week_reports.approved()
        week_pending_reports = week_reports.pending()

        ct_project = ContentType.objects.get_for_model(Project)
        all_tags = Tag.objects.filter(taggit_taggeditem_items__content_type=ct_project,
                                      taggit_taggeditem_items__object_id__in=projects)
        top_tags = all_tags \
            .annotate(items_count=Count('taggit_taggeditem_items')) \
            .order_by('-items_count')[:10]  # show top 10

        approved_percent = int(week_approved_reports.count() / week_reports.count() * 100)
        pending_percent = int(week_pending_reports.count() / week_reports.count() * 100)

        top_mappers = MapperUser.objects.filter(
            report_report_creations__in=monthly_reports) \
            .annotate(report_count=Count('report_report_creations')) \
            .order_by('-report_count')[:5]

        context['projects'] = projects
        context['all_reports'] = all_reports
        context['all_mappers'] = all_mappers
        context['top_tags'] = top_tags
        context['week_reports'] = week_reports
        context['week_approved_reports'] = week_approved_reports
        context['week_pending_reports'] = week_pending_reports
        context['approved_percent'] = approved_percent
        context['pending_percent'] = pending_percent
        context['radial_bar_approved_percent'] = radial_bar_round_down(approved_percent)
        context['radial_bar_pending_percent'] = radial_bar_round_down(pending_percent)
        context['latest_approved_reports'] = all_reports.approved()[:5]
        context['top_mappers'] = top_mappers
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
            if user is not None and user.is_mapper is False:
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
