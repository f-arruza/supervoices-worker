# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voices', '0006_auto_20170219_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voice',
            options={'ordering': ['-creation_date', '-id']},
        ),
        migrations.AlterField(
            model_name='voice',
            name='converted_file',
            field=models.FileField(blank=True, null=True, upload_to='static/voices/'),
        ),
        migrations.AlterField(
            model_name='voice',
            name='original_file',
            field=models.FileField(upload_to='static/voices/'),
        ),
    ]
