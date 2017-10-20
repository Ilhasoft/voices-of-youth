# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 17:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0002_auto_20171020_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='color',
            field=models.CharField(default='ffffff', max_length=6, validators=[django.core.validators.MinLengthValidator(6)]),
            preserve_default=False,
        ),
    ]
