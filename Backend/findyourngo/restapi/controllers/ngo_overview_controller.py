from typing import Any

from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, authentication_classes

from findyourngo.restapi.models import Ngo
from findyourngo.restapi.paginators.NgoOverviewItemListPaginator import NgoOverviewItemListPaginator
from findyourngo.restapi.serializers.ngo_overview_serializer import NgoOverviewItemSerializer


class NgoOverviewItemList(GenericAPIView):

    def get_authenticators(self):
        return []

    def get(self, request: Any) -> JsonResponse:
        paginator = NgoOverviewItemListPaginator()
        paginator.page_size = 20

        self.queryset = Ngo.objects.filter(confirmed=True)
        self.queryset = self.queryset.order_by('name')
        result_page = paginator.paginate_queryset(self.queryset, request)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(ngo_overview_item_serializer.data)


@api_view(['GET'])
@authentication_classes([])
def ngo_overview_items_amount(request: Any):
    ngo_count = Ngo.objects.filter(confirmed=True).count()
    return JsonResponse({'count': ngo_count})

