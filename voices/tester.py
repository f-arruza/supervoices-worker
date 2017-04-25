# -*- coding: UTF-8 -*-
from .models import Voice, Competition
from django.http import JsonResponse


def generateTestData(request):
    c = Competition.objects.get(pk=6)

    for num in range(1, 4001):
        voice = Voice()
        voice.author_firstname = 'Fernando'
        voice.author_lastname = 'Arruza'
        voice.author_email = 'freeven2016@gmail.com'
        voice.observations = 'PRUEBA'
        voice.original_file = 'voices/0957.ogg'
        voice.state = 'P'
        voice.competition = c
        voice.save()
    status = "Success..."
    return JsonResponse(status, safe=False)
