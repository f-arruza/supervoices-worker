# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-18 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('author_firstname', models.CharField(max_length=50)),
                ('author_lastname', models.CharField(max_length=50)),
                ('author_email', models.CharField(max_length=50)),
                ('observations', models.CharField(blank=True, max_length=512, null=True)),
                ('original_file', models.FileField(upload_to='voices')),
                ('converted_file', models.FileField(upload_to='voices')),
                ('state', models.CharField(choices=[('P', 'IN PROCESS'), ('C', 'CONVERTED')], max_length=1)),
                ('active', models.BooleanField(default=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voices', to='voices.Competition')),
            ],
        ),
    ]
