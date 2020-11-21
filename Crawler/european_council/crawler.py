import time
from typing import List

from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from european_council.MainPageInfo import Name, Address, ContactInfo, Representative, MainPageInfo

URL = 'http://coe-ngo.org/#/ingos'


def crawl() -> None:
    driver = _get_driver()
    driver.get(URL)

    _crawl_main_page(driver)

    # TODO crawl detail pages


def _get_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/Users/Chris/Downloads/chromedriver", chrome_options=options)
    return driver


def _crawl_main_page(driver):
    rows: List[WebElement] = _get_table_rows(driver)

    extracted_information = []
    for row in rows:
        cols = row.find_elements_by_tag_name('td')
        cols = filter_empty_cols(cols)

        main_page_info = extract_information(cols)
        extracted_information.append(main_page_info)

    run_sanity_checks(extracted_information)

    extracted_information = clean_up(extracted_information)
    # TODO clean up


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
    link: WebElement = extract_detail_link(cols[0])
    # cols[1] is name in French
    address: Address = extract_address(cols[2])
    contact: ContactInfo = extract_contact_information(cols[3])
    representative: Representative = extract_representative(cols[4])

    return MainPageInfo(idx, name, link, address, contact, representative)


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


def extract_detail_link(col: WebElement) -> WebElement:
    # TODO
    return None


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


if __name__ == '__main__':
    crawl()