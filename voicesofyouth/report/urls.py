from django.conf.urls import url

from voicesofyouth.report.view import AddReportView
from voicesofyouth.report.view import PendingReportView
from voicesofyouth.report.view import ReportView

urlpatterns = [
    url(r'^(?P<project>[0-9])/$', ReportView.as_view(), name='index'),
    url(r'^new/', AddReportView.as_view(), name='new'),
    url(r'^pending/', PendingReportView.as_view(), name='pending'),
]
