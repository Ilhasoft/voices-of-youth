# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 14:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0003_auto_20170823_2155'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this item is active, use this instead of deleting')),
                ('created_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was originally created')),
                ('modified_on', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='When this item was last modified')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('system_tag', models.BooleanField(default=False, verbose_name='Enabled')),
                ('urgency_score', models.IntegerField(default=0, verbose_name='Urgency Score')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countries.Country')),
                ('created_by', models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='tags_tag_creations', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='tags_tag_modifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
