import tempfile

from PIL import Image
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from voicesofyouth.projects.models import Project
from voicesofyouth.users.models import User


def create_fake_image():
    img = Image.new('RGB', (100, 100), 255)
    tmp_img = tempfile.NamedTemporaryFile(suffix='.jpg')
    img.save(tmp_img)
    tmp_img.seek(0)
    return tmp_img


class ProjectTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'name': 'Project X',
            'thumbnail': create_fake_image()
        }
        cls.url_list = reverse_lazy('projects-list')
        cls.admin_credentials = {'username': 'admin', 'password': 'Un1c3f@@'}
        cls.user_credentials = {'username': 'user', 'password': 'user'}
        cls.admin = User.objects.get(username='admin')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Project.objects.all().delete()
        self.project = mommy.make(Project)
        self.url_detail = reverse_lazy('projects-detail', args=[self.project.id, ])
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
