import random

from django.db.utils import IntegrityError
from django.test import TestCase
from django.conf import settings

from model_mommy import mommy

from voicesofyouth.project.models import Project
from voicesofyouth.theme.models import Theme
from voicesofyouth.theme.models import ThemeTranslation


def make_theme_translations(theme=None, quantity=1):
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
        if theme:
            translations.append(mommy.make(ThemeTranslation, theme=theme, language=lang))
        else:
            translations.append(mommy.make(ThemeTranslation, language=lang))
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
        # Unrelated theme translation.
        make_theme_translations(quantity=10)
        make_theme_translations(theme=self.theme, quantity=10)
        self.assertEqual(ThemeTranslation.objects.count(), 20)
        self.assertEqual(self.theme.translations.count(), 10)
        difference = self.theme.translations.order_by('language').difference(
                ThemeTranslation.objects.filter(theme=self.theme).order_by('language'))
        self.assertEqual(difference.count(), 0)

    def test_uniqueness(self):
        """
        Uniqueness of theme is using name and project?
        """
        project = mommy.make(Project)
        mommy.make(Theme, project=project, name='Theme foo')
        with self.assertRaises(IntegrityError):
            mommy.make(Theme, project=project, name='Theme foo')


class ThemeTranslationTestCase(TestCase):
    def setUp(self):
        self.theme = mommy.make(Theme)
        self.theme_translation_language = 'en'
        self.theme_translation = mommy.make(ThemeTranslation, theme=self.theme, language=self.theme_translation_language)

    def test__str__(self):
        """
        String representation of ThemeTranslation is correct?
        """
        self.assertEqual(str(self.theme_translation), self.theme_translation_language)

    def test_uniqueness(self):
        """
        Uniqueness of theme is using name and project?
        """
        translation = make_theme_translations(theme=self.theme, quantity=10)[0]
        with self.assertRaises(IntegrityError):
            mommy.make(ThemeTranslation, theme=translation.theme, language=translation.language)
