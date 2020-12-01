import pickle
import time
from typing import List, Tuple, Dict, Any, Optional

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from findyourngo.data_import.InfoClasses import MainPageInfo, DetailPageInfo, HardFacts, SoftFacts, Representative, \
    ContactInfo, Address, Name, Info
from findyourngo.data_import.ngo_advisor.parser_functions.functions import parse_organization_name, parse_website_url, \
    parse_type_of_organization, parse_year_founded, parse_hq_location, parse_hq_country, \
    parse_sectors_of_activity, parse_countries_where_active, parse_primary_contact, parse_representative, \
    parse_membership_based, parse_total_members, parse_accreditation, parse_yearly_income, parse_surplus_deficit, \
    parse_legal_status, parse_mission

ORGANIZATION_NAME = 'ORGANIZATION NAME'
TYPE_OF_ORGANIZATION = 'TYPE OF ORGANIZATION'
LATEST_YEARLY_INCOME = 'LATEST YEARLY INCOME (ALL COUNTRIES AND ENTITIES)'
HQ_LOCATION_CITY_COUNTRY = 'HQ LOCATION: CITY, COUNTRY'
HQ_MAILING_ADDRESS = 'HQ MAILING ADDRESS'
PRIMARY_CONTACT = 'PRIMARY CONTACT AND GENERAL INQUIRIES'
REPRESENTATIVE = 'NAME OF OFFICIAL REPRESENTATIVE FOR PROFILE'
WEBSITE_URL = 'ENGLISH-LANGUAGE WEBSITE URL'
YEAR_FOUNDED = 'YEAR FOUNDED'
TOTAL_MEMBERS = 'TOTAL MEMBERS'
MISSION = 'MISSION'
ACCREDITATION = 'IS YOUR ORGANIZATION ACCREDITED TO ECOSOC (UN)?'
SECTORS_OF_ACTIVITY = 'SECTORS OF ACTIVITY'
COUNTRIES_WHERE_ACTIVE = 'COUNTRY (OR COUNTRIES) WHERE ACTIVE'
MEMBERSHIP_BASED = 'IS YOUR ORGANISATION MEMBERSHIP-BASED ?'

LEGAL_STATUS = 'LEGAL STATUS'
LATEST_SURPLUS_DEFICIT = 'LATEST SURPLUS/DEFICIT'

URL = 'https://www.ngoadvisor.net/ong'


possible_fields = [
    ORGANIZATION_NAME,
    WEBSITE_URL,
    TYPE_OF_ORGANIZATION,
    YEAR_FOUNDED,
    HQ_LOCATION_CITY_COUNTRY,
    HQ_MAILING_ADDRESS,
    SECTORS_OF_ACTIVITY,
    COUNTRIES_WHERE_ACTIVE,
    PRIMARY_CONTACT,
    REPRESENTATIVE,
    MEMBERSHIP_BASED,
    TOTAL_MEMBERS,
    ACCREDITATION,
    LATEST_YEARLY_INCOME,
    LATEST_SURPLUS_DEFICIT,
    LEGAL_STATUS,
]

function_for_header = {
    ORGANIZATION_NAME: parse_organization_name,
    WEBSITE_URL: parse_website_url,
    TYPE_OF_ORGANIZATION: parse_type_of_organization,
    YEAR_FOUNDED: parse_year_founded,
    HQ_LOCATION_CITY_COUNTRY: parse_hq_location,
    HQ_MAILING_ADDRESS: parse_hq_country,
    SECTORS_OF_ACTIVITY: parse_sectors_of_activity,
    COUNTRIES_WHERE_ACTIVE: parse_countries_where_active,
    PRIMARY_CONTACT: parse_primary_contact,
    REPRESENTATIVE: parse_representative,
    MEMBERSHIP_BASED: parse_membership_based,
    TOTAL_MEMBERS: parse_total_members,
    ACCREDITATION: parse_accreditation,
    LATEST_YEARLY_INCOME: parse_yearly_income,
    LATEST_SURPLUS_DEFICIT: parse_surplus_deficit,
    LEGAL_STATUS: parse_legal_status,
    MISSION: parse_mission,
}


