from django.test import TestCase

from model_mommy import mommy
from taggit.models import CommonGenericTaggedItemBase
from taggit.models import TaggedItemBase

from voicesofyouth.tag.models import Tag


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
