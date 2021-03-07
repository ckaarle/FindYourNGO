import math
import random

from django.http import HttpResponse

from findyourngo.restapi.models import Ngo, NgoCountry
from findyourngo.restapi.controllers.connection_controller import create_connection


# for each subregion
# select 100 * subregion_ngo_count / total_ngo_count (round up) ngos according to tw_score
# for top 5 ngos inside subregion, connect with other 50, 40, 30, 20, 10% of countries inside
# for top 3 ngos inside each subregion, connect with any 5, 4, 3, 2, 1% of countries


def generate_data():
    all_ngos = []
    total_ngo_count = Ngo.objects.filter(confirmed=True).count()
    sub_region_list = NgoCountry.objects.values_list('sub_region').distinct()
    for sub_region in sub_region_list:
        sub_region = sub_region[0]
        ngo_count = math.ceil(100 * Ngo.objects.filter(contact__address__country__sub_region=sub_region, confirmed=True).count()
                              / total_ngo_count)
        ngos = Ngo.objects.filter(contact__address__country__sub_region=sub_region, confirmed=True).order_by('-tw_score__total_tw_score')
        all_ngos += list(ngos)[:ngo_count]
        for i in range(min(ngo_count, 5)):
            main_ngo: Ngo = ngos[i]
            for other_ngo in random.sample(list(ngos), int(ngo_count * 0.01 * (5 - i))):
                if main_ngo != other_ngo:
                    create_connection(main_ngo.id, other_ngo.id)
                    create_connection(other_ngo.id, main_ngo.id)
    for sub_region in sub_region_list:
        sub_region = sub_region[0]
        ngos = Ngo.objects.filter(contact__address__country__sub_region=sub_region, confirmed=True).order_by('-tw_score__total_tw_score')
        for i in range(min(ngos.count(), 3)):
            main_ngo: Ngo = ngos[i]
            for other_ngo in random.sample(all_ngos, int(len(all_ngos) * 0.01 * (5 - i))):
                if main_ngo != other_ngo:
                    create_connection(main_ngo.id, other_ngo.id)
                    create_connection(other_ngo.id, main_ngo.id)
    return HttpResponse('Generation complete')
