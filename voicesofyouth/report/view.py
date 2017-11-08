from django.views.generic.base import TemplateView

from voicesofyouth.report.models import Report


class ReportView(TemplateView):
    template_name = 'report/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all()[:15]
        return context


class AddReportView(TemplateView):
    template_name = 'report/add.html'


class PendingReportView(TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all()[:15]
        return context
