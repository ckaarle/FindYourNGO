from rest_framework import serializers
from findyourngo.restapi.models import Ngo, NgoAddress, NgoContact


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


class NgoOverviewItemSerializer(serializers.ModelSerializer):
    city = NgoOverviewItemContactSerializer(source="contact")

    class Meta:
        model = Ngo
        fields = ['id', 'name', 'acronym', 'city']

    def to_internal_value(self, data):
        address_internal = {}
        for key in NgoOverviewItemContactSerializer.Meta.fields:
            if key in data:
                address_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['city'] = address_internal
        return internal
