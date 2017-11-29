import magic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.core.files.images import ImageFile

from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import VoyUser
from voicesofyouth.voyadmin.utils import get_paginator
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import REPORT_STATUS_PENDING
from voicesofyouth.report.models import REPORT_STATUS_APPROVED
from voicesofyouth.report.models import REPORT_STATUS_REJECTED
from voicesofyouth.report.forms import ReportFilterForm
from voicesofyouth.report.forms import ReportForm


class ReportListView(LoginRequiredMixin, TemplateView):
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

            context['reports'] = get_paginator(Report.objects.filter(**qs_filter), page)

        return context


class ReportView(LoginRequiredMixin, TemplateView):
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


class ApproveReportView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        report_id = kwargs['report']
        if report_id:
            report = get_object_or_404(Report, pk=report_id)
            report.status = REPORT_STATUS_APPROVED
            report.save()

            messages.success(request, _('Report approved'))
        return redirect(request.META.get('HTTP_REFERER'))


class CommentsReportView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs['comment']
        status = kwargs['status']
        if comment_id and status:
            comment = get_object_or_404(ReportComment, pk=comment_id)
            comment.status = int(status)
            comment.save()

            messages.success(request, _('Comment {0}'.format('approved' if status == '1' else 'rejected')))
        return redirect(reverse('voy-admin:reports:view', kwargs={'report': comment.report.id}))


class CommentsSaveView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        report_id = kwargs['report']

        if comment and report_id:
            report = get_object_or_404(Report, pk=report_id)
            comment = ReportComment(
                report=report,
                text=comment,
                created_by=request.user,
                modified_by=request.user,
                status=REPORT_STATUS_APPROVED
            )
            comment.save()

            messages.success(request, _('Comment added'))
        return redirect(request.META.get('HTTP_REFERER'))


class AddReportView(LoginRequiredMixin, TemplateView):
    template_name = 'report/form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ReportForm(data=request.POST)
        context['selected_tags'] = request.POST.getlist('tags')

        if form.is_valid():
            mapper = VoyUser.objects.get(id=int(form.cleaned_data.get('mapper')))

            report = Report(
                theme=Theme.objects.get(id=form.cleaned_data.get('theme')),
                name=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                created_by=mapper,
                modified_by=mapper,
                location=form.cleaned_data.get('location'),
                status=REPORT_STATUS_APPROVED
            )
            report.save()
            report.tags.add(*[tag for tag in form.cleaned_data.get('tags')])

            files = request.FILES.getlist('files')

            if files:
                for file in files:
                    mime_type = magic.from_buffer(file.read(), mime=True)
                    if mime_type in ['image/jpeg', 'image/pjpeg', 'image/png', 'image/gif']:
                        media_type = mime_type.split('/')[0]

                        try:
                            report_file = ReportFile(
                                report=report,
                                title=file.name,
                                description=file.name,
                                media_type=media_type,
                                file=ImageFile(file),
                                created_by=mapper,
                                modified_by=mapper
                            )
                            report_file.save()
                        except Exception as e:
                            return HttpResponse(status=500)

            messages.success(request, _('Report created'))
            return redirect(reverse('voy-admin:reports:index', kwargs={'theme': report.theme.id}))
        else:
            messages.error(request, form.non_field_errors())

        return super(AddReportView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_form'] = ReportForm(data=self.request.POST) if self.request.method == 'POST' else ReportForm()
        return context


class EditReportView(LoginRequiredMixin, TemplateView):
    template_name = 'report/form.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ReportForm(data=request.POST)
        context['data_form'] = form
        context['selected_tags'] = request.POST.getlist('tags')
        context['remove_files'] = request.POST.getlist('remove_files[]')

        if form.is_valid():
            try:
                report_id = kwargs['report']
                report = get_object_or_404(Report, pk=report_id)
                mapper = VoyUser.objects.get(id=int(form.cleaned_data.get('mapper')))

                report.name = form.cleaned_data.get('title')
                report.theme = Theme.objects.get(id=form.cleaned_data.get('theme'))
                report.name = form.cleaned_data.get('title')
                report.description = form.cleaned_data.get('description')
                report.created_by = mapper
                report.modified_by = mapper
                report.location = form.cleaned_data.get('location')
                report.tags.add(*[tag for tag in form.cleaned_data.get('tags')])
                report.save()

                files = request.FILES.getlist('files')

                if files:
                    for file in files:
                        mime_type = magic.from_buffer(file.read(), mime=True)
                        if mime_type in ['image/jpeg', 'image/pjpeg', 'image/png', 'image/gif']:
                            media_type = mime_type.split('/')[0]

                            try:
                                report_file = ReportFile(
                                    report=report,
                                    title=file.name,
                                    description=file.name,
                                    media_type=media_type,
                                    file=ImageFile(file),
                                    created_by=mapper,
                                    modified_by=mapper
                                )
                                report_file.save()
                            except Exception as e:
                                return HttpResponse(status=500)

                if context['remove_files'] is not None:
                    ReportFile.objects.filter(id__in=context['remove_files'], report=report).delete()

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
            'location': report.location,
            'tags': report.tags.names(),
        }

        context['editing'] = True
        context['selected_tags'] = report.tags.names()

        context['files_list'] = report.files.all()
        context['data_form'] = ReportForm(initial=self.request.POST) if self.request.method == 'POST' else ReportForm(initial=data)
        return context


class PendingReportView(LoginRequiredMixin, TemplateView):
    template_name = 'report/pending.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        context['reports'] = get_paginator(Report.objects.filter(status=REPORT_STATUS_PENDING), page)

        return context
