from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.gis.geos import GEOSGeometry

from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import VoyUser
from voicesofyouth.voyadmin.utils import get_paginator
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import REPORT_STATUS_PENDING
from voicesofyouth.report.models import REPORT_STATUS_APPROVED
from voicesofyouth.report.models import REPORT_STATUS_REJECTED
from voicesofyouth.report.forms import ReportFilterForm
from voicesofyouth.report.forms import ReportForm


class ReportListView(TemplateView):
    template_name = 'report/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_id = kwargs['theme']

        context['theme'] = get_object_or_404(Theme, pk=theme_id)

        data = {
            'theme': theme_id,
            'tag': self.request.GET.get('tag'),
            'search': self.request.GET.get('search'),
            'status': self.request.GET.get('status')
        }

        form = ReportFilterForm(data=data, theme=context['theme'])
        context['filter_form'] = form

        if form.is_valid():
            cleaned_data = form.cleaned_data
            page = self.request.GET.get('page')

            qs_filter = {}
            if cleaned_data['theme'] is not None:
                qs_filter['theme'] = cleaned_data['theme']

            if cleaned_data['tag'] is not None:
                qs_filter['tags'] = cleaned_data['tag']

            if cleaned_data['status'] is not '':
                qs_filter['status'] = int(cleaned_data['status'])

            if cleaned_data['search'] is not None:
                qs_filter['name__icontains'] = cleaned_data['search']

            context['reports'] = get_paginator(Report.objects.filter(**qs_filter).order_by('created_on'), page)

        return context


class ReportView(TemplateView):
    template_name = 'report/view.html'

    def post(self, request, *args, **kwargs):
        report_id = request.POST.get('report')
        message = request.POST.get('message')

        if report_id and message:
            try:
                report = get_object_or_404(Report, pk=report_id)
                report.status = REPORT_STATUS_REJECTED
                report.save()

                messages.success(request, _('Report rejected'))
                return redirect(reverse('voy-admin:reports:index', kwargs={'theme': report.theme.id}))
            except Exception:
                return HttpResponse(status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_id = kwargs['report']

        context['report'] = get_object_or_404(Report, pk=report_id)
        context['theme'] = context['report'].theme

        return context


class ReportApproveView(TemplateView):
    def get(self, request, *args, **kwargs):
        report_id = kwargs['report']
        if report_id:
            report = get_object_or_404(Report, pk=report_id)
            report.status = REPORT_STATUS_APPROVED
            report.save()

            messages.success(request, _('Report approved'))
        return redirect(request.META.get('HTTP_REFERER'))


class AddReportView(TemplateView):
    template_name = 'report/form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ReportForm(data=request.POST)
        context['selected_tags'] = request.POST.getlist('tags')

        if request.POST.get('location') == '':
            messages.error(request, _('Set a location'))

        if form.is_valid():
            mapper = VoyUser.objects.get(id=int(form.cleaned_data.get('mapper')))
            location = form.cleaned_data.get('location').split(',')

            report = Report(
                theme=Theme.objects.get(id=form.cleaned_data.get('theme')),
                name=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                created_by=mapper,
                modified_by=mapper,
                location=GEOSGeometry('POINT({0} {1})'.format(location[0], location[1]), srid=4326)
            )
            report.save()
            report.tags.add(*[tag for tag in form.cleaned_data.get('tags')])
            messages.success(request, _('Report created'))
            return redirect(reverse('voy-admin:reports:index', kwargs={'theme': report.theme.id}))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddReportView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ReportForm(data=self.request.POST) if self.request.method == 'POST' else ReportForm()
        return context


class EditReportView(TemplateView):
    template_name = 'report/form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ReportForm(data=request.POST)
        context['data_form'] = form
        context['selected_tags'] = request.POST.getlist('tags')

        if request.POST.get('location') == '':
            messages.error(request, _('Set a location'))

        if form.is_valid():
            try:
                report_id = kwargs['report']
                report = get_object_or_404(Report, pk=report_id)
                mapper = VoyUser.objects.get(id=int(form.cleaned_data.get('mapper')))
                location = form.cleaned_data.get('location').split(',')

                report.name = form.cleaned_data.get('title')
                report.theme = Theme.objects.get(id=form.cleaned_data.get('theme'))
                report.name = form.cleaned_data.get('title')
                report.description = form.cleaned_data.get('description')
                report.created_by = mapper
                report.modified_by = mapper
                report.location = GEOSGeometry('POINT({0} {1})'.format(location[0], location[1]), srid=4326)
                report.tags.add(*[tag for tag in form.cleaned_data.get('tags')])
                report.save()

                messages.success(request, _('Report edited'))
                return redirect(reverse('voy-admin:reports:index', kwargs={'theme': report.theme.id}))
            except Exception:
                return HttpResponse(status=500)
        else:
            messages.error(request, form.non_field_errors())

        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_id = self.kwargs['report']
        report = get_object_or_404(Report, pk=report_id)

        data = {
            'title': report.name,
            'description': report.description,
            'project': report.theme.project.id,
            'theme': report.theme.id,
            'mapper': report.created_by.id,
            'location': '{0},{1}'.format(report.location[0], report.location[1]),
            'tags': report.tags.names(),
        }

        context['editing'] = True
        context['selected_tags'] = report.tags.names()
        context['data_form'] = ReportForm(initial=self.request.POST) if self.request.method == 'POST' else ReportForm(initial=data)
        return context


class PendingReportView(TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context['reports'] = get_paginator(Report.objects.filter(status=REPORT_STATUS_PENDING), page)

        return context
