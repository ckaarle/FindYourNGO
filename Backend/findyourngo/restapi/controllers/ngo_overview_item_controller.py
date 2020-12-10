from typing import Any

from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView

from findyourngo.restapi.models import Ngo
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer


class NgoOverviewItemList(GenericAPIView):

    def get(self, request: Any) -> JsonResponse:
        ngo_overview_items = Ngo.objects.all()
        ngo_overview_item_serializer = NgoOverviewItemSerializer(ngo_overview_items, many=True)
        return JsonResponse(ngo_overview_item_serializer.data, safe=False)