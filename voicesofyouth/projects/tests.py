from django.test import TestCase
from django.utils.text import slugify

from model_mommy import mommy

from .models import Project


class ProjectTestCase(TestCase):
    def setUp(self):
        self.project_name = 'Name of project'
        self.project = mommy.make(Project, name=self.project_name)

    def test_set_default_path(self):
        self.assertEqual(self.project.path, slugify(self.project.name))

    def test__str__(self):
        self.assertEqual(str(self.project), self.project_name)
