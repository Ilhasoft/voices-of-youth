from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from voicesofyouth.theme.models import Theme
from voicesofyouth.report.models import REPORT_STATUS_PENDING
from voicesofyouth.report.models import Report
from voicesofyouth.report.forms import ReportFilterForm


class ReportView(TemplateView):
    template_name = 'report/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = kwargs['theme']

        context['theme'] = get_object_or_404(Theme, pk=theme_id)
        context['reports'] = Report.objects.filter(theme=context['theme'])
        context['filter_form'] = ReportFilterForm(self, project=context['theme'].project)
        return context


class AddReportView(TemplateView):
    template_name = 'report/add.html'


class PendingReportView(TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(status=REPORT_STATUS_PENDING)[:15]
        return context
