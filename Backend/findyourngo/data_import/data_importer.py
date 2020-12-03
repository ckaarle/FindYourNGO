import pickle
from typing import List, Optional

from findyourngo.data_import.InfoClasses import Info
from findyourngo.data_import.european_council.parser import parse_european_council
from findyourngo.restapi.models import Ngo, NgoBranch, NgoTopic, NgoAccreditation, NgoDataSource, NgoMetaData, \
    NgoAddress, NgoRepresentative, NgoContact, NgoStats, NgoType


def _invalid_country(country: str) -> bool:
    if 'COUNTRIES' in country:
        return True

    if 'AND NORTH' in country:
        return True

    if 'CENTRAL ASIA' in country:
        return True

    if 'EASTERN AFRICA' in country:
        return True

    if 'IN OVER' in country:
        return True

    if country == 'LATIN AMERICA':
        return True

    if 'MIDDLE EAST' in country:
        return True

    if 'MINORITY RIGHTS GROUP' in country:
        return True

    if 'SOUTH AND SOUTHEAST' in country:
        return True

    if 'THE MEDITERRANEAN' in country:
        return True

    if 'THE SOUTH CAUCASUS' in country:
        return True

    if 'WESTERN SAHARA' in country:
        return True

    if country == 'EUROPEAN UNION' or country == 'EUROPE' or country == 'EU':
        return True

    if country == 'AFRICA':
        return True

    return False


def convert_ngo_branch(info: Info) -> List[NgoBranch]:
    countries = info.detail_info.soft_facts.greographical_representation

    if countries is None:
        return []

    branches = []
    for country in countries:
        country = _fix_country(country)

        if _invalid_country(country):
            continue
        try:
            existing_branches = NgoBranch.objects.get(country=country)
            branch = existing_branches
        except:
            branch = NgoBranch.objects.create(country=country)

        branches.append(branch)

    return branches


def _fix_topic(aoc: str) -> str:
    if aoc == 'Education for Democratic Citizenship':
        aoc = 'Education for democratic Citizenship'
    if aoc == 'Environment and sustanable development':
        aoc = 'Environment and sustainable development'
    if aoc == 'Fight against povery and social exclusion':
        aoc = 'Fight against poverty and social exclusion'
    if aoc == 'Human rights':
        aoc = 'Human Rights'
    if aoc == 'local and regional democracy':
        aoc = 'Local and regional democracy'
    if aoc == 'Social Cohension':
        aoc = 'Social Cohesion'

    return aoc


def convert_ngo_topic(info: Info) -> List[NgoTopic]:
    aocs = info.detail_info.soft_facts.areas_of_competence

    if aocs is None:
        return []

    topics = []
    for aoc in aocs:
        aoc = aoc.strip()
        aoc = _fix_topic(aoc)
        try:
            existing_topics = NgoTopic.objects.get(topic=aoc)
            topic = existing_topics
        except:
            topic = NgoTopic.objects.create(topic=aoc)

        topics.append(topic)

    return topics


def convert_ngo_accreditation(info: Info) -> List[NgoAccreditation]:
    accreditation = info.detail_info.soft_facts.accreditations

    if accreditation is not None:
        accreditation = accreditation.strip()

    if accreditation is None or not accreditation:
        return []

    try:
        existing_accreditations = NgoAccreditation.objects.get(topic=accreditation)
        acc = existing_accreditations
    except:
        acc = NgoAccreditation.objects.create(accreditation=accreditation)

    return [acc]


def convert_ngo_data_source(data_source: str, source_credible: bool) -> List[NgoDataSource]:
    try:
        source = NgoDataSource.objects.get(source=data_source)
    except:
        source = NgoDataSource.objects.create(credible=source_credible, source=data_source)

    return [source]


def format_for_postgres(date: str) -> Optional[str]:
    if not date:
        return None
    try:
        return date[0:10].strip()
    except:
        return None


def convert_ngo_meta_data(info: Info, data_sources: List[NgoDataSource]) -> NgoMetaData:
    last_updated = info.detail_info.last_updated.strip()
    last_updated = format_for_postgres(last_updated)

    meta_data = NgoMetaData.objects.create(last_updated=last_updated)
    for data_source in data_sources:
        meta_data.info_source.add(data_source)

    return meta_data


