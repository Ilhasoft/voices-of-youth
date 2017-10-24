from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from voicesofyouth.project.models import Project
from voicesofyouth.test.utils.image import create_fake_image
from voicesofyouth.translation.models import TranslatableField
from voicesofyouth.translation.models import Translation
from voicesofyouth.users.models import User


class ProjectTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'name': 'Project X',
            'thumbnail': create_fake_image()
        }
        cls.project = mommy.make(Project, name='Original name', description='Original description')
        cls.url_list = reverse_lazy('projects-list')
        cls.url_detail = reverse_lazy('projects-detail', args=[cls.project.id, ])
        cls.admin_credentials = {'username': 'admin', 'password': 'Un1c3f@@'}
        cls.user_credentials = {'username': 'user', 'password': 'user'}
        cls.admin = User.objects.get(username='admin')
        cls.user = User.objects.create_user(**cls.user_credentials, email='a@a.com')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.client.login(**self.admin_credentials)

    def tearDown(self):
        self.client.logout()

    def test_get_without_data(self):
        response = self.client.get(self.url_list)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_with_data(self):
        mommy.make(Project, 10)
        response = self.client.get(self.url_list)
        self.assertEqual(Project.objects.count(), 11)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)

    def test_get_apply_translation(self):
        """
        Project translation is applied correctly?
        """
        project = self.project
        field = TranslatableField.objects.get(model__model=project._meta.model_name,
                                              field_name=project._meta.model._meta.get_field('name').attname)
        mommy.make(Translation, field=field, language='pt-br', translation='pt-br name', content_object=project)
        response = self.client.get(f'{self.url_detail}?lang=pt-br')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'pt-br name')
        self.assertEqual(data['description'], 'Original description')
