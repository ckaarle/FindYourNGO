from typing import List, Optional

from findyourngo.data_import.InfoClasses import Info
from findyourngo.data_import.european_council.parser import parse_european_council
from findyourngo.restapi.models import Ngo, NgoBranch, NgoTopic, NgoAccreditation, NgoDataSource, NgoMetaData, \
    NgoAddress, NgoRepresentative, NgoContact, NgoStats


def convert_ngo_branch(info: Info) -> List[NgoBranch]:
    countries = info.detail_info.soft_facts.greographical_representation

    if countries is None:
        return []

    branches = []
    for country in countries:
        country_name = country.upper()

        try:
            existing_branches = NgoBranch.objects.get(country=country_name)
            branch = existing_branches
        except:
            branch = NgoBranch.objects.create(country=country_name)

        branches.append(branch)

    return branches


def convert_ngo_topic(info: Info) -> List[NgoTopic]:
    aocs = info.detail_info.soft_facts.areas_of_competence

    if aocs is None:
        return []

    topics = []
    for aoc in aocs:
        aoc_name = aoc.upper()

        try:
            existing_topics = NgoTopic.objects.get(topic=aoc_name)
            topic = existing_topics
        except:
            topic = NgoTopic.objects.create(topic=aoc_name)

        topics.append(topic)

    return topics


def convert_ngo_accreditation(info: Info) -> List[NgoAccreditation]:
    accreditation = info.detail_info.soft_facts.accreditations

    if accreditation is None or not accreditation:
        return []

    acc_name = accreditation.upper()

    try:
        existing_accreditations = NgoAccreditation.objects.get(topic=acc_name)
        acc = existing_accreditations
    except:
        acc = NgoAccreditation.objects.create(accreditation=acc_name)

    return [acc]


def convert_ngo_data_source(data_source: str, source_credible: bool) -> List[NgoDataSource]:
    try:
        source = NgoDataSource.objects.get(source=data_source)
    except:
        source = NgoDataSource.objects.create(credible=source_credible, source=data_source)

    return [source]


def format_for_postgres(date: str) -> str:
    try:
        return date[0:10]
    except:
        return ''


def convert_ngo_meta_data(info: Info, data_sources: List[NgoDataSource]) -> NgoMetaData:
    last_updated = info.detail_info.last_updated
    last_updated = format_for_postgres(last_updated)

    meta_data = NgoMetaData.objects.create(last_updated=last_updated)
    for data_source in data_sources:
        meta_data.info_source.add(data_source)

    return meta_data


def set_to_empty_string_if_none_upper_else(string: str) -> str:
    return '' if string is None or not string else string.upper()


def all_empty_string(strings: List[str]) -> bool:
    return all([s is None or s == '' for s in strings])


def convert_ngo_address(info: Info) -> Optional[NgoAddress]:
    street_formatted = set_to_empty_string_if_none_upper_else(info.main_info.address.street)
    post_code_formatted = set_to_empty_string_if_none_upper_else(info.main_info.address.postcode)
    city_formatted = set_to_empty_string_if_none_upper_else(info.main_info.address.city)
    country_formatted = set_to_empty_string_if_none_upper_else(info.main_info.address.country)

    if all_empty_string([street_formatted, post_code_formatted, city_formatted, country_formatted]):
        return None

    try:
        address = NgoAddress.objects.get(street=street_formatted, postcode=post_code_formatted, city=city_formatted, country=country_formatted)
    except:
        address = NgoAddress.objects.create(street=street_formatted, postcode=post_code_formatted, city=city_formatted, country=country_formatted)

    return address


def convert_ngo_representative(info: Info) -> Optional[NgoRepresentative]:
    first_name = set_to_empty_string_if_none_upper_else(info.main_info.representative.representative_firstname)
    last_name = set_to_empty_string_if_none_upper_else(info.main_info.representative.representative_lastname)
    email = set_to_empty_string_if_none_upper_else(info.main_info.representative.representative_email)

    if all_empty_string([email, first_name, last_name]):
        return None

    try:
        rep = NgoRepresentative.objects.get(representative_first_name=first_name, representative_last_name=last_name, representative_email=email)
    except:
        rep = NgoRepresentative.objects.create(representative_first_name=first_name, representative_last_name=last_name, representative_email=email)

    return rep


def convert_ngo_contact(info: Info, address: Optional[NgoAddress], rep: Optional[NgoRepresentative]) -> Optional[NgoContact]:
    phone = set_to_empty_string_if_none_upper_else(info.main_info.contact.phone_number)
    email = set_to_empty_string_if_none_upper_else(info.main_info.contact.email)
    website = set_to_empty_string_if_none_upper_else(info.detail_info.hard_facts.website)


    if all_empty_string([phone, email, website]) and address is None and rep is None:
        return None

    try:
        if address is None and rep is None:
            contact = NgoContact.objects.get(ngo_phone_number=phone, ngo_email=email, website=website)
        elif address is None:
            contact = NgoContact.objects.get(ngo_phone_number=phone, ngo_email=email, website=website, representative=rep)
        elif rep is None:
            contact = NgoContact.objects.get(ngo_phone_number=phone, ngo_email=email, website=website, address=address)
        else:
            contact = NgoContact.objects.get(ngo_phone_number=phone, ngo_email=email, website=website, representative=rep, address=address)
    except:
        if address is None and rep is None:
            contact = NgoContact.objects.create(ngo_phone_number=phone, ngo_email=email, website=website)
        elif address is None:
            contact = NgoContact.objects.create(ngo_phone_number=phone, ngo_email=email, website=website, representative=rep)
        elif rep is None:
            contact = NgoContact.objects.create(ngo_phone_number=phone, ngo_email=email, website=website, address=address)
        else:
            contact = NgoContact.objects.create(ngo_phone_number=phone, ngo_email=email, website=website, representative=rep, address=address)

    return contact


