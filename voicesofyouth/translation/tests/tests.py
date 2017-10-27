from django.test import TestCase
from django.test.utils import override_settings

from voicesofyouth.translation.models import TranslatableField, TranslatableModel
from .fake_app.models import FakeModel


class CreateTranslationTestCase(TestCase):

    @override_settings(INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.gis',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
        'smartmin',
        'taggit',
        'voicesofyouth.translation.tests',
        'voicesofyouth.core',
        'voicesofyouth.user',
        'voicesofyouth.project',
        'voicesofyouth.tag',
        'voicesofyouth.theme',
        'voicesofyouth.translation',
    ])
    def setUp(self):
        super().setUp()
        # management.call_command('makemigrations')
        # management.call_command('migrate fake_app')
        # management.call_command('migrate')

    def test_create_translatable_model_on_migration(self):
        """
        TranslatableModel is created when migration runs?
        """
        self.assertEqual(TranslatableModel.objects.filter(model=FakeModel._meta.model_name).count(), 1)

    def test_create_translatable_fields_on_migration(self):
        """
        TranslatableField is created when migration runs?
        """
        trans_model = TranslatableModel.objects.get(model=FakeModel._meta.model_name)
        self.assertEqual(TranslatableField.objects.filter(model=trans_model).count(), 2)
