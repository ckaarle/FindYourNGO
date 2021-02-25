import json
import pickle
import urllib
from typing import List

from findyourngo.data_import.InfoClasses import Info
from findyourngo.data_import.european_council.util import _extract_info, _clean_info


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
    with urllib.request.urlopen("http://coe-ngo.org/ingo") as url:
        data = json.loads(url.read().decode())

        infos = _extract_info(data)
        _clean_info(infos)

    filename = 'european_council_pickled'
    _serialize(infos, filename)

    read_infos = deserialize(filename)

    assert len(infos) == len(read_infos)