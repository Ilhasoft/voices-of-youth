# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 19:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this item is active, use this instead of deleting')),
                ('created_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was originally created')),
                ('modified_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was last modified')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('path', models.CharField(max_length=100, verbose_name='Path')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'Francais'), ('sq', 'Shqip'), ('tr', 'Turkce'), ('ar', 'Arabic')], default='en', max_length=90)),
                ('created_by', models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='countries_country_creations', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='countries_country_modifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
