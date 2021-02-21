import requests

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group
from django.db import connection, transaction
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from findyourngo.data_import.data_importer import run_initial_data_import
from findyourngo.data_import.data_generator import generate_data
from findyourngo.data_import.db_sql_queries import delete_all_query, delete_background_tasks_query
from findyourngo.restapi.serializers.serializers import UserSerializer, GroupSerializer
from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater
from findyourngo.restapi.models import Ngo, NgoAccount


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
    initial_import_necessary = run_initial_data_import(request)
    if initial_import_necessary:
        return HttpResponse('Data import finished successfully. Please refer to the backend console output for logs.')
    else:
        return HttpResponse('Data import not necessary')


def clearDatabase(request):
    cursor = connection.cursor()
    cursor.execute(delete_all_query)
    transaction.commit()
    return HttpResponse('Database has been cleared')


def dataGenerate(request):
    generate_data()
    return HttpResponse('Data generation complete')

def clearBackgroundTasks(request):
    cursor = connection.cursor()
    cursor.execute(delete_background_tasks_query)
    transaction.commit()
    return HttpResponse('Background tasks have been cleared')


def twUpdate(request):
    TWUpdater().update()
    return HttpResponse('TW updated with PageRank')


def storeDailyTw(request):
    TWUpdater().store_daily_tw()
    return HttpResponse('Daily TW stored')


# request is a necessary positional parameter for the framework call
def name_list(request):
    result = list(map(lambda ngo: ngo['name'], Ngo.objects.all().order_by('name').values()))
    return JsonResponse({'names': result})


class LoginView(APIView):
    def post(self, request):
        return create_user(request.data, request.query_params.get('ngo_name'), 'login')


class RegisterView(APIView):
    def post(self, request):
        return create_user(request.data, request.query_params.get('ngo_name'), 'register')


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get('token')}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        return create_user(data, request.query_params.get('ngo_name'))


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

        return create_user(data, request.query_params.get('ngo_name'))


class RefreshView(APIView):
    def post(self, request):
        refresh_token = RefreshToken(token=request.data.get('refresh_token'))
        return Response({'access_token': str(refresh_token.access_token)})


def create_user(data, ngo_name, mode=None):
    # create user if user does not exist
    try:
        if mode == 'login':
            email_or_username = data['email']

            if '@' in email_or_username:
                user = User.objects.get(email=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
        else:
            user = User.objects.get(email=data['email'])

        if mode == 'register':
            return Response({'error': 'User already registered'}, status=401)
    except User.DoesNotExist:
        if mode == 'login':
            return Response({'error': 'User not found'}, status=401)
        user = User()
        if data.get('username'):
            user.username = data['username']
        else:
            user.username = data['email']
        if data.get('password'):
            user.password = make_password(data['password'])
        else:  # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
        user.email = data.get('email')
        user.save()
        if ngo_name:
            ngo = Ngo.objects.get(name=ngo_name)
            NgoAccount.objects.create(user=user, ngo=ngo)
            print(list(NgoAccount.objects.all()))

    if mode == 'login' and not check_password(data['password'], user.password):
        return Response({'error': 'User credentials incorrect'}, status=401)

    ngo_id = -1
    try:
        ngo_id = NgoAccount.objects.get(user=user).ngo_id
    except Exception:
        pass

    token = RefreshToken.for_user(user)  # generate token without username & password
    response = {'username': user.username,
                'ngo_id': ngo_id,
                'access_token': str(token.access_token),
                'refresh_token': str(token),
                }
    return Response(response)


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request)
        to_check = request.data.get('user_id')
        if request.user.id == to_check:
            return JsonResponse({'success': f'User {request.user.username} was verified!'})
        return JsonResponse({'error': f'User was {request.user.id} but the request was for {to_check}'})
