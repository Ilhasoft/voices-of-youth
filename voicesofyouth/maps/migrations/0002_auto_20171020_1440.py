# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.CASCADE, related_name='maps_map_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='map',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.CASCADE, related_name='maps_map_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='map',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='project.Project'),
        ),
    ]
