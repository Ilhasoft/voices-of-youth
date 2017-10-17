from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from smartmin.models import SmartModel

SUPER_ADMIN_GROUP = 'super admin'
LOCAL_ADMIN_GROUP = 'local admin'
MAPPER_GROUP = 'mapper'
LOCAL_ADMIN_GROUP_TEMPLATE = 'local admin template'
MAPPER_GROUP_TEMPLATE = 'mapper template'
PROTECTED_GROUPS = (
    SUPER_ADMIN_GROUP,
    LOCAL_ADMIN_GROUP,
    MAPPER_GROUP,
    LOCAL_ADMIN_GROUP_TEMPLATE,
    MAPPER_GROUP_TEMPLATE
)


__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


class BaseManager(models.Manager):
    '''
    This manager hide records when is_active flag is active.

    Todo:
        * Instead of delete records, use flag is_active to manage when display them or not. The
          challenge is, how to get related objects to disable them too.
    '''
    def get_queryset(self):
        qs = super(BaseManager, self).get_queryset()
        return qs.filter(is_active=True)


class BaseModel(SmartModel):
    '''
    Default manager used by all VoY models.
    '''
    objects = BaseManager()
    default_objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'default_objects'


####################################################################################################
# Signals
####################################################################################################

@receiver(pre_delete, sender=Group)
def check_delete_protected_group(instance, **kwargs):
    '''
    A protected group cannot be deleted.
    '''
    if instance.name.lower() in PROTECTED_GROUPS:
        msg = _('This is a protected group. You cannot delete a protected group')
        raise ValidationError({'name': msg})

@receiver(pre_save, sender=Group)
def check_add_or_edit_protected_group(instance, sender, **kwargs):
    '''
    A protected group can be added, but cannot be edited.

    Only the name is protected.
    '''
    original_instance = instance
    if instance.pk:
        original_instance = sender.objects.get(id=instance.pk)

    delete = any((original_instance.name.lower() in PROTECTED_GROUPS,
                  sender.objects.filter(name__iexact=instance.name).exists()))

    if original_instance and delete:
        msg = _('This is a protected group. You cannot edit a protected group')
        raise ValidationError({'name': msg})

@receiver(m2m_changed, sender=User.groups.through)
def group_association(instance, action, model, pk_set, **_):
    '''
    When user is linked with super admin group, we set the flag is_superuser. When is removed we do
    the inverse.
    '''
    if model.objects.filter(id__in=pk_set).filter(name__iexact=SUPER_ADMIN_GROUP).count():
        if action == 'post_add':
            instance.is_superuser = True
            instance.save()
        elif action == 'post_remove':
            instance.is_superuser = False
            instance.save()
