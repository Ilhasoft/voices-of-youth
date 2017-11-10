from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from voicesofyouth.theme.models import Theme
from voicesofyouth.tag.models import Tag
from voicesofyouth.report.models import REPORT_STATUS_PENDING
from voicesofyouth.report.models import Report
from voicesofyouth.report.forms import ReportFilterForm


class ReportView(TemplateView):
    template_name = 'report/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = kwargs['theme']

        context['theme'] = get_object_or_404(Theme, pk=theme_id)
        form = ReportFilterForm(data=self.request.GET, theme=context['theme'])
        context['filter_form'] = form

        if form.is_valid():
            cleaned_data = form.cleaned_data

            '''if cleaned_data['theme'] is not None:
                context['reports'] = cleaned_data['theme'].reports.all()
            else:
                context['reports'] = Report.objects.filter(theme=context['theme'])'''

            qs_filter = {}
            if cleaned_data['theme'] is not None:
                qs_filter['theme'] = cleaned_data['theme']

            if cleaned_data['tag'] is not None:
                print(cleaned_data['tag'].id)
                qs_filter['tags'] = Tag.objects.get(pk=cleaned_data['tag'].id)

                print(qs_filter)

            context['reports'] = Report.objects.filter(**qs_filter)

            # print(cleaned_data['theme'].reports.all())

        # context['reports'] = Report.objects.filter(theme=context['theme'])

        return context


class AddReportView(TemplateView):
    template_name = 'report/add.html'


class PendingReportView(TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(status=REPORT_STATUS_PENDING)[:15]
        return context
