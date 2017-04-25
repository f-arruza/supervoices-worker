# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-25 01:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voices', '0008_remove_competition_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='compts', to='voices.Competition')),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='voices.Voice')),
            ],
        ),
    ]
