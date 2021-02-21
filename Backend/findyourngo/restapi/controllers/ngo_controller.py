from datetime import datetime

from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from findyourngo.restapi.models import Ngo, NgoCountry, NgoRepresentative, NgoMetaData, NgoDataSource, NgoContact, \
    NgoTWScore, NgoAddress
from findyourngo.restapi.serializers.ngo_serializer import NgoSerializer, NgoShortSerializer, update_ngo_instance
from findyourngo.restapi.utils.email_util import send_email

SELF_REPORTED_DATA_SOURCE = 'self-reported and confirmed'


@api_view(['GET', 'POST', 'DELETE'])
def ngo_list(request):
    if request.method == 'GET':
        ngos = Ngo.objects.filter(confirmed=True)
        ngo_serializer = NgoSerializer(ngos, many=True)
        return JsonResponse(ngo_serializer.data, safe=False)

    elif request.method == 'POST':
        ngo_data = JSONParser().parse(request)
        ngo_serializer = NgoSerializer(data=ngo_data)
        if ngo_serializer.is_valid():
            ngo_serializer.save()
            return JsonResponse(ngo_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(ngo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ngo_detail(request):
    ngo = Ngo.objects.get(pk=request.query_params.get('id'))

    if request.method == 'GET':
        ngo_serializer = NgoSerializer(ngo)
        return JsonResponse(ngo_serializer.data)

    elif request.method == 'PUT':
        ngo_data = JSONParser().parse(request)
        try:
            update_ngo_instance(ngo, ngo_data)
            ngo_serializer = NgoSerializer(ngo)
            return JsonResponse(ngo_serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return JsonResponse({'error': 'Ngo could not be updated.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ngo.delete()
        return JsonResponse({'message': 'Ngo was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ngo_short_list(request):
    ngos = Ngo.objects.filter(confirmed=True)
    ngo_serializer = NgoShortSerializer(ngos, many=True)
    return JsonResponse(ngo_serializer.data, safe=False)


@api_view(['GET'])
def ngo_short_list_all(request):
    ngos = Ngo.objects.all()
    ngo_serializer = NgoShortSerializer(ngos, many=True)
    return JsonResponse(ngo_serializer.data, safe=False)


@api_view(['POST'])
def register_ngo(request) -> JsonResponse:
    new_ngo_request = JSONParser().parse(request)
    print(new_ngo_request)
    new_ngo_request = new_ngo_request['ngo']

    ngo_name = new_ngo_request['ngoName']

    if len(Ngo.objects.filter(name=ngo_name.upper())) > 0:
        return JsonResponse({'error': f'Ngo with name {ngo_name} already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    ngo_country = new_ngo_request['ngoCountry']

    try:
        country = NgoCountry.objects.get(name=ngo_country.upper())
    except:
        return JsonResponse({'error': f'Country {ngo_country} not found'}, status=status.HTTP_400_BAD_REQUEST)

    address = NgoAddress.objects.create(
        street='',
        postcode='',
        city='',
        country=country
    )

    first_name = new_ngo_request['representativeFirstName']
    last_name = new_ngo_request['representativeLastName']
    email = new_ngo_request['representativeEmail']

    representative = NgoRepresentative.objects.create(
        representative_first_name=first_name,
        representative_last_name=last_name,
        representative_email=email
    )

    contact = NgoContact.objects.create(
        ngo_phone_number='',
        website='',
        representative=representative,
        address=address
    )

    try:
        info_source = NgoDataSource.objects.get(source=SELF_REPORTED_DATA_SOURCE)
    except:
        info_source = NgoDataSource.objects.create(
            credible=True,
            source=SELF_REPORTED_DATA_SOURCE
        )

    meta_data = NgoMetaData.objects.create(
        last_updated=datetime.now()
    )
    meta_data.info_source.add(info_source)
    meta_data.save()

    tw_score = NgoTWScore.objects.create(
        total_tw_score=0,
        base_tw_score=0,
        user_tw_score=0
    )

    Ngo.objects.create(
        name=ngo_name,
        acronym='',
        aim='',
        activities='',
        contact=contact,
        meta_data=meta_data,
        tw_score=tw_score,
        confirmed=False,
    )

    send_email(
        'NGO Registration FindyourNgo',
        f'''
    Dear {first_name} {last_name}, 
    
    FindyourNGO has received an application for the NGO {ngo_name}, listing you as its representative.
    We are now reviewing the application to ensure that only real NGOs are listed on our platform. To speed
    up the review process, please provide us with further information regarding your NGO's activities, funding,
    organizational structure etc by replying to this email.

    Best regards
    the FindyourNGO-team
        ''',
        'registration@findyourngo.org',
        [email]
    )

    return JsonResponse({'message': f'Ngo {ngo_name} was added successfully.'}, status=status.HTTP_200_OK)