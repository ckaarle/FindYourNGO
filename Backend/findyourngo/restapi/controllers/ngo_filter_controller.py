from typing import Any

from django.db.models import QuerySet
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser

from findyourngo.filtering.NgoFilter import NgoFilter
from findyourngo.restapi.models import Ngo, NgoStats, NgoType, NgoAddress, NgoTopic, NgoBranch
from findyourngo.restapi.paginators.NgoOverviewItemListPaginator import NgoOverviewItemListPaginator
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer


class NgoFilterController(GenericAPIView):

    def get(self, request: Any) -> JsonResponse:
        return JsonResponse(self.filter_object())

    def post(self, request: Any) -> JsonResponse:
        # paginator = NgoOverviewItemListPaginator()
        # paginator.page_size = 20
        # filter_data = JSONParser().parse(request)
        # filter_serializer = FilterSerializer(data=filter_data)
        #
        # if filter_serializer.is_valid():
        #     print(f'REQUEST WAS {filter_data}')
        #     filter_config = filter_serializer.create(filter_serializer.validated_data)
        #     filter = NgoFilter(filter_config)
        #     self.queryset: QuerySet = filter.apply()
        #
        #     print(f'FOUND {len(self.queryset)} RESULTS')
        #
        #     result_page = paginator.paginate_queryset(self.queryset, request)
        #
        #     ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        #     return paginator.get_paginated_response(ngo_overview_item_serializer.data)
        filter_data = JSONParser().parse(request)
        filter_serializer = FilterSerializer(data=filter_data)

        if filter_serializer.is_valid() and request.method == 'POST':
            print(f'REQUEST WAS {filter_data}')
            filter_config = filter_serializer.create(filter_serializer.validated_data)
            filter = NgoFilter(filter_config)
            ngo_result: QuerySet = filter.apply()

            print(f'FOUND {len(ngo_result)} RESULTS')

            result_serializer = NgoOverviewItemSerializer(ngo_result, many=True)

            return JsonResponse(result_serializer.data, safe=False)
        return JsonResponse(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter_object(self):  # TODO: move to frontend
        return {
            'branches': {"displayName": "Branches", "values": self.branches(), "icon": "account_tree"},
            'topics': {"displayName": "Topics", "values": self.topics(), "icon": "topic"},
            'hasEcosoc': {"displayName": "Accreditations", "values": False, "icon": "account_balance"},
            'isCredible': {"displayName": "Credibility", "values": False, "icon": "loyalty"},
            'countries': {"displayName": "Countries", "values": self.hq_countries(), "icon": "flag"},
            'cities': {"displayName": "Cities", "values": None, "icon": "location_on"},
            'contactOptionPresent': {"displayName": "Contactable", "values": False, "icon": "how_to_reg"},
            'typeOfOrganization': {"displayName": "Type of organization", "values": self.types_of_organization(),
                                   "icon": "corporate_fare"},
            'workingLanguages': {"displayName": "Working languages", "values": self.working_languages(),
                                 "icon": "translate"},
            'funding': {"displayName": "Funding", "values": self.funding(), "icon": "attach_money"},
            'trustworthiness': {"displayName": "Trustworthiness", "values": None, "icon": "star"}
        }

    def branches(self):
        branches = list(map(lambda ngo_branch: ngo_branch['country'],
                            NgoBranch.objects.all().order_by('country').values('country').distinct()))
        return branches

    def topics(self):
        topics = list(map(lambda ngo_topic: ngo_topic['topic'],
                          NgoTopic.objects.all().order_by('topic').values('topic').distinct()))
        return topics

    def hq_countries(self):
        hq_countries = list(map(lambda ngo_hq_address: ngo_hq_address['country'],
                                NgoAddress.objects.all().order_by('country').values('country').distinct()))
        return hq_countries

    def types_of_organization(self):
        types_of_organization = list(
            map(lambda ngo_type: ngo_type['type'], NgoType.objects.all().order_by('type').values('type').distinct()))
        return types_of_organization

    def working_languages(self):
        return ["English", "French", "German"]

    def funding(self):
        funding = list(map(lambda ngo_stats: ngo_stats['funding'],
                           NgoStats.objects.all().order_by('funding').values('funding').distinct()))
        return funding