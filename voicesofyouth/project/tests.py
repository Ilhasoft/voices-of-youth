from PIL import Image
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.files.images import ImageFile
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.text import slugify
from model_mommy import mommy
from unipath import Path

from voicesofyouth.core.models import LOCAL_ADMIN_GROUP_TEMPLATE
from .models import Project
from .models import ProjectTranslation


class ProjectTestCase(TestCase):
    def setUp(self):
        self.project_name = 'Name of project'
        self.project = mommy.make(Project, name=self.project_name)

    def test_with_path_none(self):
        '''
        When path is None we use slugify version of project.name?
        '''
        self.assertEqual(self.project.path, slugify(self.project.name))

    def test__str__(self):
        self.assertEqual(str(self.project), self.project_name)

    def test_duplicate_project_name(self):
        '''
        Project name is unique?
        '''
        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name)
                self.fail('Duplicate project name is allowed!')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name.lower())
                self.fail('Duplicate project name(lower case) is allowed!')
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                mommy.make(Project, name=self.project_name.upper())
                self.fail('Duplicate project name(upper case) is allowed!')
        except IntegrityError:
            pass

    def test_with_window_title_none(self):
        '''
        When window_title is None we use project name as default value?
        '''
        self.assertEqual(self.project.window_title, self.project.name)

    def test_thumbnail_resize(self):
        """
        The thumbnail file are resized when saving?
        """
        test_img = Path(__file__).absolute().ancestor(2).child('test', 'assets', 'python.png')
        with self.settings(MEDIA_ROOT='/tmp'), open(test_img, 'rb') as image:
            fake_thumbnail = ImageFile(image)
            project = mommy.make(Project, thumbnail=fake_thumbnail)
            resized = Image.open(project.thumbnail.file)
            self.assertEqual(resized.size, (139, 139))


class ProjectTranslationTestCase(TestCase):
    def setUp(self):
        self.project = mommy.make(Project)
        self.project_language = mommy.make(ProjectTranslation, name='Test project', language='US')

    def test__str__(self):
        self.assertEqual('Test project(US)', str(self.project_language))


class ProjectLocalAdminGroupTestCase(TestCase):
    def setUp(self):
        self.project = mommy.make(Project)

    def test_local_admin_group_name(self):
        """
        When we create a new project, your local admin group is created?
        """
        self.assertEqual(self.project.local_admin_group.name, f'Project({self.project.id}) - local admins')

    def test_local_admin_group_get_permissions_from_template_group(self):
        """
        When we create a new local admin group, he get the permissions from template group?
        """
        template_group = Group.objects.get(name=LOCAL_ADMIN_GROUP_TEMPLATE)
        for perm in Permission.objects.all()[0:10]:
            template_group.permissions.add(perm)
        project = mommy.make(Project)
        self.assertListEqual(list(project.local_admin_group.permissions.all()),
                             list(template_group.permissions.all()))

    def test_add_permission_in_local_admin_template_group_is_replicated(self):
        """
        When add a new permission to local admin template group, this will replicate to local admin groups?
        """
        template_group = Group.objects.get(name=LOCAL_ADMIN_GROUP_TEMPLATE)
        for perm in Permission.objects.all()[0:10]:
            template_group.permissions.add(perm)
        project = mommy.make(Project)
        # Add extra permission
        template_group.permissions.add(Permission.objects.all()[10])
        self.assertListEqual(list(project.local_admin_group.permissions.all()),
                             list(template_group.permissions.all()))

    def test_remove_permission_in_local_admin_template_group_is_replicated(self):
        """
        When remove a new permission from local admin template group, this will replicate to local admin groups?
        """
        template_group = Group.objects.get(name=LOCAL_ADMIN_GROUP_TEMPLATE)
        template_group.permissions.add(*Permission.objects.all()[0:10])
        project = mommy.make(Project)
        # remove some permissions
        template_group.permissions.remove(*Permission.objects.all()[5:10])
        self.assertListEqual(list(project.local_admin_group.permissions.all()),
                             list(template_group.permissions.all()))
