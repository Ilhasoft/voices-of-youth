from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.query_utils import Q
from django.urls.base import reverse
from django.utils.functional import cached_property


__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'

DEFAULT_AVATAR = 1
AVATAR_FILE_EXTENSION = '.png'
AVATARS = (
    (1, f'{settings.MEDIA_URL}users/avatars/group-1{AVATAR_FILE_EXTENSION}'),
    (2, f'{settings.MEDIA_URL}users/avatars/group-2{AVATAR_FILE_EXTENSION}'),
    (3, f'{settings.MEDIA_URL}users/avatars/group-3{AVATAR_FILE_EXTENSION}'),
    (4, f'{settings.MEDIA_URL}users/avatars/group-4{AVATAR_FILE_EXTENSION}'),
    (5, f'{settings.MEDIA_URL}users/avatars/group-5{AVATAR_FILE_EXTENSION}'),
    (6, f'{settings.MEDIA_URL}users/avatars/group-6{AVATAR_FILE_EXTENSION}'),
    (7, f'{settings.MEDIA_URL}users/avatars/group-7{AVATAR_FILE_EXTENSION}'),
    (8, f'{settings.MEDIA_URL}users/avatars/group-8{AVATAR_FILE_EXTENSION}'),
    (9, f'{settings.MEDIA_URL}users/avatars/group-9{AVATAR_FILE_EXTENSION}'),
    (10, f'{settings.MEDIA_URL}users/avatars/group-10{AVATAR_FILE_EXTENSION}'),
    (11, f'{settings.MEDIA_URL}users/avatars/group-11{AVATAR_FILE_EXTENSION}'),
    (12, f'{settings.MEDIA_URL}users/avatars/group-12{AVATAR_FILE_EXTENSION}'),
    (13, f'{settings.MEDIA_URL}users/avatars/group-13{AVATAR_FILE_EXTENSION}'),
    (14, f'{settings.MEDIA_URL}users/avatars/group-14{AVATAR_FILE_EXTENSION}'),
    (15, f'{settings.MEDIA_URL}users/avatars/group-15{AVATAR_FILE_EXTENSION}'),
    (16, f'{settings.MEDIA_URL}users/avatars/group-16{AVATAR_FILE_EXTENSION}'),
    (17, f'{settings.MEDIA_URL}users/avatars/group-17{AVATAR_FILE_EXTENSION}'),
    (18, f'{settings.MEDIA_URL}users/avatars/group-18{AVATAR_FILE_EXTENSION}'),
    (19, f'{settings.MEDIA_URL}users/avatars/group-19{AVATAR_FILE_EXTENSION}'),
    (20, f'{settings.MEDIA_URL}users/avatars/group-20{AVATAR_FILE_EXTENSION}'),
    (21, f'{settings.MEDIA_URL}users/avatars/group-21{AVATAR_FILE_EXTENSION}'),
    (22, f'{settings.MEDIA_URL}users/avatars/group-22{AVATAR_FILE_EXTENSION}'),
    (23, f'{settings.MEDIA_URL}users/avatars/group-23{AVATAR_FILE_EXTENSION}'),
    (24, f'{settings.MEDIA_URL}users/avatars/group-24{AVATAR_FILE_EXTENSION}'),
    (25, f'{settings.MEDIA_URL}users/avatars/group-25{AVATAR_FILE_EXTENSION}'),
)


class VoyUser(AbstractUser):
    '''
    Attributes:
        language: Default language of user.
        avatar: User avatar.
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = models.IntegerField(choices=AVATARS, default=DEFAULT_AVATAR)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="%(app_label)s_%(class)s_creations",
                                   null=True,
                                   blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="%(app_label)s_%(class)s_modifications",
                                    null=True,
                                    blank=True)
    modified_on = models.DateTimeField(auto_now=True, editable=False, blank=True)

    @cached_property
    def is_mapper(self):
        return self.groups.filter(name__contains='- mappers').exists()

    @cached_property
    def is_global_admin(self):
        return self.is_superuser

    @cached_property
    def is_local_admin(self):
        return self.groups.filter(name__contains='- local admin').exists()

    @property
    def is_admin(self):
        return self.is_local_admin or self.is_global_admin

    @property
    def reports(self):
        return self.report_report_creations.all()

    @property
    def projects(self):
        from voicesofyouth.project.models import Project
        return Project.objects.filter(local_admin_group__user=self).distinct()

    @property
    def themes(self):
        from voicesofyouth.theme.models import Theme
        return Theme.objects.filter(project__in=self.projects).distinct()

    @property
    def local_admin_of(self):
        """
        Return all projects where this user is local admin.
        """
        # If we put this import in global scope we fall in a circular reference.
        from voicesofyouth.project.models import Project
        return Project.objects.filter(local_admin_group__in=self.groups.all())

    def get_absolute_url(self):
        """
        I try to implements this method directly in MapperUser model but, unfortunately doesn't work on proxy model.
        """
        if self.is_mapper:
            return reverse('voy-admin:users:mapper_detail', args=[self.id, ])
        elif GlobalUserAdmin.is_mapper or LocalUserAdmin.is_mapper:
            return reverse('voy-admin:users:admin_detail', args=[self.id, ])


class MapperUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(groups__name__contains='- mappers').distinct()


class MapperUser(VoyUser):
    """
    Represents a mapper user.
    """
    objects = MapperUserManager()

    class Meta:
        proxy = True
        ordering = ('first_name', 'username',)

    @property
    def themes(self):
        from voicesofyouth.theme.models import Theme
        return Theme.objects.filter(mappers_group__user=self)

    @property
    def projects(self):
        from voicesofyouth.project.models import Project
        return Project.objects.filter(themes__in=self.themes).distinct()


class LocalAdminUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(groups__name__contains='- local admin').distinct()


class LocalUserAdmin(VoyUser):
    """
    Represents a local admin user.
    """
    objects = LocalAdminUserManager()

    class Meta:
        proxy = True


class GlobalAdminUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(is_superuser=True).distinct()


class GlobalUserAdmin(VoyUser):
    """
    Represents a global admin user.
    """
    objects = GlobalAdminUserManager()

    class Meta:
        proxy = True


class AdminUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).filter(Q(is_superuser=True) |
                                                          Q(groups__name__contains='- local admin')).distinct()
        return qs.order_by('-is_superuser')


class AdminUser(VoyUser):
    """
    Represents a admin user(global or local).
    """
    objects = AdminUserManager()

    class Meta:
        proxy = True


# We put this code here to centralize all references to User model.
User = get_user_model()
