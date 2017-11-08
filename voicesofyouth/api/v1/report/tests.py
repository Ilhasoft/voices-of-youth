from collections import OrderedDict

from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework_gis.fields import GeoJsonDict

from voicesofyouth.project.models import Project
from voicesofyouth.report.models import Report
from voicesofyouth.report.models import ReportComment
from voicesofyouth.theme.models import Theme
from voicesofyouth.user.models import AVATARS
from voicesofyouth.user.models import DEFAULT_AVATAR
from voicesofyouth.user.models import User


class ReportTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_list = reverse_lazy('reports-list')
        cls.admin_credentials = {'username': 'admin', 'password': 'Un1c3f@@'}
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
        self.maxDiff = None
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
                                       ('avatar', f'http://testserver{AVATARS[DEFAULT_AVATAR - 1][1]}'),
                                       ('username', 'admin'),
                                       ('is_mapper', False)
                                       ]),
            'editable': True,
            'visible': True,
            'description': 'Report description',
            'name': 'Report name',
            'last_image': None}
        self.assertGreater(len(returned_data.pop('created_on')), 0)
        self.assertGreater(len(returned_data.pop('theme_color')), 0)
        self.assertEqual(len(returned_data.pop('tags')), 0)
        self.assertDictEqual(expected_data, returned_data)

    def test_patch_report(self):
        """
        We can patch a report?
        """
        self.assertEqual(Report.objects.count(), 1)
        response = self.client.patch(self.url_detail, data={'name': 'Patched name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Report.objects.count(), 1)
        self.report.refresh_from_db()
        self.assertEqual(self.report.name, 'Patched name')

    def test_put_report(self):
        """
        We can put a report?
        """
        self.assertEqual(Report.objects.count(), 1)
        data = self.client.get(self.url_detail).data
        data['name'] = 'Patched name'
        data['description'] = 'Some description'
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Report.objects.count(), 1)
        self.report.refresh_from_db()
        self.assertEqual(self.report.name, 'Patched name')
        self.assertEqual(self.report.description, 'Some description')

    def test_delete_report(self):
        """
        We can delete a report?
        """
        self.assertEqual(Report.objects.count(), 1)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Report.objects.count(), 0)


class TestReportComment(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.url_list = reverse_lazy('report-comments-list')
        cls.report = mommy.make(Report)
        cls.url_detail = reverse_lazy('report-comments-detail', args=[cls.report.id, ])
        cls.user = User.objects.create_user('user', password='MyP4ssw0rd', first_name='Authenticated', last_name='User')
        cls.user_credentials = {'username': 'user', 'password': 'MyP4ssw0rd'}

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_anonymous_comment(self):
        """
        We can create an anonymous comment?
        """
        self.maxDiff = None
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(ReportComment.objects.count(), 0)
        data = {
            'report': self.report.id,
            'text': 'Report commentary.',
        }
        response = self.client.post(self.url_list, data=data)
        returned_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            'report': self.report.id,
            'created_by': OrderedDict([('id', 2),
                                       ('first_name', 'Guest'),
                                       ('last_name', ''),
                                       ('language', 'en'),
                                       ('avatar', f'http://testserver{AVATARS[DEFAULT_AVATAR - 1][1]}'),
                                       ('username', 'guest'),
                                       ('is_mapper', False)
                                       ]),
            'text': 'Report commentary.'
        }
        self.assertGreater(returned_data.pop('id'), 0)
        self.assertGreater(len(returned_data.pop('created_on')), 0)
        self.assertGreater(len(returned_data.pop('modified_on')), 0)
        self.assertDictEqual(returned_data, expected_data)

    def test_create_authenticated_comment(self):
        """
        We can create a comment with authenticated user?
        """
        self.maxDiff = None
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(ReportComment.objects.count(), 0)
        data = {
            'report': self.report.id,
            'text': 'Report authenticated commentary.',
        }
        self.client.login(**self.user_credentials)
        response = self.client.post(self.url_list, data=data)
        returned_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {
            'report': self.report.id,
            'created_by': OrderedDict([('id', self.user.id),
                                       ('first_name', self.user.first_name),
                                       ('last_name', self.user.last_name),
                                       ('language', 'en'),
                                       ('avatar', f'http://testserver{self.user.get_avatar_display()}'),
                                       ('username', self.user.username),
                                       ('is_mapper', False)
                                       ]),
            'text': 'Report authenticated commentary.'
        }
        self.assertGreater(returned_data.pop('id'), 0)
        self.assertGreater(len(returned_data.pop('created_on')), 0)
        self.assertGreater(len(returned_data.pop('modified_on')), 0)
        self.assertDictEqual(returned_data, expected_data)
