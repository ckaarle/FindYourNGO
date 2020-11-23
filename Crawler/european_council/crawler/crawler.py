import time
from typing import List, Tuple, Optional

from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from european_council.crawler.MainPageInfo import Name, Address, ContactInfo, Representative, MainPageInfo, DetailPageInfo, \
    HardFacts, SoftFacts

URL = 'http://coe-ngo.org/#/ingos'


def crawl() -> Tuple[MainPageInfo, DetailPageInfo]:
    driver = _get_driver()
    driver.get(URL)

    main_page_info = _crawl_main_page(driver)
    detail_page_infos = _crawl_detail_page(driver)

    return main_page_info, detail_page_infos


def _get_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/Users/Chris/Downloads/chromedriver", chrome_options=options)
    return driver


def _crawl_main_page(driver) -> List[MainPageInfo]:
    rows: List[WebElement] = _get_table_rows(driver)

    extracted_information = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        cols = filter_empty_cols(cols)

        main_page_info = extract_information(cols)
        extracted_information.append(main_page_info)

    run_sanity_checks(extracted_information)

    extracted_information = clean_up(extracted_information)
    return extracted_information


def _get_table_rows(driver: WebDriver) -> List[WebElement]:
    time.sleep(1) # if we don't wait here, the table might not be loaded yet
    table = driver.find_element_by_tag_name('table')
    body = table.find_element_by_tag_name('tbody')
    rows = body.find_elements_by_tag_name('tr')
    return rows


def filter_empty_cols(cols: List[WebElement]) -> List[WebElement]:
    return cols[:-1] # last column is empty


def extract_information(cols: List[WebElement]) -> MainPageInfo:
    idx: int = extract_idx(cols[0])
    name: Name = extract_name(cols[0])
    # cols[1] is name in French
    address: Address = extract_address(cols[2])
    contact: ContactInfo = extract_contact_information(cols[3])
    representative: Representative = extract_representative(cols[4])

    return MainPageInfo(idx, name, address, contact, representative)


def extract_idx(col: WebElement) -> int:
    return int(col.find_element_by_tag_name('span').text.strip())


def extract_name(col: WebElement) -> Name:
    link_element = col.find_element_by_tag_name('a')
    name = link_element.text.strip()
    acronym = extract_acronym(col.text.strip())
    return Name(name, acronym)


def extract_acronym(text: str) -> str:
    idx_opening_bracket = text.rfind('(')
    idx_closing_bracket = text.rfind(')')

    return text[idx_opening_bracket + 1 : idx_closing_bracket].strip()


def extract_address(col: WebElement) -> Address:
    full_address = col.text

    country_split_index = full_address.rfind(',')
    country = full_address[country_split_index + 1:].strip()

    street_city = full_address[:country_split_index]

    city_split_index = street_city.rfind(' ')
    city = ''
    street = ''
    try:
        city = street_city[city_split_index + 1:].strip()
        street = street_city[:city_split_index].strip()
    except:
        pass

    return Address(street, city, country, full_address)


def extract_contact_information(col: WebElement) -> ContactInfo:
    full_info = col.text
    email = col.find_element_by_tag_name('span').text.strip()

    phone_number = ''
    try:
        index_after_phone_number = full_info.index('\n')
        phone_number = full_info[:index_after_phone_number].strip()
    except:
        pass

    return ContactInfo(phone_number, email, full_info)


def extract_representative(col: WebElement) -> Representative:
    full_info = col.text

    email = col.find_element_by_tag_name('span').text.strip()

    name = ''
    try:
        index_after_name = full_info.index('\n')
        name = full_info[:index_after_name].strip()
    except:
        pass

    return Representative(name, email, full_info)


def run_sanity_checks(infos: List[MainPageInfo]) -> None:
    assert infos[0].idx == 1

    for idx, info in enumerate(infos):
        if idx == 0:
            continue

        assert info.idx == infos[idx - 1].idx + 1

    assert infos[-1].idx == 314