def crawl_ngo_advisor() -> List[Info]:
    driver = _get_driver()
    driver.get(URL)

    detail_links = _get_detail_links(driver)

    infos = []
    counter = 0
    impossible_to_crawl_links = []

    for link in detail_links:
        print(f'Crawling {link} ({counter})')

        try:
            converted_infos = _crawl(link, driver)
            infos.append(converted_infos)
        except ElementClickInterceptedException:
            print(f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX IMPOSSIBLE TO CRAWL: {link}')
            impossible_to_crawl_links.append(link)

        counter += 1
        print(f'So far, {len(impossible_to_crawl_links)} website(s) could not be crawled:')
        print(f'{impossible_to_crawl_links}')
        print('----------------------------------------------------------------')

    return infos


def _get_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/Users/Chris/Downloads/chromedriver", chrome_options=options)
    return driver


def _get_detail_links(driver: WebDriver) -> List[str]:
    time.sleep(10) # website is very slow
    detail_links = []

    ngo_list = driver.find_element_by_id('toplist')
    links = ngo_list.find_elements_by_tag_name('a')

    for link in links:
        link_href = link.get_attribute("href")
        detail_links.append(link_href)

    return detail_links


def _crawl(detail_link: str, driver: WebDriver) -> Info:
    driver.get(detail_link)
    time.sleep(5)

    accordeon = driver.find_elements_by_class_name('accordeon')

    try:
        driver.find_element_by_class_name('moove-gdpr-infobar-allow-all').click() # get rid of cookie banner blocking all clicks on this website
    except:
        pass

    info = _get_all_present_fields(accordeon, driver)

    return _convert(info)


def _get_all_present_fields(accordeon: List[WebElement], driver: WebDriver) -> Dict[str, Any]:
    infos = {}
    for a in accordeon:
        if 'Opinion & Ratings' in a.text: # accordeon that only some pages have, containing a rating by NGO Advisor
            continue
        if 'General' not in a.text: # 'general' accordeon is already open
            b = a.find_element_by_class_name('barre')
            b.click() # open the accordeon (otherwise data will not be loaded)

        c = a.find_element_by_class_name('content')
        fields = c.find_elements_by_class_name('field')

        new_infos = _set_existing_field_values(fields)
        infos.update(new_infos)

        b = a.find_element_by_class_name('barre')
        b.click()  # close the accordeon

    return infos


def _set_existing_field_values(fields: List[WebElement]) -> Dict[str, Any]:
    infos = {}
    for field in fields:
        try:
            header = field.find_element_by_tag_name('span').text.strip()

            if not header:
                continue

            if header not in possible_fields:
                print(f'--------------- New header found: {header} - skipping')
                continue

            info = function_for_header[header](field)
            infos[header] = info
        except:
            continue

    return infos


def fill_string(header: str, infos: Dict[str, Any]) -> Optional[str]:
    if header in infos.keys():
        return infos[header]

    return None


def fill_int(header: str, infos: Dict[str, Any]) -> Optional[int]:
    try:
        return infos[header]
    except:
        return None


def _convert(infos: Dict[str, Any]) -> Info:
    n = infos[ORGANIZATION_NAME]
    acronym = '' # NGOAdvisor does not list acronyms
    funding = None
    type_of_organization = infos[TYPE_OF_ORGANIZATION]
    yearly_income = fill_string(LATEST_YEARLY_INCOME, infos)
    name = Name(n, acronym, funding, type_of_organization, yearly_income)

    street = None
    postcode = None
    city, co = None, None
    if HQ_LOCATION_CITY_COUNTRY in infos.keys():
        city, co = infos[HQ_LOCATION_CITY_COUNTRY]

    if co is None or not co:
        country = fill_string(HQ_MAILING_ADDRESS, infos)
    else:
        country = co
    address = Address(street, postcode, city, country)

    email, phone = None, None
    if PRIMARY_CONTACT in infos.keys():
        email, phone = infos[PRIMARY_CONTACT]
    contact = ContactInfo(phone, email)

    rep_first_name = None
    rep_last_name = None
    rep_email = fill_string(REPRESENTATIVE, infos)
    rep = Representative(rep_last_name, rep_first_name, rep_email)

    website = fill_string(WEBSITE_URL, infos)
    pres_first = None
    pres_last = None
    founding_year = fill_int(YEAR_FOUNDED, infos)
    staff = None
    members = fill_int(TOTAL_MEMBERS, infos)
    languages = None
    hard_facts = HardFacts(website, pres_first, pres_last, founding_year, staff, members, languages)

    aims = fill_string(MISSION, infos)
    activities = None

    accreditations = None
    if ACCREDITATION in infos.keys():
        if infos[ACCREDITATION]:
            accreditations = 'ECOSOC' # only this one accreditation was listed

    aocs = None
    if SECTORS_OF_ACTIVITY in infos.keys():
        aocs = infos[SECTORS_OF_ACTIVITY]

    geographical_rep = None
    if COUNTRIES_WHERE_ACTIVE in infos.keys():
        geographical_rep = infos[COUNTRIES_WHERE_ACTIVE]

    soft_facts = SoftFacts(aims, activities, accreditations, aocs, geographical_rep)

    last_updated = ''

    main_info = MainPageInfo(-1, name, address, contact, rep)
    detail_info = DetailPageInfo(-1, last_updated, hard_facts, soft_facts)

    info = Info(main_info, detail_info)

    print_info(info)

    return info


def print_info(info: Info) -> None:
    print(f'Info for {info.main_info.name.name}')
    print(f'Funding: {info.main_info.name.funding}, type: {info.main_info.name.type_of_organization}, income: {info.main_info.name.yearly_income}')
    print(f'City: {info.main_info.address.city}, country: {info.main_info.address.country}')
    print(f'Phone: {info.main_info.contact.phone_number}, email: {info.main_info.contact.email}')
    print(f'Rep email: {info.main_info.representative.representative_email}')
    print(f'Website: {info.detail_info.hard_facts.website}, founding year: {info.detail_info.hard_facts.founding_year}, members: {info.detail_info.hard_facts.members}')
    print(f'Aims: {info.detail_info.soft_facts.aims}')
    print(f'Aocs: {info.detail_info.soft_facts.areas_of_competence}')
    print(f'Accreditation: {info.detail_info.soft_facts.accreditations}')
    print(f'Geo. Rep: {info.detail_info.soft_facts.greographical_representation}')
    print('----------------------------------------------------------------')


def _serialize(infos: List[Info], filename: str) -> None:
    with open(filename, 'ab+') as f:
        for info in infos:
            pickle.dump(info, f)


def deserialize(filename: str) -> List[Info]:
    infos = []
    with open(filename, 'rb') as f:
        try:
            while True:
                infos.append(pickle.load(f))
        except EOFError:
            pass

    return infos


if __name__ == '__main__':
    infos = crawl_ngo_advisor()

    filename = 'ngoadvisor_pickled'
    _serialize(infos, filename)

    # serializing test
    infos_deserialized = deserialize(filename)

    assert len(infos) == len(infos_deserialized)
