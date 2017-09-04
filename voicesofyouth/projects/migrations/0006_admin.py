# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 19:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_auto_20170904_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this item is active, use this instead of deleting')),
                ('created_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was originally created')),
                ('modified_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was last modified')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='projects_admin_creations', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='projects_admin_modifications', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'verbose_name': 'Admins',
                'verbose_name_plural': 'Admins',
                'db_table': 'projects_project_admins',
            },
        ),
    ]