def set_to_empty_string_if_none_upper_else(string: str) -> str:
    return '' if string is None or not string else string.strip().upper()


def set_to_empty_string_if_none(string: str) -> str:
    return '' if string is None or not string else string.strip()


def all_empty_string(strings: List[str]) -> bool:
    return all([s is None or s == '' for s in strings])


def _fix_address_country(country: str) -> str:
    if country is None:
        return country

    if country == '47 avenue de la résistance 93104 Montreuil Cedex':
        country = 'France'

    if country == '(not available for security reasons)':
        country = ''

    if country == '1F., No.2-1, Shunan St., Xindian Dist., New Taipei City, 23143, Taiwan':
        country = 'Taiwan'

    if 'FÉDÉRATION HANDICAP INTERNATIONAL' in country:
        country = 'France'

    if 'NEW YORK OFFICE' in country:
        country = 'Switzerland'

    if 'Discovery House' in country:
        country = 'United Kingdom'

    if '19 Rea St South Digbeth, Birmingham B5 6LB UK' in country:
        country = 'United Kingdom'

    if 'Street Masoud Bin Saed, P.O. Box 2943 , Amman 11181, Jordan' in country:
        country = 'Jordan'

    if 'Oxfam House, John Smith Drive, Oxford OX4 2JY, UK' in country:
        country = 'United Kingdom'

    if '191028, Russia,' in country:
        country = 'Russia'

    if '888 Commonwealth Avenue, 3rd floor, Boston, MA 02215 USA' in country:
        country = 'USA'

    if '100, rue des fougères' in country:
        country = 'France'

    if 'USA & Amsterdam' in country:
        country = 'USA'

    if '501 Kings Highway East, Suite 400, Fairfield, CT 06825 USA' in country:
        country = 'USA'

    if '301/301, Voluntários da Pátria, 22270-003, Rio de Janeiro, Rio de Janeiro, Brazil.' in country:
        country = 'Brazil'

    if 'c/o Scorpio Corporate Advisors S-405 (LGF), Greater Kailash - II New Delhi 110 048 India' in country:
        country = 'India'

    if 'Parkstraat 83' in country:
        country = 'Netherlands'

    if 'SolarAid' in country:
        country = 'United Kingdom'

    if '6 Charterhouse Buildings, London EC1M 7ET, UK' in country:
        country = 'United Kingdom'

    if '2015 Australia' in country:
        country = 'Australia'

    if 'House No: 08(1st floor), Main Road, Block: C' in country:
        country = 'Bangladesh'

    if 'Rua Aspicuelta, 678, Vila Madalena - Zip Code: 05433-011, Sao Paulo/SP, Brazil.' in country:
        country = 'Brazil'

    if 'COMMUNICATIONS HOUSE, 26 YORK STREET, LONDON, W1U 6PZ, UK' in country:
        country = 'United Kingdom'

    if 'PO Box 4130,' in country:
        country = 'Netherlands'

    return country


def convert_ngo_address(info: Info) -> Optional[NgoAddress]:
    street_formatted = set_to_empty_string_if_none(info.main_info.address.street)
    post_code_formatted = set_to_empty_string_if_none(info.main_info.address.postcode)
    city_formatted = set_to_empty_string_if_none(info.main_info.address.city)
    country_formatted = set_to_empty_string_if_none(info.main_info.address.country)
    country_formatted = _fix_address_country(country_formatted)

    if all_empty_string([street_formatted, post_code_formatted, city_formatted, country_formatted]):
        return None

    try:
        address = NgoAddress.objects.get(street=street_formatted, postcode=post_code_formatted, city=city_formatted, country=country_formatted)
    except:
        address = NgoAddress.objects.create(street=street_formatted, postcode=post_code_formatted, city=city_formatted, country=country_formatted)

    return address