def clean_up(infos: List[MainPageInfo]) -> List[MainPageInfo]:
    for info in infos:
        if info.idx == 8:
            info.address.detail_address = ''
            info.address.city = 'Düsseldorf'
        if info.idx == 13:
            info.address.detail_address = 'BP 2541 F - 69218'
            info.address.city = 'Lyon'
        if info.idx == 14:
            info.address.detail_address = ''
        if info.idx == 33:
            info.address.detail_address = 'MEA House, Ellison Place NE1 8XS'
            info.address.city = 'Newcastle Upon Tyne'
        if info.idx == 39:
            info.address.detail_address = '65, rue du taureau 1025'
            info.address.city = 'Bormla'
        if info.idx == 40:
            info.contact.phone_number = ''
        if info.idx == 45:
            info.contact.phone_number = ''
        if info.idx == 60:
            info.address.detail_address = 'Riouwstraat 139 2585 HP'
            info.address.city = 'The Hague'
        if info.idx == 63:
            info.name.acronym = ''
        if info.idx == 64:
            info.address.detail_address = 'Lange Voorhout 35 2514 EC'
            info.address.city = 'The Hague'
        if info.idx == 77:
            info.contact.phone_number = '00 33 1 48 05 67 58'
        if info.idx == 81:
            info.address.detail_address = '11 rue du Verdon 67024'
            info.address.city = 'Strasbourg'
        if info.idx == 88:
            info.address.detail_address = '39 route de Montesson 78110'
            info.address.city = 'LE VESINET'
        if info.idx == 101:
            info.address.detail_address = 'Lützowplatz 9'
        if info.idx == 110:
            info.contact.phone_number = '+33 1 40 64 49 00'
        if info.idx == 111:
            info.contact.phone_number = ''
        if info.idx == 112:
            info.contact.phone_number = ''
        if info.idx == 116:
            info.contact.phone_number = ''
        if info.idx == 117:
            info.address.detail_address = 'B.P. 80007 67015'
            info.address.city = 'Strasbourg'
        if info.idx == 122:
            info.address.detail_address = '105 avenue Gambetta 75960'
            info.address.city = 'Paris'
        if info.idx == 135:
            info.contact.phone_number = ''
        if info.idx == 136:
            info.contact.phone_number = ''
        if info.idx == 152:
            info.contact.phone_number = '0032 2 647 72 79'
        if info.idx == 171:
            info.address.detail_address = '1 Station A M5W 1A2'
            info.address.city = 'Toronto, Ontario'
        if info.idx == 174:
            info.address.detail_address = '350 Fifth Avenue, 34th floor NY 10118-3'
            info.address.city = 'New York'
        if info.idx == 181:
            info.address.detail_address = '7 rue des Magnolias 17800'
            info.address.city = 'LaCroix St. Léger'
        if info.idx == 183:
            info.address.city = 'Kiev'
        if info.idx == 191:
            info.address.detail_address = 'Brolaeggerstraede 9 1211'
            info.address.city = 'Copenhagen'
        if info.idx == 196:
            info.address.detail_address = '1 rue de Varembé PO Box 96 CH 1211'
            info.address.city = 'Geneva'
        if info.idx == 202:
            info.address.detail_address = '14 Eversley Park Road, Winchmore Hill N21 IJU'
            info.address.city = 'London'
        if info.idx == 204:
            info.address.detail_address = 'C/O MOVISIE at Catharijnesingel 47 3501DC'
            info.address.city = 'Utrecht'
        if info.idx == 208:
            info.address.detail_address = 'Bryghuspladsen 8, Entrance C, 3rd floor 1473'
            info.address.city = 'Copenhagen'
            info.contact.email = 'info@ifhp.org'
        if info.idx == 217:
            info.address.detail_address = '21, rue d\'Assas 75270'
            info.address.city = 'Paris'
        if info.idx == 234:
            info.contact.phone_number = ''
        if info.idx == 237:
            info.address.detail_address = ''
        if info.idx == 242:
            info.address.detail_address = 'P.O Box 983 2501 CZ'
            info.address.city = 'The Hague'
        if info.idx == 252:
            info.address.detail_address = '300 W 22nd Street 60523-8842'
            info.address.city = 'Oak Brook'
        if info.idx == 253:
            info.contact.phone_number = ''
            info.representative.representative_email = 'info@mfhr.gr'
        if info.idx == 266:
            info.address.detail_address = '866 United Nations Plaza/Office 422 NY10017'
            info.address.city = 'New York'
        if info.idx == 267:
            info.address.detail_address = 'Pastoor de Kroonstaat 349 5211'
            info.address.city = 'XJ Den Bosch'
            info.contact.phone_number = ''
        if info.idx == 269:
            info.address.detail_address = 'Transvaal, 13 1865 AK'
            info.address.city = 'Bergen aan Zee'
        if info.idx == 278:
            info.address.detail_address = '1133 19th Street NW 20036'
            info.address.city = 'Washington DC'
        if info.idx == 282:
            info.address.detail_address = ''
        if info.idx == 291:
            info.name.acronym = ''
            info.representative.representative_name = ''
        if info.idx == 295:
            info.address.detail_address = ''
        if info.idx == 300:
            info.representative.representative_name = ''
        if info.idx == 303:
            info.contact.phone_number = ''
        if info.idx == 305:
            info.contact.phone_number = '+32 2 893 24 35'
        if info.idx == 313:
            info.address.detail_address = '1200 Harger Road, Suite 330 IL 60523'
            info.address.city = 'Oak Brook'

    return infos


