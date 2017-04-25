from __future__ import absolute_import
from celery import task
from .utils import convertAudio, convertAudioDynamoDB


@task(max_retries=2)
def convertIndividualAudioById(voice):
    convertAudio(voice)
    return voice.id


@task(max_retries=2)
def convertIndividualAudioDynamoDB(voice_id, input_file, author_firstname,
                                   author_email, competition_name):
    convertAudioDynamoDB(voice_id, input_file, author_firstname, author_email,
                         competition_name)
    return id
