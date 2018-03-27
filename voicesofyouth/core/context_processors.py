from voicesofyouth.report.models import NOTIFICATION_STATUS_PENDING, NOTIFICATION_STATUS_REVALUTION
from voicesofyouth.report.models import ReportNotification


def notifications(request):
    if 'admin' in request.path and hasattr(request.user, 'projects'):
        return {'notifications': ReportNotification.objects
                .filter(status__in=[NOTIFICATION_STATUS_PENDING, NOTIFICATION_STATUS_REVALUTION])
                .filter(read=False)
                .filter(report__theme__project__in=request.user.projects).order_by('-modified_on').distinct()}
    return {}
