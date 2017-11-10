from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query_utils import Q
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
)


class VoyUser(AbstractUser):
    '''
    Attributes:
        language: Default language of user.
        avatar: User avatar.
    '''
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    avatar = models.IntegerField(choices=AVATARS, default=DEFAULT_AVATAR)

    @cached_property
    def is_mapper(self):
        return self.groups.filter(name__contains='- mappers').exists()

    @property
    def reports(self):
        return self.report_report_creations.all()

    @property
    def themes(self):
        from voicesofyouth.theme.models import Theme
        return Theme.objects.filter(mappers_group__user=self)

    @property
    def projects(self):
        from voicesofyouth.project.models import Project
        return Project.objects.filter(themes__in=self.themes).distinct()


class MapperUserManager(models.Manager):
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


class LocalAdminUserManager(models.Manager):
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


class GlobalAdminUserManager(models.Manager):
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
