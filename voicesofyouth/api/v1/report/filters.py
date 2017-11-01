from django_filters import rest_framework as filters

from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportFile
from voicesofyouth.report.models import ReportComment


class ReportFilter(filters.FilterSet):
    project = filters.NumberFilter(name='theme__project__id')

    class Meta:
        model = Report
        fields = ('theme', )


class ReportFileFilter(filters.FilterSet):
    theme = filters.NumberFilter(name='report__theme')

    class Meta:
        model = ReportFile
        fields = ('theme', 'report')


class ReportCommentFilter(filters.FilterSet):
    report = filters.NumberFilter(name='report__id')

    class Meta:
        model = ReportComment
        fields = ('report', )
