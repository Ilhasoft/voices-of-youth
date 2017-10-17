from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from model_mommy import mommy

from voicesofyouth.core.models import PROTECTED_GROUPS
from voicesofyouth.core.models import SUPER_ADMIN_GROUP
from voicesofyouth.core.models import LOCAL_ADMIN_GROUP_TEMPLATE
from voicesofyouth.core.models import MAPPER_GROUP_TEMPLATE


__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'
__credits__ = ['Elton Pereira', 'Eduardo Douglas']
__status__ = 'Development'


User = get_user_model()


class GroupProtectedTestCase(TestCase):
    def test_delete(self):
        """
        Protected groups cannot be deleted?
        """
        for protected_group in PROTECTED_GROUPS:
            try:
                with transaction.atomic():
                    group = Group.objects.get(name=protected_group)
                    group.delete()
                    self.fail('Delete an protected group is allowed!')
            except ValidationError:
                pass

    def test_edit(self):
        """
        Protected groups cannot be edited?
        """
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                group = Group.objects.get(name=protected_group)
                group.name = 'foo'
                group.save()

    def test_duplicate(self):
        """
        Duplicate protected groups raises an exception?
        """
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                mommy.make(Group, name=protected_group)
                self.fail('Duplicate protected group is allowed!')

    def test_duplicate_is_case_insensitive(self):
        """
        Duplicate protected groups is case insensitive?
        """
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                mommy.make(Group, name=protected_group.upper())

    def test_change_permission(self):
        """
        We can change permissions from protected groups?
        """
        for protected_group in PROTECTED_GROUPS:
            group = Group.objects.get(name=protected_group)
            group.permissions.add(*Permission.objects.all())

    def test_fake_edit(self):
        """
        We can call save without modifications in protected group?
        """
        for protected_group in PROTECTED_GROUPS:
            group = Group.objects.get(name=protected_group)
            group.save()


class GroupUnprotectedTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.group = mommy.make(Group, name='Unprotected user')

    def test_delete(self):
        """"""
        self.assertEqual(Group.objects.all().count(), 6)
        self.group.delete()
        self.assertEqual(Group.objects.all().count(), 5)

    def test_edit(self):
        """"""
        self.group.name = 'foo'
        self.group.save()
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'foo')


class SuperAdminGroupTestCase(TestCase):
    def test_add_user_in_superadmin_group(self):
        """
        When add an user to super admin group, the flag is_superuser is set to True?
        """
        group = Group.objects.get(name__iexact=SUPER_ADMIN_GROUP)
        user = mommy.make(User)
        self.assertFalse(user.is_superuser)
        user.groups.add(group)
        self.assertTrue(user.is_superuser)

    def test_remove_user_from_superadmin_group(self):
        """
        When remove an user from super admin group, the flag is_superuser is set to False?
        """
        group = Group.objects.get(name__iexact=SUPER_ADMIN_GROUP)
        user = mommy.make(User)
        user.groups.add(group)
        self.assertTrue(user.is_superuser)
        user.groups.remove(group)
        self.assertFalse(user.is_superuser)


class GroupLocalAdminTemplateTestCase(TestCase):
    def test_group_exists(self):
        """
        Template group local admin exists?
        """
        self.assertTrue(Group.objects.filter(name=LOCAL_ADMIN_GROUP_TEMPLATE).exists())


class GroupMapperTemplateTestCase(TestCase):
    def test_group_exists(self):
        """
        Template group mapper exists?
        """
        self.assertTrue(Group.objects.filter(name=MAPPER_GROUP_TEMPLATE).exists())
