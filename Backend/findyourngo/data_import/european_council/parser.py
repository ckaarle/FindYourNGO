from typing import List

from findyourngo.data_import.InfoClasses import Info
from findyourngo.data_import.european_council.store_results import deserialize


def parse_european_council() -> List[Info]:
    filename = 'findyourngo/data_import/european_council/european_council_pickled'
    read_infos = deserialize(filename)
    return read_infos


if __name__ == '__main__':
    parse_european_council()