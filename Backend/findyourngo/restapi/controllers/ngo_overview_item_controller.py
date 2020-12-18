from typing import Any

from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination

from findyourngo.restapi.models import Ngo
from findyourngo.restapi.paginators.NgoOverviewItemListPaginator import NgoOverviewItemListPaginator
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer
from findyourngo.restapi.controllers.ngo_controller import ngo_filter


class NgoOverviewItemList(GenericAPIView):

    def get(self, request: Any) -> JsonResponse:
        paginator = NgoOverviewItemListPaginator()
        paginator.page_size = 20

        self.queryset = Ngo.objects.all()
        self.queryset = ngo_filter(self.queryset, request.query_params)
        self.queryset = self.queryset.order_by('name')
        result_page = paginator.paginate_queryset(self.queryset, request)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(ngo_overview_item_serializer.data)
