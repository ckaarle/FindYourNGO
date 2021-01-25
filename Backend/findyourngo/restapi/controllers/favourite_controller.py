from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser

from findyourngo.restapi.models import NgoFavourites, Ngo


@api_view(['GET', 'POST'])
def user_favourite(request) -> JsonResponse:
    user_id = request.query_params.get('userId')

    if request.user.id != int(user_id):
        return JsonResponse({'error': 'Favourited NGOs cannot be accessed for a different user.'})

    if request.method == 'GET':
        ngo_id = request.query_params.get('ngoId')
        try:
            ngo = Ngo.objects.get(pk=ngo_id)
            user = User.objects.get(pk=user_id)
            NgoFavourites.objects.get(favourite_ngo=ngo, user=user)
            return JsonResponse(True, safe=False)
        except:
            return JsonResponse(False, safe=False)

    if request.method == 'POST':
        ngo_id = request.query_params.get('ngoId')

        data = JSONParser().parse(request)
        favourite = data['favourite']

        user = User.objects.get(pk=user_id)
        ngo = Ngo.objects.get(pk=ngo_id)

        if favourite:
            try:
                if len(NgoFavourites.objects.filter(user=user, favourite_ngo=ngo)) > 0:
                    return JsonResponse({'error': 'NGO already favourited.'})

                ngo_favourite = NgoFavourites.objects.create(user=user)
                ngo_favourite.favourite_ngo.add(ngo)
                ngo_favourite.save()
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'NGO could not be favourited.'})
        else:
            try:
                ngo_favourite = NgoFavourites.objects.get(favourite_ngo=ngo, user=user)
                ngo_favourite.delete()
            except:
                return JsonResponse({'error': 'NGO could not be un-favourited.'})

        return JsonResponse(favourite, safe=False)

@api_view(['GET'])
def user_favourites(request) -> JsonResponse:
    user_id = request.query_params.get('userId')

    if request.user.id != int(user_id):
        return JsonResponse({'error': 'Favourited NGOs cannot be read for a different user.'})

    try:
        user = User.objects.get(pk=user_id)
        favourites = NgoFavourites.objects.filter(user=user)

        favourite_ids = []
        for favourite in favourites:
            for ngo in favourite.favourite_ngo.all():
                favourite_ids.append(ngo.id)
        return JsonResponse(favourite_ids, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)