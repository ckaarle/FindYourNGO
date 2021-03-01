import shutil
from findyourngo.restapi.models import Ngo, NgoAccreditation, NgoMetaData, NgoAddress, NgoContact, NgoDataSource, \
    NgoCountry
from findyourngo.data_import.data_importer import update_ngo_tw_score, _get_ngo_tw_score


def import_wango_general_data(source):
    countries = []
    guessed_countries = []
    with open('/tmp/results.txt', encoding='utf-8') as results:
        line_num = 0
        for line in results:
            line = line.strip()
            try:
                line_num += 1
                if line_num % 2 == 1:  # handle name of ngo
                    name, acronym = parse_name(line)
                if line_num % 2 == 0:  # handle address of ngo
                    country, city, street = parse_address(line)
                if line_num % 2 == 0:  # update ngo
                    if name is None:
                        print(f'No name found in line {line_num-1} "{line}"')
                        continue
                    try:
                        country = fix_country(country)
                        if country == '' or country is None:
                            country = guess_country(city)
                            if country != '' and country is not None:
                                guessed_countries.append((city, country))
                        country = NgoCountry.objects.get(name=country)
                    except:
                        if country not in countries:
                            countries.append(f'{line_num}:{country}')
                        country = None
                    create_or_update_ngo(name, source, acronym, country, city, street)
            except Exception as e:
                print(f'Failure in line {line_num} "{line}": {e}')
    print(f'Following {len(countries)} countries not found: {countries}')
    print(f'Following {len(guessed_countries)} countries were guessed using cities: {guessed_countries}')


def import_wango_accredited_data(source, accreditation):
    countries = []
    guessed_countries = []
    with open('/tmp/certified_results.txt', encoding='utf-8') as certified_results:
        line_num = 0
        for line in certified_results:
            line = line.strip()
            try:
                line_num += 1
                if line_num % 3 == 1:  # handle name of ngo
                    name, acronym = parse_name(line)
                if line_num % 3 == 2:  # handle address of ngo
                    country, city, street = parse_address(line)
                if line_num % 3 == 0:  # handle email of ngo
                    email = parse_email(line)
                if line_num % 3 == 0:  # update ngo
                    if name is None:
                        print(f'No name found in line {line_num-2} "{line}"')
                        continue
                    try:
                        country = fix_country(country)
                        if country == '' or None:
                            country = guess_country(city)
                            if country != '' and country is not None:
                                guessed_countries.append((city, country))
                        country = NgoCountry.objects.get(name=country)
                    except:
                        if country not in countries:
                            countries.append(f'{line_num}:{country}')
                        country = None
                    create_or_update_ngo(name, source, acronym, country, city, street,
                                         email=email, accreditation=accreditation)
            except Exception as e:
                print(f'Failure in line {line}: {e}')
    print(f'Following {len(countries)} countries (accredited) not found: {countries}')
    print(f'Following {len(guessed_countries)} countries were guessed using cities: {guessed_countries}')


def parse_name(name) -> (str, str):
    acronym = None
    name = name.strip().upper()
    if len(name) == 0:
        name = None
    elif name == '1':
        name = None
    elif name[-1] == ')' and name.find('(') != -1:
        acronym = name[name.index('(') + 1:-1].strip()
        if len(acronym) < 10:
            name = name[0:name.index('(')].strip()
        else:
            acronym = None
    return name, acronym


def parse_address(address) -> (str, str, str):
    address = address.upper().strip().split(',')
    address = [x.strip() for x in address]
    street = None
    if address[0] == '1':
        return None, None, None
    if len(address) == 1:
        country = address[0]
        city = None
    elif len(address) == 2:
        country = address[1]
        city = address[0]
    elif len(address) == 3 and (address[1] == '' or address[1] == address[2]):
        country = address[2]
        city = address[0]
    else:
        country = address.pop()
        city = address.pop()
        street = ', '.join(address)
    return country.upper(), city, street


