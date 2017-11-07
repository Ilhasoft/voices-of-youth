from django.test import TestCase
from model_mommy import mommy
from taggit.models import CommonGenericTaggedItemBase
from taggit.models import TaggedItemBase

from voicesofyouth.project.models import Project
from voicesofyouth.report.models import Report
from voicesofyouth.tag.models import InvalidTag
from voicesofyouth.tag.models import Tag
from voicesofyouth.theme.models import Theme


class TagTestCase(TestCase):
    def test_property_name(self):
        """
        Tag name property is correct?
        """
        tag_name = 'tag abc'
        tag = mommy.make(Tag, tag__name=tag_name)
        self.assertEqual(str(tag.name), tag_name)

    def test_base_classes(self):
        self.assertTrue(issubclass(Tag, (CommonGenericTaggedItemBase, TaggedItemBase)))


class ReportTagManager(TestCase):
    def test_with_valid_theme_tag(self):
        self.assertEqual(Tag.objects.count(), 0)
        theme = mommy.make(Theme)
        theme.tags.add('tag_theme')
        report = mommy.make(Report, theme=theme)
        report.tags.add('tag_theme')
        self.assertEqual(report.tags.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)

    def test_with_valid_project_tag(self):
        self.assertEqual(Tag.objects.count(), 0)
        project = mommy.make(Project)
        project.tags.add('tag_project')
        theme = mommy.make(Theme, project=project)
        theme.tags.add('tag_theme')
        report = mommy.make(Report, theme=theme)
        report.tags.add('tag_theme', 'tag_project')
        self.assertEqual(report.tags.count(), 2)
        self.assertEqual(Tag.objects.count(), 4)

    def test(self):
        self.assertEqual(Tag.objects.count(), 0)
        project = mommy.make(Project)
        project.tags.add('tag_project')
        theme = mommy.make(Theme, project=project)
        theme.tags.add('tag_theme')
        report = mommy.make(Report, theme=theme)
        report.tags.add('tag_theme', 'tag_project')
        with self.assertRaises(InvalidTag):
            report.tags.add('invalid_tag')
        self.assertEqual(report.tags.count(), 2)
        self.assertEqual(Tag.objects.count(), 4)
