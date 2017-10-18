"""
This module stores the core resources for VoY project.

Groups
======

This module provides 5 default groups, each of then have an specific purpose. Bellow you can see each of these groups,
the top group can do anything that group bellow can.:

* **super admin** - Anyone added to this group becomes a super user, this implies that he can do anything inside the VoY.
* **local admin** - Can create themes and mappers, and, can create an association between these themes and the mappers.
  Local admin cannot create projects.
* **mapper** - Users in these group, can only create or edit your own reports.

Template groups
---------------

The template groups are used as an permissions aggregators, any permission added or removed from any of these template
groups, will be reflected to any group vinculated with then.

* **local admin template** - Permissions for local admins.
* **mapper template** - Permissions for mappers.
"""
from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from smartmin.models import SmartModel

SUPER_ADMIN_GROUP = 'super admin'
LOCAL_ADMIN_GROUP_TEMPLATE = 'local admin template'
MAPPER_GROUP_TEMPLATE = 'mapper template'
PROTECTED_GROUPS = (
    SUPER_ADMIN_GROUP,
    LOCAL_ADMIN_GROUP_TEMPLATE,
    MAPPER_GROUP_TEMPLATE
)


__author__ = ['Elton Pereira', 'Eduardo Douglas']
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


class BaseManager(models.Manager):
    """
    This manager hide records when is_active flag is active.

    Todo:
        * Instead of delete records, use flag is_active to manage when display them or not. The
          challenge is, how to get related objects to disable them too.
    """
    def get_queryset(self):
        qs = super(BaseManager, self).get_queryset()
        return qs.filter(is_active=True)


class BaseModel(SmartModel):
    """
    Default manager used by all VoY models.
    """
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
    """
    A protected group cannot be deleted.
    """
    if instance.name.lower() in PROTECTED_GROUPS:
        msg = _('This is a protected group. You cannot delete a protected group')
        raise ValidationError({'name': msg})

@receiver(pre_save, sender=Group)
def check_add_or_edit_protected_group(instance, sender, **kwargs):
    """
    A protected group can be added, but cannot be edited.

    Only the name is protected. The user can modify permissions freely.
    """
    original_instance = instance
    if instance.pk:
        original_instance = sender.objects.get(id=instance.pk)

    protected_group = original_instance.name.lower() in PROTECTED_GROUPS
    name_changed = original_instance.name != instance.name

    # Edit an protected group.
    if (name_changed and protected_group):
        msg = _('This is a protected group. You cannot edit a protected group')
        raise ValidationError({'name': msg})

    # Changing the group name conflicts with an existing group.
    if sender.objects.filter(name__iexact=instance.name).exists() and name_changed:
        msg = _('This group already exists!')
        raise ValidationError({'name': msg})

    # Trying to create an new group with the same name from the group that already exists.
    if sender.objects.filter(name__iexact=instance.name).exists() and not instance.id:
        msg = _('This group already exists!')
        raise ValidationError({'name': msg})

@receiver(m2m_changed, sender=User.groups.through)
def group_association(instance, action, model, pk_set, **__):
    """
    Take care of some business logic about groups.

    When user is linked with super admin group, we set the flag is_superuser, when is removed we do the inverse.
    When try to associated an user is to any template group, we raise the appropriated exception.
    """
    qs = model.objects.filter(id__in=pk_set)

    if qs.filter(name__iexact=SUPER_ADMIN_GROUP).count():
        if action == 'post_add':
            instance.is_superuser = True
            instance.save()
        elif action == 'post_remove':
            instance.is_superuser = False
            instance.save()
    if qs.filter(Q(name__iexact=MAPPER_GROUP_TEMPLATE) | Q(name__iexact=LOCAL_ADMIN_GROUP_TEMPLATE)).count():
        if action == 'pre_add':
            raise ValidationError(_('You cannot add an user to a template group.'))
