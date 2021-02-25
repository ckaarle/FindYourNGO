from typing import List, Any, Optional

from findyourngo.data_import.InfoClasses import HardFacts, Info, SoftFacts, DetailPageInfo, MainPageInfo, \
    Representative, ContactInfo, Address, Name


def _extract_info(data: List[Any]) -> List[Info]:
    infos = []
    for idx, d in enumerate(data):
        main_info = _extract_main_info(idx, d)
        detail_info = _extract_detail_info(idx, d)

        infos.append(Info(main_info, detail_info))
    return infos


def _extract_main_info(idx: int, data: Any) -> MainPageInfo:
    nameEn = _clean(data['nameEn'])
    acronym = _clean(data['acronymEn'])

    if 'funding' in data:
        funding = _clean(data['funding'])
    else:
        funding = None

    name = Name(nameEn, acronym, funding)

    street = None
    postcode = None
    city = None
    country = None

    if 'street' in data:
        street = _clean(data['street'])
    if 'postcode' in data:
        postcode = _clean(data['postcode'])
    if 'town' in data:
        city = _clean(data['town'])
    if 'country' in data:
        country = _clean(data['country'])
    address = Address(street, postcode, city, country)

    phone = None
    if 'tel' in data:
        phone = _clean(data['tel'])

    email = None
    if 'email' in data:
        email = _clean(data['email'])
    contact = ContactInfo(phone, email)

    rep = _clean(data['officialRep'])

    rep_firstname = None
    if 'firstname' in rep:
        rep_firstname = _clean(rep['firstname'])

    rep_lastname= None
    if 'lastname' in rep:
        rep_lastname = _clean(rep['lastname'])

    rep_email = None
    if 'email' in rep:
        rep_email = _clean(rep['email'])
    representative = Representative(rep_lastname, rep_firstname, rep_email)

    return MainPageInfo(idx, name, address, contact, representative)


def _clean(word: str) -> Optional[str]:
    if 'undefined' in word:
        return None
    if 'n.a.' in word:
        return None
    if not word:
        return None
    if word == '-':
        return None
    if word == '--':
        return None

    return word


def _extract_detail_info(idx: int, data: Any) -> DetailPageInfo:
    last_updated = _clean(data['updatedAt'])

    hard_facts = _extract_hard_facts(data, idx)
    soft_facts = _extract_soft_facts(data)

    return DetailPageInfo(idx, last_updated, hard_facts, soft_facts)


def _extract_soft_facts(data: Any) -> SoftFacts:
    aims = None
    if 'aims' in data:
        aims = _clean(data['aims'])
        if not aims:
            aims = None

    activities = None
    if 'activities' in data:
        activities = _clean(data['activities'])
        if not activities:
            activities = None

    accreditations = None
    if 'accreditations' in data:
        accreditations = _clean(data['accreditations'])
        if not accreditations:
            accreditations = None

    areas_of_competence = None
    if 'aocs' in data:
        areas_of_competence = data['aocs']

        if isinstance(areas_of_competence, str):
            if not areas_of_competence:
                areas_of_competence = None
            else:
                areas_of_competence = areas_of_competence.split(',')

    geographical_representation = None
    if 'geoRep' in data:
        geographical_representation = data['geoRep']
        if isinstance(geographical_representation, str):
            if not geographical_representation:
                geographical_representation = None
            else:
                geographical_representation = geographical_representation.split(',')

    soft_facts = SoftFacts(aims, activities, accreditations, areas_of_competence, geographical_representation)
    return soft_facts


def _extract_hard_facts(data: Any, idx: int) -> HardFacts:
    website = None
    if 'website' in data:
        website = _clean(data['website'])

    pres_firstname = None
    if 'presidentFirstname' in data:
        pres_firstname = _clean(data['presidentFirstname'])

    pres_lastname = None
    if 'presidentLastname' in data:
        pres_lastname = _clean(data['presidentLastname'])

    if not 'yearFoundation' in data:
        founding_year = None
    else:
        founding_year_string = data['yearFoundation']
        if founding_year_string:
            try:
                founding_year = int(founding_year_string)
                if founding_year < 1700:
                    founding_year = None
            except ValueError:
                print(f'Found non integer founding year: {founding_year_string}')
                founding_year = None
        else:
            founding_year = None

    if not 'staff' in data:
        staff_number = None
    else:
        staff_string = _clean(data['staff'])
        try:
            staff_string = staff_string.replace(' ', '')
            staff_number = int(staff_string)
        except:
            if staff_string == '6fulltime+2interns':
                staff_number = 6
            elif staff_string == '2.8':
                staff_number = 3
            elif staff_string == '3employeesand7volunteers':
                staff_number = 3
            elif staff_string == '5employees':
                staff_number = 5
            else:
                staff_number = None

    if not 'nbMembers' in data:
        members_number = None
    else:
        members_string = _clean(data['nbMembers'])

        try:
            members_string = members_string.replace(' ', '')
            members_string = members_string.replace('+', '')
            members_number = int(members_string)
        except:
            if members_string == '384organisations':
                members_number = 384
            elif members_string == '50delegations':
                members_number = 50
            elif members_string == '120,000':
                members_number = 120000
            elif members_string == 'Around35':
                members_number = 35
            elif members_string == 'about5000':
                members_number = 5000
            elif members_string == '46nationaluniversitysportsgoverningbodies':
                members_number = 46
            elif members_string == 'around1000membersin34branches':
                members_number = 1000
            elif members_string == '44associations':
                members_number = 44
            elif members_string == 'approx.700':
                members_number = 700
            elif members_string == '5,000,000':
                members_number = 5000000
            elif members_string == '250associations':
                members_number = 250
            elif members_string == '28memberorganisations':
                members_number = 28
            else:
                members_number = None

    if not 'workLang' in data:
        working_languages = None
    else:
        working_languages = _clean(data['workLang'])

    hard_facts = HardFacts(website, pres_firstname, pres_lastname, founding_year, staff_number, members_number,
                           working_languages)
    return hard_facts


def _clean_info(infos: List[Info]) -> None:
    for info in infos:
        if info.main_info.address.city is not None and 'Legal Seat' in info.main_info.address.city:
            info.main_info.address.city = 'Düsseldorf'
        if info.main_info.address.street is not None and 'BP 2541' in info.main_info.address.street:
            info.main_info.address.city = 'Lyon'
        if info.main_info.address.street is not None and 'Holds status' in info.main_info.address.street:
            info.main_info.address.street = None
        if info.main_info.address.street is not None and 'Council of Europe' in info.main_info.address.street:
            info.main_info.address.street = None