# -*- coding: UTF-8 -*-
import os
import uuid
import subprocess
import socket
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

import boto
import boto3
from boto.s3.key import Key


def send_email_competition(request, compt, recipient_name, recipient_email):
    try:
        subject = 'SUPERVOICES :: Invitación a participar en Concurso'
        body_text = 'Estimado(a) ' + recipient_name + ', \n\n'
        body_text = body_text + 'Queremos informarte de la apertura de un '
        body_text = body_text + 'nuevo concurso y te invitamos a participar. '
        body_text = body_text + '\n\n El concurso estará vigente hasta el '
        body_text = body_text + str(compt.end_date) + ', para mayor '
        body_text = body_text + 'información consulta el siguiente link: \n\n'
        body_text = body_text + 'http://' + request.META['HTTP_HOST']
        body_text = body_text + '/competitions/detail/' + compt.url + '/\n\n'
        body_text = body_text + 'Cordial saludo,\n\n'
        body_text = body_text + request.user.first_name + ' '
        body_text = body_text + request.user.last_name + '.'

        send_mail(subject, body_text, settings.EMAIL_FROM_MAIL,
                  [recipient_email], fail_silently=True)
        return True
    except:
        return False


def send_email_convert_audio(author_firstname, author_email, competition_name):
    subject = 'SUPERVOICES :: Audio Publicado'
    body_text = 'Estimado(a) ' + author_firstname + ', \n\n'
    body_text = body_text + 'Queremos informarte que ha sido publicado '
    body_text = body_text + 'su audio en el concurso '
    body_text = body_text + competition_name + '.\n\n'
    body_text = body_text + 'Cordial saludo,\n\n'
    body_text = body_text + 'Administrador de Supervoices'

    return send_mail(subject, body_text, settings.EMAIL_FROM_MAIL,
                     [author_email], fail_silently=False)


def convertIndividualAudio(voice):
    convertAudio(voice)
    return voice.id


def convertAudio(voice):
    # Convertir Archivo de Audio
    output_file_name = 'voices/' + str(uuid.uuid1()) + '.mp3'

    input_file = settings.MEDIA_URL + str(voice.original_file)
    output_file = settings.MEDIA_TMP + output_file_name

    # Convertir Archivo de audio a MP3
    cmd = settings.FFMPEG_PATH + ' -i ' + input_file
    cmd = cmd + ' -map_metadata 0:s:0 -y ' + output_file
    subprocess.call(cmd, shell=True)

    # Subir archivo MP3 a S3
    file = open(output_file, 'rb')
    if upload_to_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                    file, settings.AWS_STORAGE_BUCKET_NAME,
                    '/media/' + output_file_name):
        print('It worked!')

        # Actualizar registro en base de datos
        voice.converted_file = output_file_name
        voice.converted_date = timezone.now()
        voice.state = 'C'
        voice.save()
        voice_id = voice.id

        # Enviar notificación al author_firstname
        result = send_email_convert_audio(voice)
        if result > 0:
            print('Successful email notification send.')
        else:
            print('Unsuccessful email notification send.')
    else:
        print('The upload failed...')

    # Borrar archivo MP3 temporal
    if os.path.exists(output_file):
        os.remove(output_file)


def convertAudioDynamoDB(voice_id, input_file, author_firstname, author_email,
                         competition_name):
    # Convertir Archivo de Audio
    input_file_tmp = settings.MEDIA_TMP + str(uuid.uuid1())

    output_file_name = str(uuid.uuid1()) + '.mp3'
    output_file = settings.MEDIA_TMP + output_file_name

    # Convertir Archivo de audio a MP3
    cmd0 = 'wget ' + input_file + ' -O ' + input_file_tmp

    cmd = settings.FFMPEG_PATH + ' -i ' + input_file_tmp
    cmd = cmd + ' -map_metadata 0:s:0 -y ' + output_file
    subprocess.call(cmd, shell=True)

    # Subir archivo MP3 a S3
    file = open(output_file, 'rb')
    if upload_to_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                    file, settings.AWS_STORAGE_BUCKET_NODE_NAME,
                    output_file_name):
        print('It worked!')

        # Actualizar registro en base de datos
        update_voice(voice_id, settings.MEDIA_NODE_URL + output_file_name)

        # Enviar notificación al author_firstname
        result = send_email_convert_audio(author_firstname, author_email,
                                          competition_name)
        if result > 0:
            print('Successful email notification send.')
        else:
            print('Unsuccessful email notification send.')
    else:
        print('The upload failed...')

    # Borrar archivo de entrada temporal
    if os.path.exists(input_file_tmp):
        os.remove(input_file_tmp)
    
    # Borrar archivo MP3 temporal
    if os.path.exists(output_file):
        os.remove(output_file)


def update_voice(voice_id, converted_file):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_DYNAMODB_REGION,
                              endpoint_url=settings.AWS_DYNAMODB_ENDPOINT)

    table = dynamodb.Table('voice')
    set_query = "SET #state = :val1, converted_file = :val2,"
    set_query = set_query + " converted_date = :val3, converted_host = :val4"
    table.update_item(
        Key={
            'id': str(voice_id)
        },
        UpdateExpression=set_query,
        ExpressionAttributeValues={
            ':val1': "C",
            ':val2': converted_file,
            ':val3': str(timezone.now()),
            ':val4': str(socket.gethostname())
        },
        ExpressionAttributeNames={
            '#state': "state",
        }
    )


def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket, key,
                 callback=None, md5=None, reduced_redundancy=False,
                 content_type=None):
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    bucket.set_acl('public-read')
    k = Key(bucket)
    k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, replace=False,
                                    reduced_redundancy=reduced_redundancy,
                                    rewind=True, policy='public-read')
    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False
