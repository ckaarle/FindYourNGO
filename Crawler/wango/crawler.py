from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time


def crawl_all():
    url = 'https://www.wango.org/'
    driver = prepare_driver()
    file = open('results.txt', 'w', encoding="utf-8")

    driver.get(url)
    time.sleep(2)
    search_element = driver.find_element_by_css_selector('.btn-ngodir-search')
    search_element.click()
    time.sleep(3)

    for page_num in range(1115, 1117):
        if page_num != 1:
            driver.execute_script(f'javascript:goPage("{page_num}", "", "zz");void(0);')
        if page_num % 5 == 0:
            file.flush()
        ngo_names = driver.find_elements_by_css_selector('a b')
        ngo_locs = driver.find_elements_by_css_selector('.contentmargin0')
        # 'Next 50' and 'Previous 50' look just like orgs
        nav_elements = 2 if page_num != 1 and page_num != 1116 else 1
        content_count = len(ngo_names) - nav_elements
        if content_count != 50:
            print(f'Found only {content_count} ngos in page {page_num}, with {nav_elements} navigation items')
        for i in range(content_count):
            file.write(ngo_names[i].text + '\n' + ngo_locs[i * 2 + 1].text + '\n')

    file.flush()


def crawl_certified():
    url = 'https://www.wango.org/codeofethics.aspx?page=13'
    driver = prepare_driver()
    file = open('certified_results.txt', 'w', encoding="utf-8")

    driver.get(url)
    country_list = list(map(lambda elem: elem.text, driver.find_elements_by_css_selector('option')))
    print(f'Found {len(country_list)} countries to scrape, probably including an empty string')
    missing_websites = 0

    for country in country_list:
        if country == '':
            continue
        driver.get(f'{url}&country={country}')  # if broken, use .replace(" ", "%20")
        org_rows = driver.find_elements_by_css_selector('.content tbody tr')
        skip_non_org_rows_counter = 3
        for org_row in org_rows:
            if skip_non_org_rows_counter > 0:
                skip_non_org_rows_counter -= 1
                continue
            props = org_row.find_elements_by_css_selector('td')
            name = props[0].text
            city = props[1].text
            website = None
            try:
                website = props[2].find_element_by_css_selector('a').get_attribute('href')
            except NoSuchElementException:
                missing_websites += 1
            file.write(f'{name}\n{city}, {country}\n{website}\n')
        print(f'We are currently in {country}. There are {missing_websites} missing websites')
        file.flush()


def prepare_driver():
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--window-size=1920x1080')
    return webdriver.Chrome(chrome_options=chrome_options,
                            executable_path='chromedriver.exe')


if __name__ == '__main__':
    start = time.time()
    crawl_all()
    #crawl_certified()
    end = time.time()
    print(f"Everything took {end - start} seconds")
