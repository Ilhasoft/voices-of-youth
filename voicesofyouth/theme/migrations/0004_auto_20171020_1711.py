# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 17:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0003_theme_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='color',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
