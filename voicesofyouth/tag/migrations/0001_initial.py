# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=50, verbose_name='Object id')),
                ('urgency_score', models.IntegerField(default=0, verbose_name='Urgency Score')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_tag_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_tag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
