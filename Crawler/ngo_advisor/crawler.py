import time
from typing import List, Tuple, Dict, Any

from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from european_council.parser.MainPageInfo import MainPageInfo, DetailPageInfo
from ngo_advisor.parser_functions.functions import parse_organization_name, parse_website_url, \
    parse_type_of_organization, parse_year_founded, parse_hq_location, parse_hq_mailing_address, \
    parse_sectors_of_activity, parse_countries_where_active, parse_primary_contact, parse_representative, \
    parse_membership_based, parse_total_members, parse_accreditation, parse_yearly_income, parse_surplus_deficit, \
    parse_legal_status

ORGANIZATION_NAME = 'ORGANIZATION NAME'
WEBSITE_URL = 'ENGLISH-LANGUAGE WEBSITE URL'
TYPE_OF_ORGANIZATION = 'TYPE OF ORGANIZATION'
YEAR_FOUNDED = 'YEAR FOUNDED'
HQ_LOCATION_CITY_COUNTRY = 'HQ LOCATION: CITY, COUNTRY'
HQ_MAILING_ADDRESS = 'HQ MAILING ADDRESS'
SECTORS_OF_ACTIVITY = 'SECTORS OF ACTIVITY'
COUNTRIES_WHERE_ACTIVE = 'COUNTRY (OR COUNTRIES) WHERE ACTIVE'
PRIMARY_CONTACT = 'PRIMARY CONTACT AND GENERAL INQUIRIES'
REPRESENTATIVE = 'NAME OF OFFICIAL REPRESENTATIVE FOR PROFILE'
MEMBERSHIP_BASED = 'IS YOUR ORGANISATION MEMBERSHIP-BASED ?'
TOTAL_MEMBERS = 'TOTAL MEMBERS'
ACCREDITATION = 'IS YOUR ORGANIZATION ACCREDITED TO ECOSOC (UN)?'
LATEST_YEARLY_INCOME = 'LATEST YEARLY INCOME (ALL COUNTRIES AND ENTITIES)'
LATEST_SURPLUS_DEFICIT = 'LATEST SURPLUS/DEFICIT'
LEGAL_STATUS = 'LEGAL STATUS'

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
    HQ_MAILING_ADDRESS: parse_hq_mailing_address,
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
}


def crawl() -> List[Tuple[MainPageInfo, DetailPageInfo]]:
    driver = _get_driver()
    driver.get(URL)

    detail_links = _get_detail_links(driver)

    infos = []
    counter = 0
    for link in detail_links:
        print(f'Crawling {link} ({counter})')
        main_info, detail_info = _crawl(link, driver)
        infos.append((main_info, detail_info))

        counter += 1

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


def _crawl(detail_link: str, driver: WebDriver) -> Tuple[MainPageInfo, DetailPageInfo]:
    driver.get(detail_link)
    time.sleep(10)

    accordeon = driver.find_elements_by_class_name('accordeon')

    fields = _get_all_present_fields(accordeon)
    info = _set_existing_field_values(fields)

    # main_info, detail_info = _convert(info) TODO
    main_info = None
    detail_info = None
    return main_info, detail_info


def _get_all_present_fields(accordeon) -> List[WebElement]:
    content_list = []
    for a in accordeon:
        c = a.find_element_by_class_name('content')
        content_list.append(c)
    all_fields = []
    for c in content_list:
        fields = c.find_elements_by_class_name('field')
        all_fields += fields

    return all_fields


def _set_existing_field_values(fields: List[WebElement]) -> Dict[str, Any]:
    infos = {}
    for field in fields:
        header = field.find_element_by_tag_name('span').text.strip()

        if not header:
            continue

        print(f'Parsing field {header}')

        if header not in possible_fields:
            print(f'--------------- New header found: {header} - skipping')
            continue

        info = function_for_header[header](field)
        infos[header] = info


def _convert(infos: Dict[str, Any]) -> Tuple[MainPageInfo, DetailPageInfo]:
    pass # TODO


if __name__ == '__main__':
    crawl()