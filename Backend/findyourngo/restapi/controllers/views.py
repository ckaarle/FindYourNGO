import requests

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import connection, transaction
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from findyourngo.data_import.data_importer import run_initial_data_import, update_ngo_tw_score
from findyourngo.data_import.db_sql_queries import delete_all_query
from findyourngo.restapi.serializers.serializers import UserSerializer, GroupSerializer
from findyourngo.restapi.models import Ngo, NgoBranch, NgoTopic


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def dataImport(request):
    initial_import_necessary = run_initial_data_import()
    if initial_import_necessary:
        return HttpResponse('Data import finished successfully. Please refer to the backend console output for logs.')
    else:
        return HttpResponse('Data import not necessary')


def clearDatabase(request):
    cursor = connection.cursor()
    cursor.execute(delete_all_query)
    transaction.commit()
    return HttpResponse('Database has been cleared')


def recalculateTW(request):
    for ngo in Ngo.objects.all():
        update_ngo_tw_score(ngo)
        ngo.save()
    return HttpResponse('Trustworthiness scores have been recalculated')


# request is a necessary positional parameter for the framework call
def country_list(request):
    result = list(map(lambda ngo: ngo['country'], NgoBranch.objects.all().order_by('country').values()))
    return JsonResponse({'countries': result})


def topic_list(request):
    result = list(map(lambda ngo_topic: ngo_topic['topic'], NgoTopic.objects.all().order_by('topic').values()))
    return JsonResponse({'topics': result})


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get('token')}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        return create_user(data)


class FacebookView(APIView):
    def post(self, request):
        payload = {
            'access_token': request.data.get('token'),
            'fields': 'id, name, email',
        }  # validate the token
        r = requests.get('https://graph.facebook.com/me', params=payload)
        data = json.loads(r.text)
        print(data)

        if 'error' in data:
            content = {'message': 'wrong facebook token / this facebook token is already expired.'}
            return Response(content)

        return create_user(data)


def create_user(data):
    # create user if user does not exist
    try:
        user = User.objects.get(email=data['email'])
    except User.DoesNotExist:
        user = User()
        user.username = data['email']
        # provider random default password
        user.password = make_password(BaseUserManager().make_random_password())
        user.email = data['email']
        user.save()

    token = RefreshToken.for_user(user)  # generate token without username & password
    response = {'username': user.username,
                'access_token': str(token.access_token),
                'refresh_token': str(token),
                }
    return Response(response)
