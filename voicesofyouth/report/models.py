import os
import uuid
from datetime import datetime

from django.contrib.gis.db import models as gismodels
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from voicesofyouth.core.models import BaseModel
from voicesofyouth.tag.models import _ReportTaggableManager
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import MapperUser


REPORT_STATUS_APPROVED = 1
REPORT_STATUS_PENDING = 2
REPORT_STATUS_NOTAPPROVED = 3

REPORT_COMMENT_STATUS_APPROVED = 1
REPORT_COMMENT_STATUS_PENDING = 2
REPORT_COMMENT_STATUS_REJECTED = 3

REPORT_STATUS_CHOICES = (
    (REPORT_STATUS_APPROVED, _('Approved')),
    (REPORT_STATUS_PENDING, _('Pending')),
    (REPORT_STATUS_NOTAPPROVED, _('Not Approved')),
)

REPORT_COMMENT_STATUS_CHOICES = (
    (REPORT_COMMENT_STATUS_APPROVED, _('Approved')),
    (REPORT_COMMENT_STATUS_PENDING, _('Pending')),
    (REPORT_COMMENT_STATUS_REJECTED, _('Not Approved')),
)

FILE_TYPE_IMAGE = 'image'
FILE_TYPE_VIDEO = 'video'
FILE_TYPES = (
    (FILE_TYPE_IMAGE, _('Image')),
    (FILE_TYPE_VIDEO, _('Video')),
)

FILE_FORMATS = [
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/gif',
    'video/webm',
    'video/mp4'
]

NOTIFICATION_STATUS_APPROVED = 1
NOTIFICATION_STATUS_PENDING = 2
NOTIFICATION_STATUS_NOTAPPROVED = 3
NOTIFICATION_STATUS_REVALUTION = 4

NOTIFICATION_STATUS = [
    (NOTIFICATION_STATUS_APPROVED, _('Approved')),
    (NOTIFICATION_STATUS_PENDING, _('Pending')),
    (NOTIFICATION_STATUS_NOTAPPROVED, _('Not Approved')),
    (NOTIFICATION_STATUS_REVALUTION, _('Revaluation')),
]

NOTIFICATION_ORIGIN_REPORT = 1
NOTIFICATION_ORIGIN_COMMENT = 2

NOTIFICATION_ORIGIN = [
    (NOTIFICATION_ORIGIN_REPORT, _('Report')),
    (NOTIFICATION_ORIGIN_COMMENT, _('Comment'))
]


def unique_filename(filename):
    filename, ext = os.path.splitext(filename)
    fn = ('%s' % uuid.uuid4()).split('-')
    return '%s%s%s' % (fn[-1], fn[-2], ext)


def get_content_file_path(instance, filename):
    filename = unique_filename(filename)
    now = datetime.now()
    return os.path.join('content/%d/%d/%d/' % (now.year, now.month, now.day), filename)


class ReportQuerySet(models.QuerySet):

    def approved(self):
        return self.filter(status=REPORT_STATUS_APPROVED)

    def rejected(self):
        return self.filter(status=REPORT_STATUS_NOTAPPROVED)

    def pending(self):
        return self.filter(status=REPORT_STATUS_PENDING)


class ReportManager(models.Manager):
    def get_queryset(self):
        return ReportQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

    def rejected(self):
        return self.get_queryset().rejected()

    def pending(self):
        return self.get_queryset().pending()


class ReportCommentQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status=REPORT_COMMENT_STATUS_APPROVED)

    def rejected(self):
        return self.filter(status=REPORT_COMMENT_STATUS_REJECTED)

    def pending(self):
        return self.filter(status=REPORT_COMMENT_STATUS_PENDING)


class ReportCommentManager(models.Manager):
    def get_queryset(self):
        return ReportCommentQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

    def rejected(self):
        return self.get_queryset().rejected()

    def pending(self):
        return self.get_queryset().pending()


