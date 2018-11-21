# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-21 14:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0015_report_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_report_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_report_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportcomment',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportcomment_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportcomment',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportcomment_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportfile',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportfile_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportfile',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportfile_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportnotification',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportnotification_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportnotification',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reportnotification_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reporturl',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reporturl_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reporturl',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='report_reporturl_modifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
