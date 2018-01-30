from django_filters import rest_framework as filters

from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile


class ReportFilter(filters.FilterSet):
    project = filters.NumberFilter(name='theme__project__id', help_text='Filter reports by project id.')
    theme = filters.NumberFilter(name='theme__id', help_text='Filter reports by theme id.')
    mapper = filters.NumberFilter(name='created_by__id', help_text='Filter reports by mapper id.')
    status = filters.NumberFilter(name='status', help_text='Filter reports by status.')

    class Meta:
        model = Report
        fields = ('theme', 'project', 'mapper', 'status')


class ReportFileFilter(filters.FilterSet):
    theme = filters.NumberFilter(name='report__theme',
                                 help_text='Get all files from the all reports linked with the theme id.')
    report = filters.NumberFilter(name='report__id',
                                  help_text='Get all files from the reports id.')
    project = filters.NumberFilter(name='report__theme__project__id',
                                   help_text='Get all files from the project id.')
    media_type = filters.CharFilter(name='media_type',
                                    help_text='Get all files from the media type')

    class Meta:
        model = ReportFile
        fields = ('theme', 'report', 'project', 'media_type')


class ReportCommentFilter(filters.FilterSet):
    report = filters.NumberFilter(name='report__id', help_text='Get all comments from the report id.')

    class Meta:
        model = ReportComment
        fields = ('report', )
