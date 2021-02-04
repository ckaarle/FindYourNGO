from rest_framework import serializers

from findyourngo.filtering.filter_util import FilterConfig
from findyourngo.restapi.models import NgoTopic, NgoBranch, NgoAddress, NgoType, NgoStats


def filter_object():
    return {
            'name': None,
            'branches': branches(),
            'regions': regions(),
            'topics': topics(),
            'hasEcosoc': False,
            'isCredible': False,
            'countries': hq_countries(),
            'cities': hq_cities(),
            'contactOptionPresent': False,
            'typeOfOrganization': types_of_organization(),
            'workingLanguages': working_languages(),
            'funding': funding(),
            'trustworthiness': None
        }


def branches():
    branches = list(map(lambda ngo_branch: ngo_branch['country'], NgoBranch.objects.all().order_by('country').values('country').distinct()))
    return branches


def regions():
    return ["Africa", "Asia", "Europe"]


def topics():
    topics = list(map(lambda ngo_topic: ngo_topic['topic'], NgoTopic.objects.all().order_by('topic').values('topic').distinct()))
    return topics


def hq_countries():
    hq_countries = list(map(lambda ngo_hq_address: ngo_hq_address['country'], NgoAddress.objects.all().order_by('country').values('country').distinct()))
    return hq_countries


def hq_cities():
    hq_cities = []
    for country in hq_countries():
        hq_cities.append({country: list(map(lambda ngo_hq_address: ngo_hq_address['city'], NgoAddress.objects.filter(country=country).order_by('city').values('city').distinct()))})
    return hq_cities


def types_of_organization():
    types_of_organization = list(map(lambda ngo_type: ngo_type['type'], NgoType.objects.all().order_by('type').values('type').distinct()))
    return types_of_organization


def working_languages():
    return ["English", "French", "German"]


def funding():
    funding = list(map(lambda ngo_stats: ngo_stats['funding'], NgoStats.objects.all().order_by('funding').values('funding').distinct()))
    return funding


class FilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    branches = serializers.ListField(required=False)
    regions = serializers.ListField(required=False)
    topics = serializers.ListField(required=False)
    hasEcosoc = serializers.BooleanField(required=False)
    isCredible = serializers.BooleanField(required=False)
    countries = serializers.ListField(required=False)
    cities = serializers.ListField(required=False)
    contactOptionPresent = serializers.BooleanField(required=False)
    typeOfOrganization = serializers.ListField(required=False)
    workingLanguages = serializers.ListField(required=False)
    funding = serializers.ListField(required=False)
    trustworthiness = serializers.FloatField(required=False)

    def create(self, validated_data):
        name = validated_data.get('name')
        branches = validated_data.get('branches')
        regions = validated_data.get('regions')
        topics = validated_data.get('topics')
        use_ecosoc = validated_data.get('hasEcosoc')
        use_credible_source = validated_data.get('isCredible')
        hq_countries = validated_data.get('countries')
        hq_cities = validated_data.get('cities')
        use_contact_possible = validated_data.get('contactOptionPresent')
        types_of_organization = validated_data.get('typeOfOrganization')
        working_languages = validated_data.get('workingLanguages')
        funding = validated_data.get('funding')
        trustworthiness_lower_bound = validated_data.get('trustworthiness')
        return FilterConfig(
            name,
            branches,
            regions,
            topics,
            use_ecosoc,
            use_credible_source,
            hq_countries,
            hq_cities,
            use_contact_possible,
            types_of_organization,
            working_languages,
            funding,
            trustworthiness_lower_bound,
        )