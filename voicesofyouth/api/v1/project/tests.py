from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from voicesofyouth.projects.models import Project
from voicesofyouth.users.models import User
from voicesofyouth.test.utils.image import create_fake_image


class ProjectTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'name': 'Project X',
            'thumbnail': create_fake_image()
        }
        cls.project = mommy.make(Project)
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
