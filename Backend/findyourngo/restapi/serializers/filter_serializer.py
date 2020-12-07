from rest_framework import serializers

from findyourngo.filtering.filter_util import FilterConfig


class FilterSerializer(serializers.Serializer):
    branches_to_include = serializers.ListField()
    topics_to_include = serializers.ListField()
    use_ecosoc = serializers.BooleanField()
    use_credible_source = serializers.BooleanField()
    hq_country_to_include = serializers.ListField()
    hq_city_to_include = serializers.ListField()
    use_contact_possible = serializers.BooleanField()
    types_of_organization_to_include = serializers.ListField()
    working_languages_to_include = serializers.ListField()
    funding_to_include = serializers.ListField()
    trustworthiness_lower_bound = serializers.FloatField()

    def create(self, validated_data):
        branches = validated_data.get('branches_to_include')
        topics = validated_data.get('topics_to_include')
        use_ecosoc = validated_data.get('use_ecosoc')
        use_credible_source = validated_data.get('use_credible_source')
        hq_countries = validated_data.get('hq_country_to_include')
        hq_cities = validated_data.get('hq_city_to_include')
        use_contact_possible = validated_data.get('use_contact_possible')
        types_of_organization = validated_data.get('types_of_organization_to_include')
        working_languages = validated_data.get('working_languages_to_include')
        funding = validated_data.get('funding_to_include')
        trustworthiness_lower_bound = validated_data.get('trustworthiness_lower_bound')
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