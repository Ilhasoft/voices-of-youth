# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 18:54
from django.conf import settings
from django.contrib.gis.geos.point import Point
from django.db import migrations

from unipath import Path

__author__ = 'Elton Pereira'
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'

test_img = Path(__file__).absolute().ancestor(3).child('test', 'assets', 'python.png')
user = None


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
        ('translation', '0001_initial'),
        ('project', '0005_auto_20171122_1712'),
        ('theme', '0004_auto_20171121_1406'),
        ('tag', '0001_initial'),
        ('report', '0004_auto_20171110_2008'),
        ('user', '0004_remove_voyuser_created_on'),
    ]

    operations = []


if settings.DEBUG:
    import random

    from django.core.files.images import ImageFile
    from django.db import transaction
    from django.db.utils import IntegrityError

    from voicesofyouth.project.models import Project
    from voicesofyouth.report.models import REPORT_STATUS_CHOICES
    from voicesofyouth.report.models import FILE_TYPES
    from voicesofyouth.report.models import Report
    from voicesofyouth.report.models import ReportComment
    from voicesofyouth.report.models import ReportFile
    from voicesofyouth.report.models import ReportURL
    from voicesofyouth.theme.models import Theme
    from voicesofyouth.translation.fields import CharFieldTranslatable
    from voicesofyouth.translation.fields import TextFieldTranslatable
    from voicesofyouth.translation.models import TranslatableField
    from voicesofyouth.translation.models import Translation
    from voicesofyouth.translation.models import create_translatable_model
    from voicesofyouth.user.models import User

    import lorem
    from model_mommy import mommy
    from model_mommy.random_gen import gen_string

    mommy.generators.add(TextFieldTranslatable, gen_string)
    mommy.generators.add(CharFieldTranslatable, gen_string)

    def make_translation(obj, lang):
        for field in TranslatableField.objects.filter(model__model=obj._meta.model_name):
            current_value = getattr(obj, field.field_name)
            try:
                with transaction.atomic():
                    mommy.make(Translation,
                               field=field,
                               content_object=obj,
                               language=lang,
                               translation=f'{lang} - {lorem.sentence()[:len(current_value) - len(lang)]}')
            except IntegrityError:
                pass


    def make_report_medias(report):
        with open(test_img, 'rb') as image:
            fake_file = ImageFile(image)

            mommy.make(ReportFile,
                       title=lorem.sentence(),
                       description=lorem.paragraph(),
                       report=report,
                       created_by=user,
                       modified_by=user,
                       media_type=random.choice(FILE_TYPES)[0],
                       file=fake_file)

        mommy.make(ReportURL,
                   report=report,
                   created_by=user,
                   modified_by=user,
                   url='https://google.com')


    def create_dev_data(apps, schema_editor):
        global user
        create_translatable_model(Project)
        create_translatable_model(Theme)
        with open(test_img, 'rb') as image, transaction.atomic():
            tags = ('trash',
                    'healthy',
                    'security',
                    'harzadous area',
                    'climate changes',
                    'star wars',
                    'crazy',
                    'anything')
            fake_users = (('Neil', 'Tyson'),
                          ('Albert', 'Einstein'),
                          ('Isaac', 'Newton'),
                          ('Max', 'Planck'),
                          ('Carl', 'Sagan'),
                          ('Stephen', 'Hawking'),
                          ('Nikola', 'Tesla'),
                          ('Galileu', 'Galilei'),
                          ('Charles', 'Darwin'))
            projects_names = (
                'Apollo',
                'Astro',
                'Barracuda',
                'Camelot',
                'Elixir',
                'Firestorm',
                'Phoenix',
                'Nautilus',
                'Sand storm'
            )
            themes_names = (
                'Trash problems',
                'Health problems',
                'Zica virus',
                'Security problems',
                'Hazardous area',
                'Degradation of nature',
                'Pollution',
                'Political negligence',
                'Human rights',
                'Education',
                'Violence, war and conflicts',
                'Employment',
                'Culture',
                'Technology',
                'Governance'
            )
            fake_thumbnail = ImageFile(image)
            users = []
            for i in range(1, 9):
                user = fake_users[i]
                users.append(mommy.make(User,
                                        username=user[1].lower(),
                                        avatar=random.randint(1, 22),
                                        first_name=user[0],
                                        last_name=user[1]))
            for x in range(random.randint(5, 10)):
                user = random.choice(users)
                project_name = random.choice(projects_names)
                while Project.objects.filter(name=project_name).count() > 0:
                    project_name = random.choice(themes_names)
                project = mommy.make(Project,
                                     name=project_name,
                                     thumbnail=fake_thumbnail,
                                     description=lorem.paragraph(),
                                     created_by=user,
                                     modified_by=user)
                project.tags.add(*random.choices(tags, (len(t) for t in tags), k=random.randint(1, 6)))
                for y in range(random.randint(5, 10)):
                    theme_name = random.choice(themes_names)
                    while Theme.objects.filter(name=theme_name, project=project).count() > 0:
                        theme_name = random.choice(themes_names)
                    theme = mommy.make(Theme,
                                       project=project,
                                       name=theme_name,
                                       description=lorem.paragraph(),
                                       created_by=user,
                                       modified_by=user)
                    # Create the link between mapper and theme.
                    theme.mappers_group.user_set.add(*random.choices(users,
                                                                     (len(t.username) for t in users),
                                                                     k=random.randint(1, 6)))
                    theme.tags.add(*random.choices(tags, (len(t) for t in tags), k=random.randint(1, 6)))
                    lang_idx = random.randint(0, len(settings.LANGUAGES) - 1)
                    lang = settings.LANGUAGES[lang_idx][0]
                    make_translation(theme, lang)
                    make_translation(project, lang)
                    for z in range(random.randint(1, 10)):
                        user = random.choice(users)
                        report = mommy.make(Report,
                                            name=f'Report {z}',
                                            location=Point(random.randint(-150, 150), random.randint(-60, 60)),
                                            description=lorem.paragraph(),
                                            theme=theme,
                                            created_by=user,
                                            status=random.choice(REPORT_STATUS_CHOICES)[0],
                                            modified_by=user)
                        valid_tags = list(theme.tags.names()) + list(theme.project.tags.names())
                        report_tags = random.choices(valid_tags,
                                                     (len(t) for t in valid_tags),
                                                     k=random.randint(1, len(valid_tags)))
                        report.tags.add(*report_tags)
                        for _ in range(random.randint(1, 10)):
                            user = random.choice(users)
                            mommy.make(ReportComment,
                                       text=lorem.paragraph(),
                                       report=report,
                                       created_by=user,
                                       status=random.choice(REPORT_STATUS_CHOICES)[0],
                                       modified_by=user)
                        for _ in range(random.randint(1, 3)):
                            make_report_medias(report)

    Migration.operations.append(migrations.RunPython(create_dev_data))

else:
    def noop(*args, **kwargs):
        pass


    Migration.operations.append(migrations.RunPython(noop))
