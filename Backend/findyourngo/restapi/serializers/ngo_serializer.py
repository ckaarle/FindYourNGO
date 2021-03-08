from rest_framework import serializers
from django.db.models import Prefetch
from findyourngo.restapi.models import Ngo, NgoAddress, NgoContact, NgoDataSource, NgoRepresentative, NgoMetaData, \
    NgoStats, NgoTWScore, NgoReview, NgoEvent, NgoAccreditation, NgoBranch, NgoCountry, NgoTopic, NgoType, NgoConnection
from findyourngo.trustworthiness_calculator.AccreditationCalculator import AccreditationCalculator


class NgoDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoDataSource
        fields = ['credible', 'source']


class NgoCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoCountry
        fields = ['name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        country_representation = representation.pop('name')

        return country_representation


class NgoAddressSerializer(serializers.ModelSerializer):
    country = NgoCountrySerializer(read_only=True)

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
    presidentFirstName = serializers.CharField(source='president_first_name')
    presidentLastName = serializers.CharField(source='president_last_name')
    foundingYear = serializers.IntegerField(source='founding_year')
    staffNumber = serializers.IntegerField(source='staff_number')
    memberNumber = serializers.IntegerField(source='member_number')
    workingLanguages = serializers.CharField(source='working_languages')
    yearlyIncome = serializers.CharField(source='yearly_income')

    class Meta:
        model = NgoStats
        fields = ['foundingYear', 'staffNumber', 'memberNumber', 'workingLanguages', 'funding',
                  'presidentFirstName', 'presidentLastName', 'typeOfOrganization', 'yearlyIncome']


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


class NgoBranchSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = NgoBranch
        fields = ['country']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        country_representation = representation.pop('country')

        return country_representation


class NgoSerializer(serializers.ModelSerializer):
    branches = NgoBranchSerializer(read_only=True, many=True)

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


class NgoShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ngo
        fields = ['id', 'name']


class NgoEventSerializer(serializers.ModelSerializer):
    organizer = NgoShortSerializer(read_only=True)

    class Meta:
        model = NgoEvent
        fields = ['id', 'name', 'start_date', 'end_date', 'organizer', 'description', 'tags']


def update_ngo_instance(ngo: Ngo, ngo_update):
    ngo.activities = ngo_update['activities']
    ngo.aim = ngo_update['aim']
    update_ngo_contact(ngo, ngo_update)
    update_ngo_stats(ngo, ngo_update)
    update_ngo_accreditations(ngo, ngo_update)
    update_ngo_branches(ngo, ngo_update)
    update_ngo_topics(ngo, ngo_update)

    acc_calculator = AccreditationCalculator()
    valid_acc, wce = acc_calculator.has_valid_accreditation_and_wango_code_of_ethics((ngo))
    ngo.has_valid_accreditations = valid_acc
    ngo.has_wce = wce

    ngo.save()


def update_ngo_contact(ngo: Ngo, ngo_update):
    ngo_contact = NgoContact.objects.get(pk=ngo.contact_id)
    ngo_contact.ngo_phone_number = ngo_update['ngoPhoneNumber']
    ngo_contact.ngo_email = ngo_update['ngoEmail']
    ngo_contact.website = ngo_update['website']
    update_ngo_representative(ngo_contact, ngo_update)

    ngo_contact_address = NgoAddress.objects.get(pk=ngo_contact.address_id)
    ngo_contact_address.street = ngo_update['street']
    ngo_contact_address.city = ngo_update['city']
    ngo_contact_address.postcode = ngo_update['postcode']

    ngo_contact_address_country = NgoCountry.objects.get(pk=ngo_contact_address.country_id)
    ngo_contact_address_country.name = ngo_update['country']
    ngo_contact_address_country.save()
    ngo_contact_address.save()
    ngo_contact.save()


def update_ngo_representative(ngo_contact: NgoContact, ngo_update):
    ngo_contact_representative = ngo_contact.representative_id
    if ngo_contact_representative is None:
        ngo_contact_representative = NgoRepresentative.objects.create(
            representative_first_name=ngo_update['representativeFirstName'],
            representative_last_name=ngo_update['representativeLastName'],
            representative_email=ngo_update['representativeEmail'])
        ngo_contact.representative_id = ngo_contact_representative.id
    else:
        ngo_contact_representative = NgoRepresentative.objects.get(pk=ngo_contact.representative_id)
        ngo_contact_representative.representative_first_name = ngo_update['representativeFirstName']
        ngo_contact_representative.representative_last_name = ngo_update['representativeLastName']
        ngo_contact_representative.representative_email = ngo_update['representativeEmail']
        ngo_contact_representative.save()


def update_ngo_stats(ngo: Ngo, ngo_update):
    ngo_stats = NgoStats.objects.get(pk=ngo.stats_id)
    ngo_stats.founding_year = ngo_update['foundingYear']
    ngo_stats.staff_number = ngo_update['staffNumber']
    ngo_stats.member_number = ngo_update['memberNumber']
    ngo_stats.working_languages = ngo_update['workingLanguages']
    ngo_stats.funding = ngo_update['funding']
    ngo_stats.president_first_name = ngo_update['presidentFirstName']
    ngo_stats.president_last_name = ngo_update['presidentLastName']
    ngo_stats.yearly_income = ngo_update['yearlyIncome']
    update_ngo_types(ngo_stats, ngo_update)
    ngo_stats.save()


def update_ngo_accreditations(ngo: Ngo, ngo_update):
    ngo.accreditations.clear()
    updated_accreditations = ngo_update['accreditations']
    for accreditation in updated_accreditations:
        if NgoAccreditation.objects.filter(accreditation=accreditation).exists():
            existing_accreditation = NgoAccreditation.objects.filter(accreditation=accreditation).first()
            ngo.accreditations.add(existing_accreditation)
        else:
            new_accreditation = NgoAccreditation.objects.create(accreditation=accreditation)
            ngo.accreditations.add(new_accreditation)


def update_ngo_branches(ngo: Ngo, ngo_update):
    ngo.branches.clear()
    updated_branches = ngo_update['branches']
    for branch in updated_branches:
        if NgoBranch.objects.filter(country__name=branch)\
                .prefetch_related(Prefetch('country', queryset=NgoCountry.objects.filter(name=branch))).exists():
            existing_branch = NgoBranch.objects.get(country__name=branch)\
                .prefetch_related(Prefetch('country', queryset=NgoCountry.objects.filter(name=branch))).first()
            ngo.branches.add(existing_branch)
        else:
            continue  # assuming all countries have been created, no new countries should be creatable


def update_ngo_topics(ngo: Ngo, ngo_update):
    ngo.topics.clear()
    updated_topics = ngo_update['topics']
    for topic in updated_topics:
        if NgoTopic.objects.filter(topic=topic).exists():
            existing_topic = NgoTopic.objects.filter(topic=topic).first()
            ngo.topics.add(existing_topic)
        else:
            new_topic = NgoTopic.objects.create(topic=topic)
            ngo.topics.add(new_topic)


def update_ngo_types(ngo_stats: NgoStats, ngo_update):
    ngo_stats.type_of_organization.clear()
    updated_types = ngo_update['typeOfOrganization']
    for updated_type in updated_types:
        if NgoType.objects.filter(type=updated_type).exists():
            existing_type = NgoType.objects.filter(type=updated_type).first()
            ngo_stats.type_of_organization.add(existing_type)
        else:
            new_type = NgoType.objects.create(type=updated_type)
            ngo_stats.type_of_organization.add(new_type)


class NgoPlotSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    trustworthiness = serializers.SlugRelatedField(
        read_only=True,
        slug_field='total_tw_score',
        source='tw_score'
    )

    def get_coordinates(self, obj):
        address = obj.contact.address
        lat = address.latitude
        long = address.longitude
        return lat, long

    class Meta:
        model = Ngo
        fields = ['id', 'name', 'coordinates', 'trustworthiness']


class NgoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgoConnection
        fields = ['id', 'connected_ngo_id', 'reporter_id']
