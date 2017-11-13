from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from voicesofyouth.theme.models import Theme
from voicesofyouth.report.models import REPORT_STATUS_PENDING
from voicesofyouth.report.models import Report
from voicesofyouth.report.forms import ReportFilterForm


class ReportListView(TemplateView):
    template_name = 'report/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = kwargs['theme']

        context['theme'] = get_object_or_404(Theme, pk=theme_id)

        data = {
            'theme': theme_id,
            'tag': self.request.GET.get('tag'),
            'search': self.request.GET.get('search')
        }

        form = ReportFilterForm(data=data, theme=context['theme'])
        context['filter_form'] = form

        if form.is_valid():
            cleaned_data = form.cleaned_data

            qs_filter = {}
            if cleaned_data['theme'] is not None:
                qs_filter['theme'] = cleaned_data['theme']

            if cleaned_data['tag'] is not None:
                qs_filter['tags'] = cleaned_data['tag']

            if cleaned_data['search'] is not None:
                qs_filter['name__icontains'] = cleaned_data['search']

            context['reports'] = Report.objects.filter(**qs_filter)

        return context


class ReportView(TemplateView):
    template_name = 'report/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_id = kwargs['report']

        context['report'] = get_object_or_404(Report, pk=report_id)
        context['theme'] = context['report'].theme

        return context


class AddReportView(TemplateView):
    template_name = 'report/add.html'


class PendingReportView(TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(status=REPORT_STATUS_PENDING)[:15]
        return context
