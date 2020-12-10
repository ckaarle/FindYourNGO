from typing import Any

from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination

from findyourngo.restapi.models import Ngo
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer


class NgoOverviewItemList(GenericAPIView):

    def get(self, request: Any) -> JsonResponse:
        paginator = PageNumberPagination()
        paginator.page_size = 20

        query_set = Ngo.objects.all().order_by('name')
        result_page = paginator.paginate_queryset(query_set, request)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(ngo_overview_item_serializer.data)