def _crawl_detail_page(driver: WebDriver) -> List[DetailPageInfo]:
    detail_pages_infos = []

    for idx in range(1, 315):
        driver.get(URL)

        rows: List[WebElement] = _get_table_rows(driver)
        for row in rows:
            cols = row.find_elements_by_tag_name('td')

            row_idx: int = extract_idx(cols[0])
            if row_idx == idx:
                link_element = cols[0].find_element_by_tag_name('a')
                link_element.click()

                detail_page_info = _extract_detail_info(driver, idx)
                detail_pages_infos.append(detail_page_info)
                break

    _clean_detail_pages(detail_pages_infos)
    return detail_pages_infos


def _extract_detail_info(driver: WebDriver, idx: int) -> DetailPageInfo:
    hard_facts = _extract_hard_facts(driver, idx)
    soft_facts = _extract_soft_facts(driver)

    return DetailPageInfo(idx, hard_facts, soft_facts)


def _extract_hard_facts(driver: WebDriver, idx: int) -> HardFacts:
    hard_fact_element = driver.find_elements_by_tag_name('div')[12]

    website = hard_fact_element.find_elements_by_tag_name('span')[1].text.strip()

    president_element = hard_fact_element.find_elements_by_class_name('row')[4]
    president_name = president_element.find_element_by_tag_name('h4').text.strip()

    founding_year, staff_number, members_number, languages = _extract_quick_facts(driver, idx)

    return HardFacts(website, president_name, founding_year, staff_number, members_number, languages)


