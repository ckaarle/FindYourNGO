from typing import Any

from django.db.models import QuerySet
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser

from findyourngo.filtering.NgoFilter import NgoFilter
from findyourngo.restapi.paginators.NgoOverviewItemListPaginator import NgoOverviewItemListPaginator
from findyourngo.restapi.serializers.filter_serializer import FilterSerializer, filter_object
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer

MAX_PAGE_SIZE = 20

last_filter_config = []


@api_view(['GET'])
def ngo_filter_options(request: Any) -> JsonResponse:
    return JsonResponse(filter_object())


class NgoFilterView(GenericAPIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                filter_data = JSONParser().parse(request)
                filter_serializer = FilterSerializer(data=filter_data)

                if filter_serializer.is_valid():
                    last_filter_config.clear()
                    last_filter_config.append(filter_serializer.create(filter_serializer.validated_data))
            except:
                return JsonResponse(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return super(NgoFilterView, self).dispatch(request, *args, **kwargs)

    def get(self, request: Any) -> JsonResponse:
        paginator = NgoOverviewItemListPaginator()
        paginator.page_size = MAX_PAGE_SIZE

        filter = NgoFilter(last_filter_config[-1])
        self.queryset: QuerySet = filter.apply()

        result_page = paginator.paginate_queryset(self.queryset, request)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(ngo_overview_item_serializer.data)

    def post(self, request: Any) -> JsonResponse:
        paginator = NgoOverviewItemListPaginator()
        paginator.page_size = MAX_PAGE_SIZE

        filter = NgoFilter(last_filter_config[-1])
        self.queryset: QuerySet = filter.apply()

        result_page = paginator.paginate_queryset(self.queryset, request)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(ngo_overview_item_serializer.data)
