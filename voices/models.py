# -*- coding: UTF-8 -*-
import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from celery import chain
from .tasks import convertIndividualAudioById
from .utilsAMQP import publishVoiceID


# Create your models here.
class Competition(models.Model):
    name = models.CharField(max_length=100, blank=False)
    banner = models.ImageField(upload_to='banners', null=True,
                               blank=True)
    url = models.CharField(unique=True, max_length=20, blank=False, default='')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False,
                                 default=0.00)
    text = models.CharField(max_length=1024, blank=False, default='')
    recommendations = models.CharField(max_length=512, blank=False, default='')
    active = models.BooleanField(default=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='compts', null=True)

    def __str__(self):
        return self.name


class Voice(models.Model):
    def generate_path(instance, filename):
        ext = filename.split('.')[-1]
        return os.path.join('voices', str(uuid.uuid1()) + '.' + ext)

    creation_date = models.DateField(auto_now_add=True)
    author_firstname = models.CharField(max_length=50, null=False, blank=False)
    author_lastname = models.CharField(max_length=50, null=False, blank=False)
    author_email = models.CharField(max_length=50, null=False, blank=False)
    observations = models.CharField(max_length=512, null=True, blank=True)
    original_file = models.FileField(upload_to=generate_path)
    converted_file = models.FileField(upload_to='voices', null=True,
                                      blank=True)
    converted_date = models.DateTimeField(blank=False, null=False,
                                          default='1900-01-01 00:00:00')
    STATE = (
        ('P', 'EN PROCESO'),
        ('C', 'CONVERTIDO'),
    )
    state = models.CharField(max_length=1, blank=False, choices=STATE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE,
                                    related_name='voices')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-creation_date', '-id']

    def save(self, *args, **kwargs):
        voice_id = self.id
        super(Voice, self).save(*args, **kwargs)

        if (voice_id is None):
            # publishVoiceID(self.id)
            workflow_convert = chain(convertIndividualAudioById.s(self))
            workflow_convert.delay()

    def __str__(self):
        return self.author_firstname


class Winner(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE,
                                       related_name='compts')
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE,
                              related_name='winner')

    def __str__(self):
        return self.competition.name + ' - ' + voice.author_firstname