def convert_ngo_representative(info: Info) -> Optional[NgoRepresentative]:
    first_name = set_to_empty_string_if_none(info.main_info.representative.representative_firstname)
    last_name = set_to_empty_string_if_none(info.main_info.representative.representative_lastname)
    email = set_to_empty_string_if_none(info.main_info.representative.representative_email)

    if all_empty_string([email, first_name, last_name]):
        return None

    try:
        rep = NgoRepresentative.objects.get(representative_first_name=first_name, representative_last_name=last_name, representative_email=email)
    except:
        rep = NgoRepresentative.objects.create(representative_first_name=first_name, representative_last_name=last_name, representative_email=email)

    return rep


def convert_ngo_contact(info: Info, address: Optional[NgoAddress], rep: Optional[NgoRepresentative]) -> Optional[NgoContact]:
    phone = set_to_empty_string_if_none(info.main_info.contact.phone_number)
    email = set_to_empty_string_if_none(info.main_info.contact.email)
    website = set_to_empty_string_if_none(info.detail_info.hard_facts.website)


    if all_empty_string([phone, email, website]) and address is None and rep is None:
        return None

    if phone and ',' in phone:
        phone = phone.split(',')[0].strip()
    if phone and 'Mark the front of the envelope with Rule 39' in phone: # wtf
        phone = ''

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


def _default_zero_if_none(value: Optional[int]) -> int:
    return value if value is not None else 0


def convert_ngo_stats(info: Info) -> Optional[NgoStats]:
    founding_year = info.detail_info.hard_facts.founding_year
    staff_number = _default_zero_if_none(info.detail_info.hard_facts.staff_number)
    member_number = _default_zero_if_none(info.detail_info.hard_facts.members)
    if member_number is None:
        member_number = 0
    working_languages = set_to_empty_string_if_none(info.detail_info.hard_facts.working_languages)
    funding = set_to_empty_string_if_none(info.main_info.name.funding)
    president_first_name = set_to_empty_string_if_none(info.detail_info.hard_facts.president_firstname)
    president_last_name = set_to_empty_string_if_none(info.detail_info.hard_facts.president_lastname)

    type = info.main_info.name.type_of_organization
    if type is None:
        type = []
    yearly_income = set_to_empty_string_if_none(info.main_info.name.yearly_income)

    if all_empty_string([founding_year, staff_number, member_number, working_languages, funding, president_first_name, president_last_name, yearly_income]) and not type:
        return None

    types_of_organization = []
    for t in type:
        t = t.strip()
        try:
            type_of_organization = NgoType.objects.get(type=t)
        except:
            type_of_organization = NgoType.objects.create(type=t)
        types_of_organization.append(type_of_organization)

    try:
        stats = NgoStats.objects.get(
            founding_year=founding_year,
            staff_number=staff_number,
            member_number=member_number,
            working_languages=working_languages,
            funding=funding,
            president_first_name=president_first_name,
            president_last_name=president_last_name,
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
            yearly_income=yearly_income,
        )
        for t in types_of_organization:
            stats.type_of_organization.add(t.id)

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
    name = name.strip().upper() # to avoid conflicts
    acronym = set_to_empty_string_if_none_upper_else(info.main_info.name.acronym)

    aim = set_to_empty_string_if_none(info.detail_info.soft_facts.aims)
    activities = set_to_empty_string_if_none(info.detail_info.soft_facts.activities)

    if name == 'ZTESTING':
        aim = ''
        activities = ''

    try:
        # do not use this for subsequent imports as default (obviously, ngos might already be in the database)
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


def convert_to_model_classes(infos: List[Info], data_source: str, source_credible: bool = False, index: Optional[int] = None) -> None:
    for idx, info in enumerate(infos):
        i = idx if index is None else index
        print(f'STARTING TO IMPORT ({data_source}) info # {i}')
        branch = convert_ngo_branch(info) # can be empty
        topic = convert_ngo_topic(info) # can be empty
        accreditation = convert_ngo_accreditation(info) # can be empty

        data_sources = convert_ngo_data_source(data_source, source_credible)
        meta_data = convert_ngo_meta_data(info, data_sources)

        address = convert_ngo_address(info) # can be null
        representative = convert_ngo_representative(info) # can be null
        contact = convert_ngo_contact(info, address, representative) # can be null

        stats = convert_ngo_stats(info)

        before = Ngo.objects.all()
        len_before = len(before)
        ngo = convert_ngo(info, branch, topic, accreditation, meta_data, contact, stats)
        after = Ngo.objects.all()

        print(f'Before {len_before} - after {len(after)}')
        assert len_before + 1 == len(after)
        print(f'IMPORT info # {idx} FINISHED')