def fix_country(country):
    countries = {
        'UNITED STATES': 'UNITED STATES OF AMERICA',
        'USA': 'UNITED STATES OF AMERICA',
        'UNTIED STATES': 'UNITED STATES OF AMERICA',
        'UNITED KINGDOM': 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND',
        'UK': 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND',
        "COTE D'IVOIRE": 'CÔTE D’IVOIRE',
        'MACEDONIA': 'NORTH MACEDONIA',
        'OCCUPIED PALESTINIAN TERRITORY': 'STATE OF PALESTINE',
        'PALESTINE': 'STATE OF PALESTINE',
        'PALESTINIAN AUTHORITY': 'STATE OF PALESTINE',
        'HONG KONG SPECIAL ADMINISTRATIVE REGION OF CHINA': 'CHINA',
        'MACAO SPECIAL ADMINISTRATIVE REGION OF CHINA': 'CHINA',
        'TAIWAN': 'CHINA',
        'NETHERLANDS ANTILLES': 'NETHERLANDS',
        'LIBYAN ARAB JAMAHIRIYA': 'LIBYA',
        'CZECH REPUBLIC': 'CZECHIA',
        'VIETNAM': 'VIET NAM',
        'RUSSIA': 'RUSSIAN FEDERATION',
        'VENEZUELA': 'VENEZUELA (BOLIVARIAN REPUBLIC OF)',
        'MOLDOVA': 'REPUBLIC OF MOLDOVA',
        'SWAZILAND': 'ESWATINI',
        'VIRGIN ISLANDS': 'UNITED STATES VIRGIN ISLANDS',
        'IRAN': 'IRAN (ISLAMIC REPUBLIC OF)',
        'BOLIVIA': 'BOLIVIA (PLURINATIONAL STATE OF)',
        'BOLIVIA (MOZAMBIQUE)': 'BOLIVIA (PLURINATIONAL STATE OF)',
        'ANTIGUA & BARBUDA': 'ANTIGUA AND BARBUDA',
        'BOSNIA & HERZEGOVINA': 'BOSNIA AND HERZEGOVINA',
        'YUGOSLAVIA': '',  # Yugoslavia does not exist -> 7 possible countries
        'EAST TIMOR': 'TIMOR-LESTE',
        'LAO PDR': "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
        'MARIANA ISLANDS': 'NORTHERN MARIANA ISLANDS',
        'FALKLAND ISLANDS': 'FALKLAND ISLANDS (MALVINAS)',
        'KOSOVO': 'SERBIA',
        'ST. KITTS & NEVIS': 'SAINT KITTS AND NEVIS',
        'ST. LUCIA': 'SAINT LUCIA',
        'SYRIA': 'SYRIAN ARAB REPUBLIC',
        'LEEWARD ISLANDS': 'ANGUILLA',
        'EASTERN AND SOUTHERN EUROPE': '',  # This is not a country
    }
    if country in countries:
        return countries[country]
    return country


def guess_country(city):
    addresses = NgoAddress.objects.filter(city=city)
    if addresses.count() == 0:
        print(f'The city {city} could not be assigned because it was never encountered')
        return ''
    max_count = 0
    for country in NgoAddress.objects.filter(city=city).values_list('country__name').distinct():
        country = country[0]
        filtered_addresses = NgoAddress.objects.filter(city=city, country__name=country)
        if filtered_addresses.count() > addresses.count() * 0.8:
            return country
        if filtered_addresses.count() > max_count:
            max_count = filtered_addresses.count()
    percentage = max_count / addresses.count()
    print(f'The city {city} could not be assigned. Maximum matches: {max_count} of {addresses.count()} => {percentage}')


def parse_email(email) -> str:
    email = email.strip()
    if email == 'None':
        email = None
    elif '.' not in email:
        email = None
    elif 'nawa.org' in email:
        email = 'http://www.nawa.org.pk'
    elif '%20%2C%20' in email:
        email = email.replace('%20%2C%20', ', ')
    elif '%2C%20' in email:
        email = email.replace('%2C%20', ', ')
    elif 'http://%20' in email:
        email = email[10:]
    elif '.%20' in email:
        email = email.replace('%20', '')
    elif '%20or%20' in email:
        email = email.replace('%20or%20', ', ').replace('%20', '')
    elif 'wibglobal' in email:
        email = email.replace('%20', ', ')
    elif 'cmdo.org' in email:
        email = 'http://www.cmdo.org'
    elif 'kvlifelinefoundation' in email:
        email = 'http://www.kvlifelinefoundation.com'
    elif 'fundraising.com' in email:
        email = None
    return email


def create_or_update_ngo(name, source, acronym, country, city, street, email=None, accreditation=None):
    if Ngo.objects.filter(name=name).count() > 0:
        ngo = Ngo.objects.get(name=name)
        ngo.meta_data.info_source.add(source)
    else:
        meta_data = NgoMetaData.objects.create()
        meta_data.info_source.add(source)
        tw_score = _get_ngo_tw_score([], meta_data)
        if acronym:
            ngo = Ngo.objects.create(name=name, acronym=acronym, meta_data=meta_data, tw_score=tw_score)
        else:
            ngo = Ngo.objects.create(name=name, meta_data=meta_data, tw_score=tw_score)
    if ngo.contact is None:
        ngo.contact = NgoContact.objects.create()
    if ngo.contact.address is None:
        if street:
            ngo.contact.address = NgoAddress.objects.create(country=country, city=city, street=street)
        if city:
            ngo.contact.address = NgoAddress.objects.create(country=country, city=city)
        else:
            ngo.contact.address = NgoAddress.objects.create(country=country)
    if email and ngo.contact.ngo_email is None:
        ngo.contact.ngo_email = email
        update_ngo_tw_score(ngo)
    if accreditation:
        ngo.accreditations.add(accreditation)


def run_wango_data_import() -> bool:
    # Move results to tmp directory to avoid slow wsl2 mounted file reading speed
    shutil.copyfile('/wango/results.txt', '/tmp/results.txt')
    shutil.copyfile('/wango/certified_results.txt', '/tmp/certified_results.txt')

    if NgoDataSource.objects.filter(source='Wango').count() > 0:
        return False
    source = NgoDataSource.objects.create(credible=False, source='Wango')
    import_wango_general_data(source)
    accreditation = NgoAccreditation.objects.create(accreditation='WCE')
    import_wango_accredited_data(source, accreditation)

    print(f'Updating the TW score, since it depends on # data sources, which might have changed after the initial import')
    all_ngo_entries = Ngo.objects.all()
    for ngo in all_ngo_entries:
        update_ngo_tw_score(ngo)
        ngo.save()
    return True
