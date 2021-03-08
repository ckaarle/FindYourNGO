from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from findyourngo.restapi.models import NgoFavourites, Ngo, NgoEvent, NgoEventCollaborator
from findyourngo.restapi.serializers.ngo_overview_serializer import NgoOverviewItemSerializer
from findyourngo.restapi.serializers.ngo_serializer import NgoEventSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_favourite(request) -> JsonResponse:
    user_id = request.query_params.get('userId')

    if request.user.id != int(user_id):
        return JsonResponse({'error': 'Favourited NGOs cannot be accessed for a different user.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        ngo_id = request.query_params.get('ngoId')
        try:
            ngo = Ngo.objects.get(pk=ngo_id)
            user = User.objects.get(pk=user_id)
            NgoFavourites.objects.get(favourite_ngo=ngo, user=user)
            return JsonResponse(True, safe=False, status=status.HTTP_200_OK)
        except:
            return JsonResponse(False, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        ngo_id = request.query_params.get('ngoId')

        data = JSONParser().parse(request)
        favourite = data['favourite']

        user = User.objects.get(pk=user_id)
        ngo = Ngo.objects.get(pk=ngo_id)

        if favourite:
            try:
                if len(NgoFavourites.objects.filter(user=user, favourite_ngo=ngo)) > 0:
                    return JsonResponse({'error': 'NGO already favourited.'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    ngo_favourite = NgoFavourites.objects.get(user=user)
                except NgoFavourites.DoesNotExist:
                    ngo_favourite = NgoFavourites.objects.create(user=user)

                ngo_favourite.favourite_ngo.add(ngo)
                ngo_favourite.save()
            except:
                return JsonResponse({'error': 'NGO could not be favourited.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                ngo_favourite = NgoFavourites.objects.get(user=user)
                ngo_favourite.favourite_ngo.remove(ngo)
                ngo_favourite.save()
            except:
                return JsonResponse({'error': 'NGO could not be un-favourited.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(favourite, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_favourites(request) -> JsonResponse:
    user_id = request.query_params.get('userId')

    if request.user.id != int(user_id):
        return JsonResponse({'error': 'Favourited NGOs cannot be read for a different user.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(pk=user_id)
        favourites = NgoFavourites.objects.filter(user=user)

        favourite_ngos = []
        for favourite in favourites:
            for ngo in favourite.favourite_ngo.all().order_by('name'):
                favourite_ngos.append(ngo)

        ngo_overview_item_serializer = NgoOverviewItemSerializer(favourite_ngos, many=True)

        return JsonResponse(ngo_overview_item_serializer.data, safe=False, status=status.HTTP_200_OK)
    except:
        return JsonResponse([], safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favourite_events(request) -> JsonResponse:
    user_id = request.query_params.get('userId')

    if request.user.id != int(user_id):
        return JsonResponse({'error': 'Favourite events can only be accessed for oneself.'},
                            status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.get(pk=user_id)
    favourite = NgoFavourites.objects.get(user=user)

    relevant_ngos = favourite.favourite_ngo.all()

    organized_events = NgoEvent.objects.filter(organizer__in=relevant_ngos)\
        .union(NgoEvent.objects.filter(pk__in=NgoEventCollaborator.objects.filter(collaborator__in=relevant_ngos, pending=False).values('event'))).distinct()

    serializer = NgoEventSerializer(organized_events, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)