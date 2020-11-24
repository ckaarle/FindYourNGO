from typing import Any, List, Tuple

from selenium.webdriver.remote.webelement import WebElement


City = str
Country = str


def parse_organization_name(field: WebElement) -> str:
    div = field.find_element_by_tag_name('div')
    name = div.text.strip()
    return name


def parse_website_url(field: WebElement) -> str:
    div = field.find_element_by_tag_name('div')
    website = div.text.strip()
    return website


def parse_type_of_organization(field: WebElement) -> List[str]:
    div = field.find_element_by_tag_name('div')
    types = div.text.strip()

    all_types = types.split(',')
    all_types = _remove_trailing_comma_element(all_types)
    all_types = _strip(all_types)

    return all_types


def _remove_trailing_comma_element(str_list: List[str]) -> List[str]:
    if not str_list[-1]:
        str_list = str_list[:-1]
    return str_list


def _strip(str_list: List[str]) -> List[str]:
    return [s.strip() for s in str_list]


def parse_year_founded(field: WebElement) -> int:
    div = field.find_element_by_tag_name('div')
    year = int(div.text.strip())
    return year


def parse_hq_location(field: WebElement) -> Tuple[City, Country]:
    try:
        div = field.find_element_by_tag_name('div')
        location = div.text.strip()

        city_country = location.split('|')
        city_country = _strip(city_country)

        return city_country[0], city_country[1]
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


def parse_hq_mailing_address(field: WebElement) -> Any: # street | city postcode | country OR ... | country    OR Strasse <br> P.O. Box <br> post code <br> country
    print(f'++++++++++++ unparsed: {field.text}')
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
    pass # TODO


def parse_sectors_of_activity(field: WebElement) -> List[str]:
    div = field.find_element_by_tag_name('div')
    sectors = div.text.strip()

    all_sectors = sectors.split(',')
    all_sectors = _remove_trailing_comma_element(all_sectors)
    all_sectors = _strip(all_sectors)

    return all_sectors


def parse_countries_where_active(field: WebElement) -> List[str]:
    div = field.find_element_by_tag_name('div')
    countries = div.text.strip()

    all_countries = countries.split(',')
    all_countries = _remove_trailing_comma_element(all_countries)
    all_countries = _strip(all_countries)

    return all_countries


def parse_primary_contact(field: WebElement) -> Any: # email <br> phone number - auch umgekehrt, tlw. auch erst Name und Email
    print(f'++++++++++++ unparsed: {field.text}')
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
    pass # TODO


def parse_representative(field: WebElement) -> Any: # Titel Firstname Lastname <br> job title <br> email <br> phone number
    print(f'++++++++++++ unparsed: {field.text}')
    # """
    # Ms Silvia Icardi
    # Information and Communication Manager
    # silvia.icardi@acted.org
    # Tel + 33 (0)1 42 65 61 40
    # """
    pass # TODO


def parse_membership_based(field: WebElement) -> bool:
    div = field.find_element_by_tag_name('div')
    membership_based = div.text.strip()

    return membership_based.lower() == 'yes'


def parse_total_members(field: WebElement) -> int:
    div = field.find_element_by_tag_name('div')
    members = int(div.text.strip())
    return members


def parse_accreditation(field: WebElement) -> bool:
    div = field.find_element_by_tag_name('div')
    accreditation = div.text.strip()

    return accreditation.lower() == 'yes'


def parse_yearly_income(field: WebElement) -> Any: # EUR XXX, $XXX
    print(f'++++++++++++ unparsed: {field.text}')
    pass # TODO


def parse_surplus_deficit(field: WebElement) -> Any: # EUR +xxx
    print(f'++++++++++++ unparsed: {field.text}')
    pass # TODO


def parse_legal_status(field: WebElement) -> str:
    div = field.find_element_by_tag_name('div')
    status = div.text.strip()
    return status
