# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 18:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations

__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


def create_dev_data(apps, schema_editor):
    if settings.DEBUG:
        import random
        from unipath import Path
        from django.core.files.images import ImageFile
        from model_mommy import mommy
        from voicesofyouth.project.models import Project
        from voicesofyouth.theme.models import Theme
        from voicesofyouth.theme.models import ThemeTranslation

        test_img = Path(__file__).absolute().ancestor(3).child('test', 'assets', 'python.png')
        with open(test_img, 'rb') as image:
            tags = ('trash',
                    'healthy',
                    'security',
                    'harzadous area',
                    'climate changes',
                    'star wars',
                    'crazy',
                    'anything')
            fake_thumbnail = ImageFile(image)
            for x in range(random.randint(5, 15)):
                project = mommy.make(Project, name=f'Project {x}', thumbnail=fake_thumbnail)
                for y in range(random.randint(5, 15)):
                    theme = mommy.make(Theme, project=project, name=f'Theme {y}')
                    theme.tags.add(*random.choices(tags, (len(t) for t in tags), k=random.randint(1, 6)))
                    theme.translations.add(*mommy.make(ThemeTranslation, random.randint(1, 5), theme=theme))


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('project', '0003_auto_20171023_1317'),
        ('theme', '0004_auto_20171020_1711'),
        ('tag', '0003_auto_20171020_1840')
    ]

    operations = [
        migrations.RunPython(create_dev_data)
    ]
