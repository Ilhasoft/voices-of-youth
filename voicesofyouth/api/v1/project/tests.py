import tempfile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from unipath import Path
from PIL import Image

from voicesofyouth.projects.models import Project
from voicesofyouth.users.models import User


class ProjectTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        img = Image.new('RGB', (100, 100), 255)
        tmp_img = tempfile.NamedTemporaryFile(suffix='.jpg')
        img.save(tmp_img)
        tmp_img.seek(0)
        cls.data = {
            'name': 'Project X',
            'thumbnail': tmp_img
        }
        cls.url = reverse('projects-list')
        cls.admin_credentials = {'username': 'admin', 'password': 'Un1c3f@@'}
        cls.user_credentials = {'username': 'user', 'password': 'user'}
        cls.admin = User.objects.get(username='admin')
        cls.user = User.objects.create_user(**cls.user_credentials, email='a@a.com')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_without_data(self):
        response = self.client.get(self.url)
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_with_data(self):
        mommy.make(Project, 10)
        response = self.client.get(self.url)
        self.assertEqual(Project.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_post_without_authentication(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_with_admin_authentication(self):
        self.client.login(**self.admin_credentials)
        self.assertEqual(Project.objects.count(), 0)
        response = self.client.post(self.url, self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
