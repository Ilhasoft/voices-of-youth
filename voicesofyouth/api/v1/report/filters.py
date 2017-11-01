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
    theme = filters.NumberFilter(name='report__theme')

    class Meta:
        model = ReportFile
        fields = ('theme', 'report')


class ReportCommentFilter(filters.FilterSet):
    class Meta:
        model = ReportComment
        fields = ('report', )


class ReportURLFilter(filters.FilterSet):
    class Meta:
        model = ReportURL
        fields = ('report', )


class ReportMediaFilter(filters.FilterSet):
    report = filters.NumberFilter(name='id')

    class Meta:
        model = Report
        fields = ('id', )