def deserialize(filename: str) -> List[Info]:
    infos = []
    with open(filename, 'rb') as f:
        try:
            while True:
                infos.append(pickle.load(f))
        except EOFError:
            pass

    return infos


def _print_comparison(info_match: Ngo, info: Info) -> None:
    print('----------------------')
    print(f'Comparing NGO {info.main_info.name.name.upper()} (EU) - (NgoAdvisor)')

    print(f'Name: {info_match.name} - {info.main_info.name.name.upper()}')
    print(f'Acronym: {info_match.acronym} - {info.main_info.name.acronym}')
    print(f'Aim: {info_match.aim} - {info.detail_info.soft_facts.aims}')
    print(f'Activities: {info_match.activities} - {info.detail_info.soft_facts.activities}')
    print(f'Branches: {info_match.branches} - {info.detail_info.soft_facts.greographical_representation}')
    print(f'Topics: {info_match.topics} - {info.detail_info.soft_facts.areas_of_competence}')
    print(f'Accreditations: {info_match.accreditations} - {info.detail_info.soft_facts.accreditations}')

    if info_match.stats:
        print(f'Founding year: {info_match.stats.founding_year} - {info.detail_info.hard_facts.founding_year}')
        print(f'Staff: {info_match.stats.staff_number} - {info.detail_info.hard_facts.staff_number}')
        print(f'Member: {info_match.stats.member_number} - {info.detail_info.hard_facts.members}')
        print(f'Working languages: {info_match.stats.working_languages} - {info.detail_info.hard_facts.working_languages}')
        print(f'Funding: {info_match.stats.funding} - {info.main_info.name.funding}')
        print(f'Pres first name: {info_match.stats.president_first_name} - {info.detail_info.hard_facts.president_firstname}')
        print(f'Pres last name: {info_match.stats.president_last_name} - {info.detail_info.hard_facts.president_lastname}')
        print(f'Type: {info_match.stats.type_of_organization} - {info.main_info.name.type_of_organization}')
        print(f'Yearly income: {info_match.stats.yearly_income} - {info.main_info.name.yearly_income}')
    else:
        print(f'Founding year:  - {info.detail_info.hard_facts.founding_year}')
        print(f'Staff: - {info.detail_info.hard_facts.staff_number}')
        print(f'Member: - {info.detail_info.hard_facts.members}')
        print(f'Working languages: - {info.detail_info.hard_facts.working_languages}')
        print(f'Funding: - {info.main_info.name.funding}')
        print(f'Pres first name: - {info.detail_info.hard_facts.president_firstname}')
        print(f'Pres last name: - {info.detail_info.hard_facts.president_lastname}')
        print(f'Type: - {info.main_info.name.type_of_organization}')
        print(f'Yearly income: - {info.main_info.name.yearly_income}')

    if info_match.contact:
        print(f'Phone number: {info_match.contact.ngo_phone_number} - {info.main_info.contact.phone_number}')
        print(f'Email: {info_match.contact.ngo_email} - {info.main_info.contact.email}')
        print(f'Website: {info_match.contact.website} - {info.detail_info.hard_facts.website}')
        print(f'Street: {info_match.contact.address.street} - {info.main_info.address.street}')
        print(f'Postcode: {info_match.contact.address.postcode} - {info.main_info.address.postcode}')
        print(f'City: {info_match.contact.address.city} - {info.main_info.address.city}')
        print(f'Country: {info_match.contact.address.country} - {info.main_info.address.country}')
        print(f'Rep first name: {info_match.contact.representative.representative_first_name} - {info.main_info.representative.representative_firstname}')
        print(f'Rep last name: {info_match.contact.representative.representative_last_name} - {info.main_info.representative.representative_lastname}')
        print(f'Rep email: {info_match.contact.representative.representative_email} - {info.main_info.representative.representative_email}')

    if info_match.meta_data:
        print(f'Last updated: {info_match.meta_data.last_updated} - {info.detail_info.last_updated}')
    print('----------------------')


