from django.http.response import JsonResponse
from rest_framework.decorators import api_view

from findyourngo.restapi.models import Ngo, NgoConnection
from findyourngo.restapi.serializers.ngo_serializer import NgoPlotSerializer, NgoLinkSerializer


@api_view(['GET'])
def get_plots(request) -> JsonResponse:
    plot_serializer = NgoPlotSerializer(Ngo.objects.all(), many=True)
    return JsonResponse(plot_serializer.data, safe=False)


@api_view(['GET'])
def get_links(request) -> JsonResponse:
    link_serializer = NgoLinkSerializer(NgoConnection.objects.all(), many=True)
    return JsonResponse(link_serializer.data, safe=False)
