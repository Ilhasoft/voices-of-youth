from django.test import TestCase
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from model_mommy import mommy

from voicesofyouth.core.models import PROTECTED_GROUPS


class GroupProtectedTestCase(TestCase):
    def test_delete(self):
        '''
        Protected groups cannot be deleted?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError), transaction.atomic():
                group = mommy.make(Group, name=protected_group)
                group.delete()

    def test_edit(self):
        '''
        Protected groups cannot be edited?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(ValidationError), transaction.atomic():
                group = mommy.make(Group, name=protected_group)
                group.name = 'foo'
                group.save()

    def test_duplicate(self):
        '''
        Duplicate protected groups raises an exception?
        '''
        for protected_group in PROTECTED_GROUPS:
            with self.assertRaises(IntegrityError), transaction.atomic():
                mommy.make(Group, name=protected_group)
                mommy.make(Group, name=protected_group)


class GroupUnprotectedTestCase(TestCase):
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