def _update_with_ngo_advisor_info(info_match: Ngo, info: Info) -> None:
    if info_match.name == 'AMNESTY INTERNATIONAL':
        info_match.contact.address.country = info.main_info.address.country.strip()
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'ASSOCIATION FOR THE PREVENTION OF TORTURE':
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'BALKAN CIVIL SOCIETY DEVELOPMENT NETWORK':
        _add_all_types(info, info_match)
    elif info_match.name == 'CHILD HELPLINE INTERNATIONAL':
        _add_all_branches(info, info_match)

        # just to make sure it has actual numbers and not None
        info.detail_info.hard_facts.staff_number = 0
        info.detail_info.hard_facts.members = 0
        stats = convert_ngo_stats(info)
        info_match.stats = stats

        _add_all_topics(info, info_match)
        _add_all_types(info, info_match)
    elif info_match.name == 'DEFENCE FOR CHILDREN INTERNATIONAL':
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'HUMAN RIGHTS WATCH':
        info_match.stats.founding_year = info.detail_info.hard_facts.founding_year
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'INTERNATIONAL COMMISSION OF JURISTS':
        info_match.stats.founding_year = info.detail_info.hard_facts.founding_year
        info_match.contact.website = info.detail_info.hard_facts.website.strip()
        info_match.contact.address.city = info.main_info.address.city.strip()
        info_match.contact.address.country = info.main_info.address.country.strip()
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'TRANSPARENCY INTERNATIONAL':
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'WORLD ORGANISATION AGAINST TORTURE':
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'INTERNATIONAL DETENTION COALITION':
        _add_all_types(info, info_match)
        _add_all_branches(info, info_match)
        _add_all_topics(info, info_match)
    elif info_match.name == 'CHILD RIGHTS INTERNATIONAL NETWORK':
        info.detail_info.hard_facts.staff_number = 0
        info.detail_info.hard_facts.members = 0
        stats = convert_ngo_stats(info)
        info_match.stats = stats

        info_match.stats.founding_year = info.detail_info.hard_facts.founding_year
        info_match.contact.website = info.detail_info.hard_facts.website.strip()
        info_match.contact.address.city = info.main_info.address.city.strip()

        _add_all_types(info, info_match)
        _add_all_topics(info, info_match)
    else:
        raise ValueError(f'Unexpected NGO match found: {info_match.name}')

    info_match.save()


def _add_all_types(info: Info, info_match: Ngo) -> None:
    for type in info.main_info.name.type_of_organization:
        type = type.strip()
        try:
            type_of_organization = NgoType.objects.get(type=type)
        except:
            type_of_organization = NgoType.objects.create(type=type)
        info_match.stats.type_of_organization.add(type_of_organization)


def _add_all_topics(info: Info, info_match: Ngo) -> None:
    for aoc in info.detail_info.soft_facts.areas_of_competence:
        aoc = aoc.strip()
        aoc = _fix_topic(aoc)
        try:
            existing_topics = NgoTopic.objects.get(topic=aoc)
            topic = existing_topics
        except:
            topic = NgoTopic.objects.create(topic=aoc)
        info_match.topics.add(topic)


def _add_all_branches(info: Info, info_match: Ngo) -> None:
    for country in info.detail_info.soft_facts.greographical_representation:
        country = country.strip().upper()

        country = _fix_country(country)

        if _invalid_country(country):
            continue
        try:
            existing_branches = NgoBranch.objects.get(country=country)
            branch = existing_branches
        except:
            branch = NgoBranch.objects.create(country=country)
        info_match.branches.add(branch)