class Report(BaseModel):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='reports')
    location = gismodels.PointField(null=False, blank=False)
    name = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True)
    can_receive_comments = models.BooleanField(default=True, verbose_name=_('Can receive comments'))
    editable = models.BooleanField(default=True, verbose_name=_('Editable'))
    visible = models.BooleanField(default=True, verbose_name=_('Visible'))
    status = models.IntegerField(verbose_name=_('Status'), choices=REPORT_STATUS_CHOICES, default=REPORT_STATUS_PENDING)
    tags = TaggableManager(blank=True, manager=_ReportTaggableManager)
    objects = ReportManager()

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return '{} - {}'.format(self.theme.project.name, self.theme.name)

    @cached_property
    def project(self):
        return self.theme.project

    @cached_property
    def last_image(self):
        return self.files.filter(media_type=FILE_TYPE_IMAGE).last()

    @cached_property
    def theme_color(self):
        return self.theme.color

    @cached_property
    def comments_views(self):
        return self.comments.filter(status__in=[REPORT_COMMENT_STATUS_APPROVED, REPORT_COMMENT_STATUS_PENDING])

    @property
    def images(self):
        return self.files.filter(media_type=FILE_TYPE_IMAGE)

    @property
    def videos(self):
        return self.files.filter(media_type=FILE_TYPE_VIDEO)


class ReportComment(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=False, blank=False, verbose_name=_('Comment'))
    status = models.IntegerField(verbose_name=_('Status'), choices=REPORT_STATUS_CHOICES, default=REPORT_STATUS_PENDING)
    objects = ReportCommentManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Reports Comments')
        verbose_name_plural = _('Reports Comments')
        db_table = 'report_reports_comments'


class ReportFile(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Title'))
    description = models.TextField(null=False, blank=False, verbose_name=_('Description'))
    file = models.FileField(upload_to=get_content_file_path, blank=True, verbose_name=_('File'))
    media_type = models.CharField(max_length=5, choices=FILE_TYPES, verbose_name=_('Type'))
    thumbnail = models.FileField(upload_to=get_content_file_path, blank=True, verbose_name=_('Thumbnail'))

    class Meta:
        verbose_name = _('Report file')
        verbose_name_plural = _('Reports files')
        db_table = 'report_report_files'


class ReportURL(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='urls')
    url = models.URLField(blank=True, null=True, verbose_name=_('URL'))

    class Meta:
        verbose_name = _('Report URL')
        verbose_name_plural = _('Reports URL\'s')
        db_table = 'report_report_url'

    def __str__(self):
        return self.url


class ReportNotification(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='notifications')
    status = models.IntegerField(choices=NOTIFICATION_STATUS, blank=False, null=False, verbose_name=_('Status'))
    origin = models.IntegerField(choices=NOTIFICATION_ORIGIN, blank=False, null=False, verbose_name=_('Origin'))
    message = models.TextField(null=True, blank=True, verbose_name=_('Message'))
    read = models.BooleanField(default=False, verbose_name=_('Readed'))

    class Meta:
        verbose_name = _('Report Notifications')
        verbose_name_plural = _('Reports Notifications')
        db_table = 'report_report_notification'

    def __str__(self):
        return self.report


###############################################################################
# Signals handlers
###############################################################################

@receiver(pre_save, sender=Report)
def check_user_permission(sender, instance, **kwargs):
    """
    Mapper cannot create report for a theme that he haven't permission.
    """
    if instance.created_by.is_mapper is True:
        mapper = MapperUser.objects.get(id=instance.created_by.id)
        if instance.theme not in mapper.themes:
            msg = _(f'The user "{instance.created_by}" don\'t have permission to create a report for the theme '
                    f'"{instance.theme.name}({instance.theme.id})".')
            raise PermissionDenied(msg)


@receiver(pre_save, sender=Report)
def check_report_within_theme_bounds(sender, instance, **kwargs):
    """
    Report can only be created inside the theme bounds.
    """
    if not instance.theme.bounds.contains(instance.location):
        msg = _(f'You cannot create a report outside the theme bounds.')
        raise ValidationError(msg)


@receiver(post_save, sender=Report)
def send_notification_to_local_admin(sender, instance, **kwargs):
    if instance.created_by.is_mapper is True:
        try:
            notification = ReportNotification.objects.filter(report=instance).first()

            if instance.status == REPORT_COMMENT_STATUS_PENDING:
                notification.status = NOTIFICATION_STATUS_PENDING

            elif instance.status == REPORT_STATUS_NOTAPPROVED:
                notification.status = NOTIFICATION_STATUS_REVALUTION

            notification.read = False
            notification.save()
        except Exception as e:
            ReportNotification.objects.create(
                report=instance,
                status=NOTIFICATION_STATUS_PENDING,
                origin=NOTIFICATION_ORIGIN_REPORT,
                read=False,
                created_by=instance.created_by,
                modified_by=instance.modified_by,
            )
