from typing import List

from findyourngo.filtering.filter_util import FilterConfig
from findyourngo.restapi.models import Ngo


class Filter:

    def __init__(self, filter_config: FilterConfig):
        self._filter_config = filter_config

    def apply(self) -> List[Ngo]:
        return [] # TODO