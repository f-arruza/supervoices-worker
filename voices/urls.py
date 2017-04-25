# -*- coding: UTF-8 -*-
from django.conf.urls import url
from .views import (CompetitionListView, CompetitionCreateView,
                    CompetitionUpdateView, CompetitionListByOwnerView,
                    CompetitionInfoFullView, CompetitionInfoPublicView,
                    VoiceCreateView, NotifyView, ConvertAudioView,
                    WinnerCreateView, competition_delete, VoiceUserListView,
                    VoicePublicListView)

from .tester import generateTestData

urlpatterns = [
    # Generar juego de datos para pruebas de carga y stress
    url(r'^tester/$', generateTestData, name='tester'),
    # Listar Concursos por Propietario
    url(r'^competition/by_owner/(?P<owner_id>\d+)/$',
        CompetitionListByOwnerView.as_view(),
        name='compt-list-by-owner'),
    # Listar Concursos Activos
    url(r'^competitions$', CompetitionListView.as_view(),
        name='compt-list-all'),
    # Crear Concursos
    url(r'^competitions/create/', CompetitionCreateView.as_view(),
        name='compt-create'),
    # Actualizar Información de Concurso
    url(r'^competitions/update/(?P<pk>\d+)/', CompetitionUpdateView.as_view(),
        name='compt-update'),
    # Eliminar Concurso
    url(r'^competitions/delete/(?P<pk>\d+)/', competition_delete,
        name='compt-delete'),
    # Información Detallada de un Concurso para Propietarios
    url(r'^competition/info/(?P<url>\w+)/$', CompetitionInfoFullView.as_view(),
        name='compt-info-full'),
    # Información Detallada de un Concurso para Propietarios
    url(r'^competition/public/(?P<url>\w+)/$',
        CompetitionInfoPublicView.as_view(),
        name='compt-info-pub'),
    # Agregar Voice a Concurso
    url(r'^competition/(?P<pk>\d+)/add_voice/$', VoiceCreateView.as_view(),
        name='compt-add-voice'),
    # Seleccionar Voice ganadora de Concurso
    url(r'^competition/winner/$', WinnerCreateView.as_view(),
        name='compt-winner'),
    # Notificar Concurso
    url(r'^competition/(?P<pk>\d+)/notify', NotifyView.as_view(),
        name='compt-notify'),
    # Listar Voice de un Concurso para el Propietario
    url(r'^voices-user/(?P<url>\w+)', VoiceUserListView.as_view(),
        name='voices-user-list'),
    # Listar Voice de un Concurso para el Público
    url(r'^voices-public/(?P<url>\w+)', VoicePublicListView.as_view(),
        name='voices-public-list'),
    # Convertir Audio a MP3
    url(r'^convert$', ConvertAudioView.as_view(), name='convert'),
]
