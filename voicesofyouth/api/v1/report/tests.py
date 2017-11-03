from collections import OrderedDict

from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework_gis.fields import GeoJsonDict

from voicesofyouth.project.models import Project
from voicesofyouth.report.models import Report
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import User


class ReportTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_list = reverse_lazy('reports-list')
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
        self.theme = mommy.make(Theme,
                                project=self.project1,
                                name='Original name',
                                description='Original description')
        self.report = mommy.make(Report,
                                 theme=self.theme,
                                 name='Test report')
        self.url_detail = reverse_lazy('reports-detail', args=[self.report.id, ])
        self.client.login(**self.admin_credentials)

    def tearDown(self):
        self.client.logout()

    def test_get_without_data(self):
        """
        No reports data return empty array?
        """
        Report.objects.all().delete()
        self.assertEqual(Report.objects.count(), 0)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_new_report(self):
        """
        We can create a new report?
        """
        self.assertEqual(Report.objects.count(), 1)
        data = {
            'theme': self.theme.id,
            'description': 'Report description',
            'name': 'Report name',
            'location': {
                'type': 'Point',
                'coordinates': self.report.location.coords
            }
        }
        response = self.client.post(self.url_list, data=data)
        returned_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            'id': 2,
            'theme': 1,
            'location': GeoJsonDict([('type', 'Point'),
                                     ('coordinates', self.report.location.coords)]),
            'can_receive_comments': True,
            'created_by': OrderedDict([('id', 1),
                                       ('first_name', ''),
                                       ('last_name', ''),
                                       ('language', 'en'),
                                       ('avatar', None),
                                       ('username', 'admin')]),
            'editable': True,
            'visible': True,
            'description': 'Report description',
            'name': 'Report name',
            'tags': [],
            'last_image': None}
        self.assertGreater(len(returned_data.pop('created_on')), 0)
        self.assertGreater(len(returned_data.pop('theme_color')), 0)
        self.assertDictEqual(returned_data, expected_data)
