from rest_framework import serializers

from findyourngo.filtering.filter_util import FilterConfig


class FilterSerializer(serializers.Serializer):
    branches = serializers.ListField(required=False)
    topics = serializers.ListField(required=False)
    hasEcosoc = serializers.BooleanField(required=False)
    isCredible = serializers.BooleanField(required=False)
    hqCountries = serializers.ListField(required=False)
    hqCities = serializers.ListField(required=False)
    contactOptionPresent = serializers.BooleanField(required=False)
    typeOfOrganization = serializers.ListField(required=False)
    workingLanguages = serializers.ListField(required=False)
    funding = serializers.ListField(required=False)
    trustworthiness = serializers.FloatField(required=False)

    def create(self, validated_data):
        branches = validated_data.get('branches')
        topics = validated_data.get('topics')
        use_ecosoc = validated_data.get('hasEcosoc')
        use_credible_source = validated_data.get('isCredible')
        hq_countries = validated_data.get('hqCountries')
        hq_cities = validated_data.get('hqCities')
        use_contact_possible = validated_data.get('contactOptionPresent')
        types_of_organization = validated_data.get('typeOfOrganization')
        working_languages = validated_data.get('workingLanguages')
        funding = validated_data.get('funding')
        trustworthiness_lower_bound = validated_data.get('trustworthiness')
        return FilterConfig(
            branches,
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