from rest_framework import serializers
from findyourngo.restapi.models import Ngo, NgoAddress, NgoContact, NgoDataSource, NgoRepresentative, NgoMetaData, \
    NgoStats, NgoTWScore


class NgoDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoDataSource
        fields = ['credible', 'source']


class NgoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoAddress
        fields = ['street', 'postcode', 'city', 'country']


class NgoRepresentativeSerializer(serializers.ModelSerializer):
    representativeFirstName = serializers.CharField(source='representative_first_name')
    representativeLastName = serializers.CharField(source='representative_last_name')
    representativeEmail = serializers.EmailField(source='representative_email')

    class Meta:
        model = NgoRepresentative
        fields = ['representativeFirstName', 'representativeLastName', 'representativeEmail']


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
    presidentFirstName = serializers.CharField(source='president_first_name')
    presidentLastName = serializers.CharField(source='president_last_name')
    yearlyIncome = serializers.CharField(source='yearly_income')

    class Meta:
        model = NgoStats
        fields = ['foundingYear', 'staffNumber', 'memberNumber', 'workingLanguages', 'funding',
                  'presidentFirstName', 'presidentLastName', 'typeOfOrganization',
                  'yearlyIncome']


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

    class Meta:
        model = Ngo
        fields = ['id', 'name', 'acronym', 'aim', 'activities', 'branches', 'topics', 'accreditations', 'stats',
                  'contact', 'metaData', 'trustworthiness']
