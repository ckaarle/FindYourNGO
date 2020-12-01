from typing import List, Tuple, Optional

from selenium.webdriver.remote.webelement import WebElement


City = str
Country = str
Email = str
PhoneNumber = str


def parse_organization_name(field: WebElement) -> str:
    div = field.find_element_by_tag_name('div')
    name = div.text.strip()
    return name


def parse_website_url(field: WebElement) -> str:
    try:
        div = field.find_element_by_tag_name('div')
        website = div.text.strip()
        return website
    except:
        return None


def parse_type_of_organization(field: WebElement) -> List[str]:
    try:
        div = field.find_element_by_tag_name('div')
        types = div.text.strip()

        all_types = types.split(',')
        all_types = _remove_trailing_comma_element(all_types)
        all_types = _strip(all_types)

        result = []
        for type in all_types:
            if 'social_enterprise' in type:
                pass
            else:
                result.append(type)

        return result
    except:
        return []


def _remove_trailing_comma_element(str_list: List[str]) -> List[str]:
    if not str_list[-1]:
        str_list = str_list[:-1]
    return str_list


def _strip(str_list: List[str]) -> List[str]:
    return [s.strip() for s in str_list]


def parse_year_founded(field: WebElement) -> int:
    try:
        div = field.find_element_by_tag_name('div')
        year = int(div.text.strip())
        return year
    except:
        return None


def parse_hq_location(field: WebElement) -> Tuple[City, Country]:
    try:
        div = field.find_element_by_tag_name('div')
        location = div.text.strip()

        city_country = location.split('|')
        city_country = _strip(city_country)
        city = city_country[0]

        if ',' in city:
            city = city.split(',')[0].strip() # avoiding Cambridge, MA and the like

        return city, city_country[1]
    except:
        pass


    try:
        div = field.find_element_by_tag_name('div')
        location = div.text.strip()

        address_country = location.split('÷')
        address_country = _strip(address_country)

        city = address_country[0].split(',')[0].strip()
        return city, address_country[1]
    except:
        pass

    print(f'--------------- HQ Location could not be parsed')
    return '', ''


def parse_hq_country(field: WebElement) -> Optional[str]:
    div = field.find_element_by_tag_name('div')
    address = div.text.strip()
    # 40 Worth Street, Suite 303 New York, NY, 10013, USA

    # 158 Jan Smuts Avenue Building, Rosebank, Johannesburg | South Africa

    # 14/16 Boulevard Douaumont | CS 80060 75854 PARIS CEDEX 17 | France

    # """
    # ACTED
    # 33 rue Godot de Mauroy
    # 75009 Paris
    # France
    # """

    # Locked Bag Q199,  Queen Victoria Building NSW 123 | Australia

    # Avenida Reforma 12-01 zona 10. Edificio Reforma Montúfar, Nivel 17, oficina 17-01 Ciudad de Guatemala | Guatemara

    # 10 Fawcett St, Suite 204 | Cambridge, MA 02138 | USA

    # 1904 Harbor Boulevard #831, Costa Mesa, CA 92627 ÷ USA
    country = None
    try:
        parts = address.split('|')
        country = parts[-1].strip()
    except:
        try:
            parts = address.split('\n')
            country = parts[-1].strip()
        except:
            try:
                parts = address.split(',')
                country = parts[-1].strip()
            except:
                try:
                    parts = address.split('÷')
                    country = parts[-1].strip()
                except:
                    pass
    return country


def parse_sectors_of_activity(field: WebElement) -> List[str]:
    try:
        div = field.find_element_by_tag_name('div')
        sectors = div.text.strip()

        all_sectors = sectors.split(',')
        all_sectors = _remove_trailing_comma_element(all_sectors)
        all_sectors = _strip(all_sectors)

        return all_sectors
    except:
        return []


def parse_countries_where_active(field: WebElement) -> List[str]:
    try:
        div = field.find_element_by_tag_name('div')
        countries = div.text.strip()

        all_countries = countries.split(',')
        all_countries = _remove_trailing_comma_element(all_countries)
        all_countries = _strip(all_countries)

        return all_countries
    except:
        return []


def parse_primary_contact(field: WebElement) -> Tuple[Email, PhoneNumber]:
    try:
        div = field.find_element_by_tag_name('div')
        contact = div.text.strip()

        email = None
        phone_number = None

        contact_parts = contact.split('\n')

        for part in contact_parts:
            if '@' in part:
                email = part.strip()
            elif 'Tel' in part or '+':
                phone_number = part.strip()
    except:
        pass
    # info@actionfromswitzerland.ch

    # """
    # Ms Silvia Icardi
    # Information and Communication Manager
    # silvia.icardi@acted.org
    # Tel + 33 (0)1 42 65 61 40
    # """

    # """
    # info@actforpeace.org.au
    # +612 9299 2215
    # """

    # +1 (949) 202-4681
    return email, phone_number


def parse_representative(field: WebElement) -> Email: # Titel Firstname Lastname <br> job title <br> email <br> phone number
    try:
        div = field.find_element_by_tag_name('div')
        rep = div.text.strip()

        email = None
        rep_parts = rep.split('\n')

        for part in rep_parts:
            if '@' in part:
                email = part.strip()
                return email
    except:
        pass
    # """
    # Ms Silvia Icardi
    # Information and Communication Manager
    # silvia.icardi@acted.org
    # Tel + 33 (0)1 42 65 61 40
    # """
    return email


def parse_membership_based(field: WebElement) -> bool:
    try:
        div = field.find_element_by_tag_name('div')
        membership_based = div.text.strip()

        return membership_based.lower() == 'yes'
    except:
        return False


def parse_total_members(field: WebElement) -> int:
    try:
        div = field.find_element_by_tag_name('div')
        members = int(div.text.strip())
        return members
    except:
        return None


def parse_accreditation(field: WebElement) -> bool:
    try:
        div = field.find_element_by_tag_name('div')
        accreditation = div.text.strip()

        return accreditation.lower() == 'yes'
    except:
        return False


def parse_yearly_income(field: WebElement) -> str: # EUR XXX, $XXX
    try:
        div = field.find_element_by_tag_name('div')
        income = div.text.strip()
        return income
    except:
        return None


def parse_surplus_deficit(field: WebElement) -> str: # EUR +xxx
    try:
        div = field.find_element_by_tag_name('div')
        surplus_deficit = div.text.strip()
        return surplus_deficit
    except:
        return None


def parse_legal_status(field: WebElement) -> str:
    try:
        div = field.find_element_by_tag_name('div')
        status = div.text.strip()
        return status
    except:
        return None


def parse_mission(field: WebElement) -> str:
    try:
        div = field.find_element_by_tag_name('div')
        mission = div.text.strip()
        return mission
    except:
        return None