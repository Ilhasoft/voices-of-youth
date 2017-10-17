from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connection

from model_mommy import mommy

from voicesofyouth.core.models import PROTECTED_GROUPS
from voicesofyouth.core.models import SUPER_ADMIN_GROUP


__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'
__credits__ = ['Elton Pereira', 'Eduardo Douglas']
__status__ = 'Development'


User = get_user_model()


class BaseGroupTestCase(TestCase):
    def tearDown(self):
        self.clear_group_table()

    def setUp(self):
        self.clear_group_table()

    def clear_group_table(self):
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {Group._meta.db_table}')


class GroupProtectedTestCase(BaseGroupTestCase):
    def test_delete(self):
        '''
        Protected groups cannot be deleted?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                group = mommy.make(Group, name=protected_group)
                group.delete()

    def test_edit(self):
        '''
        Protected groups cannot be edited?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                group = mommy.make(Group, name=protected_group)
                group.name = 'foo'
                group.save()

    def test_duplicate(self):
        '''
        Duplicate protected groups raises an exception?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                mommy.make(Group, name=protected_group)
                mommy.make(Group, name=protected_group)

    def test_duplicate_is_case_insensitive(self):
        '''
        Duplicate protected groups is case insensitive?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError):
                mommy.make(Group, name=protected_group.lower())
                mommy.make(Group, name=protected_group.upper())


class GroupUnprotectedTestCase(BaseGroupTestCase):
    def setUp(self):
        super().setUp()
        self.group = mommy.make(Group, name='Unprotected user')

    def test_delete(self):
        '''
        Unprotected group can be deleted?
        '''
        self.assertEqual(Group.objects.all().count(), 1)
        self.group.delete()
        self.assertEqual(Group.objects.all().count(), 0)

    def test_edit(self):
        '''
        Unprotected group can be edited?
        '''
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
