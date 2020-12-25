from findyourngo.restapi.models import Ngo, NgoAccreditation, NgoMetaData, NgoAddress, NgoContact, NgoDataSource
from findyourngo.data_import.data_importer import update_ngo_tw_score, _get_ngo_tw_score


def import_wango_general_data(source):
    with open('/wango/results.txt', encoding='utf-8') as results:
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
                        print(f"No name found in line {line_num-1} '{line}'")
                        continue
                    create_or_update_ngo(name, source, acronym, country, city, street)
                    if city is None:
                        print(f"No city found in line {line_num} '{line}'")
            except Exception as e:
                print(f"Failure in line {line_num} '{line}': {e}")


def import_wango_accredited_data(source, accreditation):
    with open('/wango/certified_results.txt', encoding='utf-8') as certified_results:
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
                        print(f"No name found in line {line_num-2} '{line}'")
                        continue
                    create_or_update_ngo(name, source, acronym, country, city, street,
                                         email=email, accreditation=accreditation)
                    if city is None:
                        print(f"No city found in line {line_num} '{line}'")
            except Exception as e:
                print(f"Failure in line {line}: {e}")


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
    address = address.strip().split(',')
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
    return country, city, street


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
    if NgoDataSource.objects.filter(source='Wango').count() > 0:
        return False
    source = NgoDataSource.objects.create(credible=False, source='Wango')
    import_wango_general_data(source)
    accreditation = NgoAccreditation.objects.create(accreditation='Wango Code of Ethics')
    import_wango_accredited_data(source, accreditation)
    return True
