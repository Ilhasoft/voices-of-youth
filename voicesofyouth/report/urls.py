from django.conf.urls import url

from voicesofyouth.report.view import AddReportView
from voicesofyouth.report.view import EditReportView
from voicesofyouth.report.view import ReportListView
from voicesofyouth.report.view import ReportView
from voicesofyouth.report.view import ApproveReportView
from voicesofyouth.report.view import PendingReportView
from voicesofyouth.report.view import CommentsReportView

urlpatterns = [
    url(r'^(?P<theme>[0-9]+)/$', ReportListView.as_view(), name='index'),
    url(r'^$', ReportListView.as_view(), name='filter'),
    url(r'^new/', AddReportView.as_view(), name='new'),
    url(r'^edit/(?P<report>[0-9]+)', EditReportView.as_view(), name='edit'),
    url(r'^view/(?P<report>[0-9]+)', ReportView.as_view(), name='view'),
    url(r'^approve/(?P<report>[0-9]+)', ApproveReportView.as_view(), name='approve'),
    url(r'^pending/', PendingReportView.as_view(), name='pending'),
    url(r'^comments/(?P<comment>[0-9]+)/(?P<status>[0-9])', CommentsReportView.as_view(), name='comments'),
]
