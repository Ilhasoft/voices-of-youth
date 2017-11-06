from django_filters import rest_framework as filters

from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportURL


class ReportFilter(filters.FilterSet):
    project = filters.NumberFilter(name='theme__project__id', help_text='Filter reports by project id.')
    theme = filters.NumberFilter(name='theme__id', help_text='Filter reports by theme id.')

    class Meta:
        model = Report
        fields = ('theme', 'project')


class ReportFileFilter(filters.FilterSet):
    theme = filters.NumberFilter(name='report__theme',
                                 help_text='Get all files from the all reports linked with the theme id.')
    report = filters.NumberFilter(name='id',
                                  help_text='Get all files from the reports id.')
    project = filters.NumberFilter(name='report__theme__project__id',
                                   help_text='Get all files from the project id.')

    class Meta:
        model = ReportFile
        fields = ('theme', 'report', 'project')


class ReportCommentFilter(filters.FilterSet):
    report = filters.NumberFilter(name='report__id', help_text='Get all comments from the report id.')

    class Meta:
        model = ReportComment
        fields = ('report', )


class ReportURLFilter(filters.FilterSet):
    report = filters.NumberFilter(name='report', help_text='Get all URL\'s from the report id.')

    class Meta:
        model = ReportURL
        fields = ('report', )


class ReportMediaFilter(filters.FilterSet):
    report = filters.NumberFilter(name='id', help_text='Get all medias(files and URL\'s) from the report id.')

    class Meta:
        model = Report
        fields = ('report', )
