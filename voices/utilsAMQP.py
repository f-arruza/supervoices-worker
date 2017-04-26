# -*- coding: UTF-8 -*-
import pika
from django.conf import settings


def publishVoiceID(voice_id):
    # Establecer conexion
    parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
    con = pika.BlockingConnection(parameters)
    ch = con.channel()

    # Declarar la cola
    ch.queue_declare(queue='voices')

    # Publicar el mensaje
    ch.basic_publish(exchange='', routing_key='voices', body=str(voice_id))
    print("Send message...")

    # Cerrar Conexion
    con.close()


def consumeIndividualVoiceID():
    # Establecer conexion
    con = pika.BlockingConnection()
    channel = con.channel()

    method_frame, header_frame, body = channel.basic_get(queue='voices')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return body.decode("utf-8")
    else:
        print('No message returned')


def consumeVoiceID(callback):
    # Establecer conexion
    parameters = pika.URLParameters(settings.BROKER_URL)
    con = pika.BlockingConnection(parameters)
    ch = con.channel()

    # Declarar la cola
    ch.queue_declare(queue='voices')

    ch.basic_consume(callback, queue='voices', no_ack=True)
    ch.start_consuming()
