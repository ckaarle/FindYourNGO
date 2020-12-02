from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.restapi.models import Ngo
from findyourngo.restapi.serializers.ngo_serializer import NgoSerializer


@api_view(['GET', 'POST', 'DELETE'])
def ngo_list(request):
    if request.method == 'GET':
        ngos = Ngo.objects.all()

        # TODO: any conditions?

        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)

    elif request.method == 'DELETE':
        count = Ngo.objects.all().delete()
        return JsonResponse({'message': '{} Ngos were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        ngo_data = JSONParser().parse(request)
        ngo_serializer = NgoSerializer(data=ngo_data)
        if ngo_serializer.is_valid():
            ngo_serializer.save()
            print("NGO SERIALIZER IS VALID")
            return JsonResponse(ngo_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ngo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

