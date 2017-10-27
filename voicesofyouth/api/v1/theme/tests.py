from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from voicesofyouth.project.models import Project
from voicesofyouth.test.utils.image import create_fake_image
from voicesofyouth.theme.models import Theme
from voicesofyouth.translation.models import TranslatableField
from voicesofyouth.translation.models import Translation
from voicesofyouth.user.models import User


class ThemeTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'name': 'Project X',
            'thumbnail': create_fake_image()
        }
        cls.url_list = reverse_lazy('themes-list')
        cls.admin_credentials = {'username': 'admin', 'password': 'Un1c3f@@'}
        cls.user_credentials = {'username': 'user', 'password': 'user'}
        cls.admin = User.objects.get(username='admin')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Project.objects.all().delete()
        Theme.objects.all().delete()
        self.project1 = mommy.make(Project)
        self.project2 = mommy.make(Project)
        self.theme = mommy.make(Theme,
                                project=self.project1,
                                name='Original name',
                                description='Original description')
        mommy.make(Theme,
                   project=self.project2,
                   _quantity=9)
        self.url_list = reverse_lazy('themes-list')
        self.url_detail = reverse_lazy('themes-detail', args=[self.theme.id, ])
        self.client.login(**self.admin_credentials)

    def tearDown(self):
        self.client.logout()

    def test_get_without_data(self):
        """
        No themes data return empty array?
        """
        Theme.objects.all().delete()
        self.assertEqual(Theme.objects.count(), 0)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_themes_without_project_id_param(self):
        """
        Cannot get themes without project_id?
        """
        response = self.client.get(self.url_list)
        self.assertEqual(Theme.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_themes_with_project_id_param(self):
        """
        We get themes related with a project_id?
        """
        response = self.client.get(f'{self.url_list}?project={self.project2.id}')
        self.assertEqual(Theme.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 9)

    def test_get_with_translation(self):
        """
        Theme translation is applied correctly?
        """
        theme = self.theme
        field = TranslatableField.objects.get(model__model=theme._meta.model_name,
                                              field_name=theme._meta.model._meta.get_field('name').attname)
        mommy.make(Translation, field=field, language='pt-br', translation='pt-br name', content_object=theme)
        response = self.client.get(f'{self.url_detail}?lang=pt-br')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'pt-br name')
        self.assertEqual(data['description'], 'Original description')
