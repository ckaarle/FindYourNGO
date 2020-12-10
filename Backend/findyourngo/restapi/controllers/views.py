from django.contrib.auth.models import User, Group
from django.db import connection, transaction
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework import permissions

from findyourngo.data_import.data_importer import run_initial_data_import, update_ngo_tw_score
from findyourngo.data_import.db_sql_queries import delete_all_query
from findyourngo.restapi.serializers.serializers import UserSerializer, GroupSerializer
from findyourngo.restapi.serializers.ngo_serializer import NgoSerializer, CountrySerializer
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


class NGOViewSet(viewsets.ModelViewSet):
    queryset = Ngo.objects.all()
    serializer_class = NgoSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Ngo.objects.all()
        country = self.request.query_params.get('country', None)
        allowed_querries = {"operation", "region", "office", "activity", "trust"}
        self.request.query_params.values()
        if country is not None:
            queryset = queryset.filter(branches__country__contains=country)

        return queryset


class CountryViewSet(viewsets.ModelViewSet):
    queryset = NgoBranch.objects.all().order_by('country')
    serializer_class = CountrySerializer


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


def country_list(request):
    result = list(map(lambda ngo: ngo['country'], NgoBranch.objects.all().order_by('country').values()))
    return JsonResponse({'countries': result})


def topic_list(request):
    result = list(map(lambda ngo_topic: ngo_topic['topic'], NgoTopic.objects.all().order_by('topic').values()))
    return JsonResponse({'topics': result})