def _fix_country(country):
    if 'AND YEMEN' in country:
        country = 'Yemen'.upper()
    if country == 'DANEMARK':
        country = 'Denmark'.upper()
    if country == 'DRC' or country == 'DR OF CONGO':
        country = 'DR Congo'.upper()
    if 'FRANCE & TERRITORIES' in country:
        country = 'France'.upper()
    if 'AND 96' in country:
        country = 'India'.upper()
    if country == 'INDIA IRELAND':
        country = 'India'.upper()
    if 'IRAQI' in country or country == 'IRAK':
        country = 'Iraq'.upper()
    if country == 'ISREAL' or country == 'JERUSALEM':
        country = 'Israel'.upper()
    if country == 'LAO P.D.R.' or country == 'LAO PDR':
        country = 'Lao'.upper()
    if 'MACEDONIA (' in country:
        country = 'Macedonia'.upper()
    if '(SOUTH AFRICA Q2' in country:
        country = 'Mexico'.upper()
    if country == 'NAIROBI':
        country = 'Kenya'.upper()
    if 'OCCUPIED' in country:
        country = 'Palestine'.upper()
    if country == 'RUSSIAN FEDERATION':
        country = 'Russia'.upper()
    if country == 'SLOVAK REPUBLIC':
        country = 'Slovakia'.upper()
    if '(INCL. SOMALILAND' in country or country == 'SOMALI REGION':
        country = 'Somalia'.upper()
    if country == 'TADJIKISTAN':
        country = 'Tajikistan'.upper()
    if 'OF MACEDONIA' in country:
        country = 'Macedonia'.upper()
    if 'TILL 2018' in country:
        country = 'Uganda'.upper()
    if 'UKRAINA' in country:
        country = 'Ukraine'.upper()
    if country == 'UNITED STATES' or country == 'US':
        country = 'USA'
    if country == 'US-IRAN':
        country = 'Iran'.upper()
    if country == 'WORLD':
        country = 'WORLDWIDE'
    if country == 'UK':
        country = 'UNITED KINGDOM'
    if country == 'THE PHILIPPINES':
        country = 'PHILIPPINES'
    if country == 'THE NETHERLANDS':
        country = 'NETHERLANDS'
    if country == 'ETHIPIA':
        country = 'ETHIOPIA'
    if 'IVOIRE' in country or 'IVORY' in country:
        country = 'IVORY COAST'
    return country


def run_initial_data_import() -> bool:
    print('TRYING TO IMPORT DATA')
    if database_not_empty():
        return False
    print('STARTING THE DATA IMPORT')
    european_council_info = parse_european_council()

    # do not use this method for other, secondary data sources
    convert_to_model_classes(european_council_info, 'European Council', True)

    print('DATA IMPORT (European Council) FINISHED')

    print('STARTING DATA IMPORT FROM NGOAdvisor ...')

    ngo_advisor_info = deserialize('findyourngo/data_import/ngo_advisor/ngoadvisor_pickled')

    match_count = 0
    skipped = 0
    already_imported_entries = len(european_council_info)
    for idx, info in enumerate(ngo_advisor_info):
        print(f'Current idx: {idx}')

        if info.main_info.name.type_of_organization is not None and ('social_enterprise' in info.main_info.name.type_of_organization or 'corporation' in info.main_info.name.type_of_organization \
            or 'academic_institution' in info.main_info.name.type_of_organization):
            print('Skipping because NGO type is weird')
            skipped += 1
            continue
        try:
            print(f'Trying to find NGO {info.main_info.name.name.upper()} in database ...')
            info_match = Ngo.objects.get(name=info.main_info.name.name.upper()) # Achtung Name noch nicht upper()
            print(f'Match in database found for {info.main_info.name.name}')
            _print_comparison(info_match, info)

            match_count += 1
            _update_with_ngo_advisor_info(info_match, info)
        except:
            print('No match found, creating new entry')
            convert_to_model_classes([info], 'NgoAdvisor', False, idx + already_imported_entries)

    print(f'Total number of matches: {match_count}')

    print('DATA IMPORT (NgoAdvisor) FINISHED')

    all_ngo_entries = Ngo.objects.all()

    print(f'All NGOS: {len(all_ngo_entries)}')
    print(f'EU NGOS: {len(european_council_info)}')
    print(f'NgoAdvisor NGOS: {len(ngo_advisor_info)}')
    print(f'Matches: {match_count}')
    print(f'Skipped: {skipped}')

    assert len(all_ngo_entries) == len(european_council_info) + len(ngo_advisor_info) - match_count - skipped

    return True


def database_not_empty() -> bool:
    return Ngo.objects.all()