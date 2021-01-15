from django.contrib.auth.models import User, Group
from django.db import connection, transaction
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions

from findyourngo.data_import.data_importer import run_initial_data_import
from findyourngo.data_import.db_sql_queries import delete_all_query
from findyourngo.restapi.serializers.serializers import UserSerializer, GroupSerializer
from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater


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


def pagerankTest(request):
    TWUpdater().update()
    return HttpResponse('TW updated with PageRank')
