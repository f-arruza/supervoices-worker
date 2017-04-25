# -*- coding: UTF-8 -*-
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.db import IntegrityError


@csrf_exempt
def verify_token(request):
    if request.method == 'POST':
        token_param = request.POST.get('token')
        try:
            token = Token.objects.get(key=token_param)
            status = {'user': token.user.id,}
        except:
            status = {'user': 'Invalid Token',}
        return JsonResponse(status)
    else:
        status = {'user': '0',}
        return JsonResponse(status)


# Create your views here.
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        response = login_service(request)
        return JsonResponse(response)
    else:
        status = "Incorrect method."
        return JsonResponse(status, safe=False)


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.auth:
            request.auth.delete()
        status = "Logout sucessfully."
        return JsonResponse(status, safe=False)


#     login_service
#     Este médodo permite registrar un usuario
#     Param: datos del usuario.
def login_service(request):
    json_data = json.loads(request.body.decode('utf-8'))

    username = json_data['username']
    password = json_data['password']

    if (username is not None and password is not None):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return login_user_to_json(user)
        else:
            status = 'Usuario o clave incorrecta.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}


#     login_user_to_json
#     Este médodo permite transformar un usuario autenticado en json
#     Param: usuario.
def login_user_to_json(user):
    # Generate Token
    try:
        token = Token.objects.create(user=user)
    except:
        token = Token.objects.get(user__id=user.id)

    json_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'token': token.key,
        'id_user': user.id,
    }
    return json_data


class UserView(ListModelMixin, GenericAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.create_user(username=json_data['username'],
                                            password=json_data['password'],
                                            email=json_data['email'],
                                            first_name=json_data['first_name'],
                                            last_name=json_data['last_name'])
            user.save()
            login(request, user)
            response = login_user_to_json(user)
            return JsonResponse(response)
        except:
            return JsonResponse({"result": "Unknown error occurred"},
                                safe=False)


class UpdateUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.filter(pk=self.kwargs['pk'])
        return user


class ChangePasswordView(ListModelMixin, GenericAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        response = change_password_action(json_data)
        return JsonResponse(response, safe=False)


def change_password_action(json_data):
    username = json_data['username']
    old_password = json_data['old_password']
    password = json_data['password']

    if (username is not None and password is not None and
            old_password is not None):
        try:
            user = authenticate(username=username, password=old_password)
            user.set_password(password)
            user.save()
            status = 'La clave fue actualizada.'
        except:
            status = 'Usuario o clave  incorrecta.'
    else:
        status = 'Todos los campos son obligatorios.'
    return {'status': status}