def _extract_quick_facts(driver: WebDriver, idx: int) -> Tuple[Optional[int], Optional[int], Optional[int], List[str]]:
    founding_year = None
    staff_number = None
    members_number = None
    languages: List[str] = []

    possible_quick_facts_elements = driver.find_elements_by_class_name('ng-scope')
    likely_quick_facts_elements = [p for p in possible_quick_facts_elements if p.find_elements_by_tag_name('strong')]

    founded = [l for l in likely_quick_facts_elements if l.text.startswith('Founded')]
    staff = [l for l in likely_quick_facts_elements if l.text.strip().endswith('staff')]
    members = [l for l in likely_quick_facts_elements if l.text.strip().endswith('members')]
    working_languages = [l for l in likely_quick_facts_elements if l.text.startswith('Working languages')]

    if founded:
        founding_year = int(founded[0].find_element_by_tag_name('strong').text.strip())

    if staff:
        staff_string = staff[0].find_element_by_tag_name('strong').text.strip()
        staff_string = staff_string.replace(' ', '')
        try:
            staff_number = int(staff_string)
        except:
            if staff_string == '6fulltime+2interns':
                staff_number = 6
            if staff_string == '2.8':
                staff_number = 3
            if staff_string == '3employeesand7volunteers':
                staff_number = 3
            if staff_string == '5employees':
                staff_number = 5
            print(f'SKIPPING STAFF ({idx}) - {staff_string}')

    if members:
        members_string = members[0].find_element_by_tag_name('strong').text.strip()
        members_string = members_string.replace(' ', '')
        members_string = members_string.replace('+', '')
        try:
            members_number = int(members_string)
        except:
            if members_string == '384organisations':
                members_number = 384
            if members_string == '50delegations':
                members_number = 50
            if members_string == '120,000':
                members_number = 120000
            if members_string == 'Around35':
                members_number = 35
            if members_string == 'about5000':
                members_number = 5000
            if members_string == '46nationaluniversitysportsgoverningbodies':
                members_number = 46
            if members_string == 'around1000membersin34branches':
                members_number = 1000
            if members_string == '44associations':
                members_number = 44
            if members_string == 'approx.700':
                members_number = 700
            if members_string == '5,000,000':
                members_number = 5000000
            if members_string == '250associations':
                members_number = 250
            if members_string == '28memberorganisations':
                members_number = 28

    if working_languages:
        languages = working_languages[0].find_element_by_tag_name('strong').text.strip()

    return founding_year, staff_number, members_number, languages


def _extract_soft_facts(driver: WebDriver) -> SoftFacts:
    elements = driver.find_elements_by_tag_name('div')
    soft_facts_elements = elements[36]
    soft_facts_list = soft_facts_elements.find_elements_by_tag_name('p')

    aims = soft_facts_list[0].text.strip()
    activities = soft_facts_list[1].text.strip()
    accreditations = soft_facts_list[3].text.strip()
    areas_of_competence = _split_into_areas(soft_facts_list[7].text.strip())
    geographical_representation = _split_into_countries(soft_facts_list[8].text.strip())

    return SoftFacts(aims, activities, accreditations, areas_of_competence, geographical_representation)


def _split_into_areas(areas: str) -> List[str]:
    if not areas:
        return []

    areas = areas.replace('[', '')
    areas = areas.replace(']', '')
    areas = areas.replace('\"', '')
    splitted = areas.split(',')

    return [s.strip() for s in splitted if s]


def _split_into_countries(country_list: str) -> List[str]:
    if not country_list:
        return []

    splitted = country_list.split(',')
    return [s.strip() for s in splitted if s]


def _clean_detail_pages(infos: List[DetailPageInfo]) -> None:
    for idx, info in enumerate(infos):
        if info.hard_facts.founding_year < 1800:
            info.hard_facts.founding_year = None

        if idx == 7:
            info.hard_facts.members = 0
        if idx == 18:
            info.hard_facts.founding_year = 1999
        if idx == 40:
            info.soft_facts.accreditations = ''
        if idx == 53:
            info.soft_facts.accreditations = ''
        if idx == 56:
            info.hard_facts.members = 0
        if idx == 102:
            info.hard_facts.president = ''
            info.soft_facts.accreditations = ''
        if idx == 134:
            info.soft_facts.accreditations = ''
        if idx == 150:
            info.hard_facts.members = 0
        if idx == 201:
            info.hard_facts.members = 7000
        if idx == 207:
            info.soft_facts.accreditations = ''
        if idx == 234:
            info.hard_facts.president = ''
            info.soft_facts.accreditations = ''
            info.soft_facts.activities = ''
            info.soft_facts.aims = ''
        if idx == 251:
            info.soft_facts.accreditations = ''
        if idx == 310:
            info.soft_facts.accreditations = ''
            info.soft_facts.activities = ''
            info.soft_facts.aims = ''


if __name__ == '__main__':
    crawl()