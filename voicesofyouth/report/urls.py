from django.conf.urls import url

from voicesofyouth.report.view import AddReportView
from voicesofyouth.report.view import ReportListView
from voicesofyouth.report.view import ReportView
from voicesofyouth.report.view import ReportApproveView
from voicesofyouth.report.view import PendingReportView


urlpatterns = [
    url(r'^(?P<theme>[0-9])/$', ReportListView.as_view(), name='index'),
    url(r'^$', ReportListView.as_view(), name='filter'),
    url(r'^new/', AddReportView.as_view(), name='new'),
    url(r'^view/(?P<report>[0-9]+)', ReportView.as_view(), name='view'),
    url(r'^approve/(?P<report>[0-9]+)', ReportApproveView.as_view(), name='approve'),
    url(r'^pending/', PendingReportView.as_view(), name='pending'),
]
