from rest_framework import serializers
from findyourngo.restapi.models import Ngo, NgoAddress, NgoContact, NgoDataSource, NgoRepresentative, NgoMetaData, \
    NgoStats, NgoTWScore, NgoReview


class NgoDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoDataSource
        fields = ['credible', 'source']


class NgoAddressSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        if obj.street == '':
            if obj.postcode == '' or obj.city == '':
                if obj.country == '':
                    return ''
                return obj.country
            elif obj.country == '':
                return f"{obj.postcode} {obj.city}"
            return f"{obj.postcode} {obj.city}, {obj.country}"
        elif obj.postcode == '' or obj.city == '':
            if obj.country == '':
                return obj.street
            return f"{obj.street}, {obj.country}"
        elif obj.country == '':
            return f"{obj.street}, {obj.postcode} {obj.city}"
        return f"{obj.street}, {obj.postcode} {obj.city}, {obj.country}"

    class Meta:
        model = NgoAddress
        fields = ['address']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representative_address = representation.pop('address')

        return representative_address


class NgoRepresentativeSerializer(serializers.ModelSerializer):
    representative = serializers.SerializerMethodField()

    def get_representative(self, obj):
        if obj.representative_first_name == '':
            if obj.representative_last_name == '':
                if obj.representative_email == '':
                    return ''
                return obj.representative_email
            elif obj.representative_email == '':
                return obj.representative_last_name
            return f"{obj.representative_last_name}, {obj.representative_email}"
        elif obj.representative_last_name == '':
            if obj.representative_email == '':
                return ''
            return obj.representative_email
        elif obj.representative_email == '':
            return f"{obj.representative_first_name} {obj.representative_last_name}"
        return f"{obj.representative_first_name} {obj.representative_last_name}, {obj.representative_email}"

    class Meta:
        model = NgoRepresentative
        fields = ['representative']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representative_representation = representation.pop('representative')

        return representative_representation


class NgoStatsSerializer(serializers.ModelSerializer):
    typeOfOrganization = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type',
        source='type_of_organization'
    )
    foundingYear = serializers.IntegerField(source='founding_year')
    staffNumber = serializers.IntegerField(source='staff_number')
    memberNumber = serializers.IntegerField(source='member_number')
    workingLanguages = serializers.CharField(source='working_languages')
    yearlyIncome = serializers.CharField(source='yearly_income')

    president = serializers.SerializerMethodField()

    def get_president(self, obj):
        if obj.president_first_name == '':
            if obj.president_last_name == '':
                return ''
            return obj.president_last_name
        elif obj.president_last_name == '':
            return obj.president_first_name
        return f"{obj.president_first_name} {obj.president_last_name}"

    class Meta:
        model = NgoStats
        fields = ['foundingYear', 'staffNumber', 'memberNumber', 'workingLanguages', 'funding',
                  'president', 'typeOfOrganization', 'yearlyIncome']


class NgoTWSerializer(serializers.ModelSerializer):
    totalTwScore = serializers.FloatField(source='total_tw_score')
    numberDataSourcesScore = serializers.FloatField(source='number_data_sources_score')
    credibleSourceScore = serializers.FloatField(source='credible_source_score')
    ecosocScore = serializers.FloatField(source='ecosoc_score')

    class Meta:
        model = NgoTWScore
        fields = ['totalTwScore', 'numberDataSourcesScore', 'credibleSourceScore', 'ecosocScore']


class NgoContactSerializer(serializers.ModelSerializer):
    ngoPhoneNumber = serializers.CharField(source='ngo_phone_number')
    ngoEmail = serializers.EmailField(source="ngo_email")
    address = NgoAddressSerializer(read_only=True)
    representative = NgoRepresentativeSerializer(read_only=True)

    class Meta:
        model = NgoContact
        fields = ['ngoPhoneNumber', 'ngoEmail', 'website', 'address', 'representative']


class NgoMetaDataSerializer(serializers.ModelSerializer):
    lastUpdated = serializers.DateField(source='last_updated')
    infoSource = NgoDataSourceSerializer(read_only=True, many=True, source='info_source')

    class Meta:
        model = NgoMetaData
        fields = ['lastUpdated', 'infoSource']


class NgoSerializer(serializers.ModelSerializer):
    branches = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='country'
    )

    topics = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='topic'
    )

    accreditations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='accreditation'
    )

    trustworthiness = serializers.SlugRelatedField(
        read_only=True,
        slug_field='total_tw_score',
        source='tw_score'
    )

    stats = NgoStatsSerializer(read_only=True)
    contact = NgoContactSerializer(read_only=True)
    metaData = NgoMetaDataSerializer(source='meta_data', read_only=True)
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return NgoReview.objects.filter(ngo=obj.id).count()

    class Meta:
        model = Ngo
        fields = ['id', 'name', 'acronym', 'aim', 'activities', 'branches', 'topics', 'accreditations', 'stats',
                  'contact', 'metaData', 'trustworthiness', 'amount']
