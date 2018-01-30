from django.views.generic.base import TemplateView

from voicesofyouth.report.models import NOTIFICATION_STATUS_PENDING, NOTIFICATION_STATUS_REVALUTION
from voicesofyouth.report.models import ReportNotification


class NotificationsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = ReportNotification.objects.filter(status__in=[NOTIFICATION_STATUS_PENDING, NOTIFICATION_STATUS_REVALUTION]).filter(read=False).distinct()

        return context
