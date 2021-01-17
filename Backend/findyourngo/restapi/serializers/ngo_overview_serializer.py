from rest_framework import serializers
from findyourngo.restapi.models import Ngo, NgoAddress, NgoContact, NgoTWScore, NgoReview


class NgoOverviewItemAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoAddress
        fields = ['city']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        city_representation = representation.pop('city')

        return city_representation


class NgoOverviewItemContactSerializer(serializers.ModelSerializer):
    city = NgoOverviewItemAddressSerializer(source="address")

    class Meta:
        model = NgoContact
        fields = ['city']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        address_representation = representation.pop('city')

        return address_representation


class NgoOverviewItemTWScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoTWScore
        fields = ['total_tw_score']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tw_score_representation = representation.pop('total_tw_score')

        return tw_score_representation


class NgoOverviewItemSerializer(serializers.ModelSerializer):
    trustworthiness = NgoOverviewItemTWScoreSerializer(source="tw_score")
    city = NgoOverviewItemContactSerializer(source="contact")
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return NgoReview.objects.filter(ngo=obj.id).count()

    class Meta:
        model = Ngo
        fields = ['id', 'name', 'acronym', 'city', 'trustworthiness', 'amount']

    def to_internal_value(self, data):
        values_internal = {}
        for key in NgoOverviewItemContactSerializer.Meta.fields:
            if key in data:
                values_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['city'] = values_internal
        internal['trustworthiness'] = values_internal
        return internal
