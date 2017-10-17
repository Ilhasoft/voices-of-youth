from django.test import TestCase
from django.utils.text import slugify
from django.db.utils import IntegrityError
from django.db import transaction

from model_mommy import mommy

from .models import Project
from .models import ProjectRegion
from .models import ProjectTranslation


class ProjectTestCase(TestCase):
    def setUp(self):
        self.project_name = 'Name of project'
        self.project = mommy.make(Project, name=self.project_name)

    def test_with_path_none(self):
        '''
        When path is None we use slugify version of project.name?
        '''
        self.assertEqual(self.project.path, slugify(self.project.name))

    def test__str__(self):
        self.assertEqual(str(self.project), self.project_name)

    def test_duplicate_project_name(self):
        '''
        Project name is unique?
        '''
        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name)
                self.fail('Duplicate project name is allowed!')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name.lower())
                self.fail('Duplicate project name(lower case) is allowed!')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name.upper())
                self.fail('Duplicate project name(upper case) is allowed!')
        except IntegrityError:
            pass

    def test_with_window_title_none(self):
        '''
        When window_title is None we use project name as default value?
        '''
        self.assertEqual(self.project.window_title, self.project.name)


class ProjectRegionTestCase(TestCase):
    def setUp(self):
        self.project = mommy.make(Project)
        self.project_region = mommy.make(ProjectRegion, project=self.project)

    def test__str__(self):
        self.assertEqual(str(self.project_region), self.project.name)

    def test_duplicate_project_setting(self):
        with self.assertRaises(IntegrityError):
            mommy.make(ProjectRegion, project=self.project)


class ProjectTranslationTestCase(TestCase):
    def setUp(self):
        self.project = mommy.make(Project)
        self.project_language = mommy.make(ProjectTranslation, name='Test project', language='US')

    def test__str__(self):
        self.assertEqual('Test project(US)', str(self.project_language))


class ProjectLocalAdminGroupTestCase(TestCase):
    def setUp(self):
        self.project = mommy.make(Project)

    def test_create_local_admin_group(self):
        """
        When we create a new project, your local admin group is created?
        """
        self.assertIsNotNone(self.project.local_admin_group)
