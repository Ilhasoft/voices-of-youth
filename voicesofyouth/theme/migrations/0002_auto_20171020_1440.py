# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
        ('taggit', '0002_auto_20150616_2121'),
        ('theme', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0002_auto_20171020_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='themetranslation',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='themes_themetranslation_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='themetranslation',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='themes_themetranslation_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='themetranslation',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_language', to='theme.Theme'),
        ),
        migrations.AddField(
            model_name='theme',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='themes_theme_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='theme',
            name='mappers_group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_mappers', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='theme',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='themes_theme_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='theme',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='theme',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='tag.Tag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
