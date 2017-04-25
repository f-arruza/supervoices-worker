import os
import json
import subprocess
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (CreateAPIView, UpdateAPIView, ListAPIView,
                                     GenericAPIView)
from celery import chain
from .tasks import convertIndividualAudioById, convertIndividualAudioDynamoDB
from rest_framework.decorators import api_view
from .models import Competition, Voice, Winner
from .utilsAMQP import publishVoiceID, consumeIndividualVoiceID
from .utils import (send_email_competition, convertIndividualAudio)
from .serializers import (CompetitionUploadSerializer, CompetitionSerializer,
                          VoiceSerializer, VoiceUploadSerializer,
                          WinnerSerializer)
from django.views.generic import DeleteView


class CompetitionCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompetitionUploadSerializer
    queryset = Competition.objects.filter(active=True)


class CompetitionUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompetitionUploadSerializer

    def get_queryset(self):
        compts = Competition.objects.filter(pk=self.kwargs['pk'])
        return compts


@api_view(['DELETE'])
def competition_delete(request, pk):
    query = Competition.objects.get(pk=pk)
    query.delete()
    return JsonResponse({"result": "Deleted"}, safe=False)


class CompetitionListView(ListAPIView):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.filter(active=True)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'url',
        'owner',
        'id',
    )


class CompetitionListByOwnerView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        compts = Competition.objects.filter(active=True,
                                            owner=self.kwargs['owner_id'])
        return compts


class CompetitionInfoFullView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        compts = Competition.objects.filter(active=True,
                                            url=self.kwargs['url'],
                                            owner=self.request.user.id)
        return compts


class CompetitionInfoPublicView(ListAPIView):
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        compts = Competition.objects.filter(active=True,
                                            url=self.kwargs['url'])
        return compts


class WinnerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WinnerSerializer
    queryset = Winner.objects.all()


class VoiceCreateView(CreateAPIView):
    serializer_class = VoiceUploadSerializer

    def get_queryset(self):
        voices = Voice.objects.filter(competition_id=self.kwargs['pk'])
        return voices


class NotifyView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            count = 0
            compt = Competition.objects.get(pk=json_data['id_competition'])
            for rcp in json_data['recipients']:
                recipient_name = rcp['name']
                recipient_email = rcp['email']
                if send_email_competition(request, compt, recipient_name,
                                          recipient_email):
                    count = count + 1
            return JsonResponse({"result": count}, safe=False)
        except:
            return JsonResponse({"error": "Competition do not exist."},
                                safe=False)


class ConvertAudioView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            voice_id = json_data['voice_id']
            input_file = json_data['input_file']
            author_firstname = json_data['author_firstname']
            competition_name = json_data['competition_name']
            author_email = json_data['author_email']

            if (voice_id is not None):
                workflow_convert = chain(
                    convertIndividualAudioDynamoDB.s(voice_id, input_file,
                                                     author_firstname,
                                                     author_email,
                                                     competition_name)
                )
                workflow_convert.delay()
            return JsonResponse({"result": "successful"}, safe=False)
        except:
            return JsonResponse({"error": "failed"},
                                safe=False)


class VoiceUserSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


class VoicePublicSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class VoiceUserListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VoiceSerializer
    pagination_class = VoiceUserSetPagination

    def get_queryset(self):
        voices = Voice.objects.filter(competition__url=self.kwargs['url'],
                                      competition__owner=self.request.user.id).order_by('-creation_date')
        return voices


class VoicePublicListView(ListAPIView):
    serializer_class = VoiceSerializer
    pagination_class = VoicePublicSetPagination

    def get_queryset(self):
        voices = Voice.objects.filter(competition__url=self.kwargs['url'],
                                      state='C').order_by('-creation_date')
        return voices
