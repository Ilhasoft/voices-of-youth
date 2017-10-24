import random

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from voicesofyouth.core.models import MAPPER_GROUP_TEMPLATE
from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.translation.models import Translation


def make_theme_translations(theme, quantity=1):
    """
    Model mommy has a bug with models with unique_together.

    When fixed we can remove this workaround.
    https://github.com/vandersonmota/model_mommy/issues/286
    """
    translations = []
    langs = settings.LANGUAGES.copy()
    for idx in range(quantity):
        lang = random.choice(langs)
        langs.pop(langs.index(lang))
        translations.append(mommy.make(Translation, content_object=theme, language=lang[0]))
    return translations


class ThemeTestCase(TestCase):
    def setUp(self):
        self.theme_name = 'Theme name'
        self.theme = mommy.make(Theme, name=self.theme_name)

    def test__str__(self):
        """
        String representation of Theme is correct?
        """
        self.assertEqual(str(self.theme), self.theme_name)

    def test_reverse_relation_translations(self):
        """
        translations attribute return correct translations?
        """
        make_theme_translations(theme=self.theme, quantity=10)
        self.assertEqual(Translation.objects.count(), 10)
        self.assertEqual(self.theme.translations.count(), 10)
        theme_ct = ContentType.objects.get_for_model(self.theme)
        difference = self.theme.translations.order_by('language').difference(
                Translation.objects.filter(content_type=theme_ct, object_id=self.theme.id).order_by('language'))
        self.assertEqual(difference.count(), 0)

    def test_uniqueness(self):
        """
        Uniqueness of theme is using name and project?
        """
        project = mommy.make(Project)
        mommy.make(Theme, project=project, name='Theme foo')
        with self.assertRaises(IntegrityError):
            mommy.make(Theme, project=project, name='Theme foo')


class ThemeMapperGroupTestCase(TestCase):
    def setUp(self):
        self.theme = mommy.make(Theme)

    def test_mapper_group_name(self):
        """
        When we create a new theme, your mapper group is created?
        """
        self.assertEqual(self.theme.mappers_group.name, f'Theme({self.theme.id}) - mappers')

    def test_mapper_group_get_permissions_from_template_group(self):
        """
        When we create a new mapper group, he get the permissions from template group?
        """
        template_group = Group.objects.get(name=MAPPER_GROUP_TEMPLATE)
        for perm in Permission.objects.all()[0:10]:
            template_group.permissions.add(perm)
        theme = mommy.make(Theme)
        self.assertListEqual(list(theme.mappers_group.permissions.all()),
                             list(template_group.permissions.all()))

    def test_add_permission_in_mapper_template_group_is_replicated(self):
        """
        When add a new permission to mapper template group, this will replicate to mapper groups?
        """
        template_group = Group.objects.get(name=MAPPER_GROUP_TEMPLATE)
        for perm in Permission.objects.all()[0:10]:
            template_group.permissions.add(perm)
        theme = mommy.make(Theme)
        # Add extra permission
        template_group.permissions.add(Permission.objects.all()[10])
        self.assertListEqual(list(theme.mappers_group.permissions.all()),
                             list(template_group.permissions.all()))

    def test_remove_permission_in_local_admin_template_group_is_replicated(self):
        """
        When remove a permission from mapper template group, this will replicate to mapper groups?
        """
        template_group = Group.objects.get(name=MAPPER_GROUP_TEMPLATE)
        template_group.permissions.add(*Permission.objects.all()[0:10])
        theme = mommy.make(Theme)
        # remove some permissions
        template_group.permissions.remove(*Permission.objects.all()[5:10])
        self.assertListEqual(list(theme.mappers_group.permissions.all()),
                             list(template_group.permissions.all()))
