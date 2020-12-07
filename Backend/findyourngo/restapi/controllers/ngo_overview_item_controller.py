from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from findyourngo.restapi.models import Ngo
from findyourngo.restapi.serializers.ngo_overview_item_serializer import NgoOverviewItemSerializer


@api_view(['GET'])
def ngo_overview_item_list(request):
    if request.method == 'GET':
        ngo_overview_items = Ngo.objects.all()
        ngo_overview_item_serializer = NgoOverviewItemSerializer(ngo_overview_items, many=True)
        return JsonResponse(ngo_overview_item_serializer.data, safe=False)

