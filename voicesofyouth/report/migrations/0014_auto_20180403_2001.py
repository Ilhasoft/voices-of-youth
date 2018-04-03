# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0013_auto_20180223_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportnotification',
            name='report',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='report.Report'),
        ),
    ]