def convert_ngo_stats(info: Info) -> Optional[NgoStats]:
    founding_year = info.detail_info.hard_facts.founding_year
    staff_number = info.detail_info.hard_facts.staff_number
    member_number = info.detail_info.hard_facts.members
    working_languages = set_to_empty_string_if_none_upper_else(info.detail_info.hard_facts.working_languages)
    funding = set_to_empty_string_if_none_upper_else(info.main_info.name.funding)
    president_first_name = set_to_empty_string_if_none_upper_else(info.detail_info.hard_facts.president_firstname)
    president_last_name = set_to_empty_string_if_none_upper_else(info.detail_info.hard_facts.president_lastname)
    type_of_organization = set_to_empty_string_if_none_upper_else(info.main_info.name.type_of_organization)
    yearly_income = set_to_empty_string_if_none_upper_else(info.main_info.name.yearly_income)

    if all_empty_string([founding_year, staff_number, member_number, working_languages, funding, president_first_name, president_last_name, type_of_organization, yearly_income]):
        return None

    try:
        stats = NgoStats.objects.get(
            founding_year=founding_year,
            staff_number=staff_number,
            member_number=member_number,
            working_languages=working_languages,
            funding=funding,
            president_first_name=president_first_name,
            president_last_name=president_last_name,
            type_of_organization=type_of_organization,
            yearly_income=yearly_income,
        )
    except:
        stats = NgoStats.objects.create(
            founding_year=founding_year,
            staff_number=staff_number,
            member_number=member_number,
            working_languages=working_languages,
            funding=funding,
            president_first_name=president_first_name,
            president_last_name=president_last_name,
            type_of_organization=type_of_organization,
            yearly_income=yearly_income,
        )

    return stats


def convert_ngo(
        info: Info,
        branch: List[NgoBranch],
        topic: List[NgoTopic],
        accreditation: List[NgoAccreditation],
        meta_data: NgoMetaData,
        contact: Optional[NgoContact],
        stats: Optional[NgoStats],
) -> Ngo:
    name = set_to_empty_string_if_none_upper_else(info.main_info.name.name)
    if name is None or not name:
        raise AssertionError('Name of organization has to be set')
    acronym = set_to_empty_string_if_none_upper_else(info.main_info.name.acronym)

    aim = set_to_empty_string_if_none_upper_else(info.detail_info.soft_facts.aims)
    activities = set_to_empty_string_if_none_upper_else(info.detail_info.soft_facts.activities)

    try: # TODO this is the initial data import
        # do not use this for subsequent imports (obviously, ngos might already be in the database)
        Ngo.objects.get(name=name, acronym=acronym)
        print(f'XXXXXXXXXXXXXXXXXXXXXXXX --- Ngo with name {name} and acronym {acronym} already in database -- skipping')
    except:
        ngo = Ngo.objects.create(
            name=name,
            acronym=acronym,
            aim=aim,
            activities=activities,
            stats=stats,
            contact=contact,
            meta_data=meta_data,
        )
        for b in branch:
            ngo.branches.add(b.id)

        for t in topic:
            ngo.topics.add(t.id)

        for a in accreditation:
            ngo.accreditations.add(a.id)

    return ngo


def convert_to_model_classes(infos: List[Info], data_source: str, source_credible: bool = False) -> None:
    for idx, info in enumerate(infos):
        print(f'STARTING TO IMPORT info # {idx}')
        branch = convert_ngo_branch(info) # can be empty
        topic = convert_ngo_topic(info) # can be empty
        accreditation = convert_ngo_accreditation(info) # can be empty

        data_sources = convert_ngo_data_source(data_source, source_credible)
        meta_data = convert_ngo_meta_data(info, data_sources)

        address = convert_ngo_address(info) # can be null
        representative = convert_ngo_representative(info) # can be null
        contact = convert_ngo_contact(info, address, representative) # can be null

        stats = convert_ngo_stats(info)

        ngo = convert_ngo(info, branch, topic, accreditation, meta_data, contact, stats)
        print(f'IMPORT info # {idx} FINISHED')


def run_initial_data_import() -> bool:
    print('TRYING TO IMPORT DATA')
    if database_not_empty():
        return False
    print('STARTING THE DATA IMPORT')
    european_council_info = parse_european_council()

    # TODO do not use this method for other, secondary data sources
    convert_to_model_classes(european_council_info, 'European Council', True)

    print('DATA IMPORT FINISHED')
    return True


def database_not_empty() -> bool:
    return Ngo.objects.all()