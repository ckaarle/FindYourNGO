from typing import Dict, Iterable

from findyourngo.restapi.models import Ngo
from findyourngo.trustworthiness_calculator import TWCalculator
from findyourngo.trustworthiness_calculator.trustworthiness_constants import RAW_SCORE_AFTER_PAGERANK_MIN_VALUE, \
    RAW_SCORE_AFTER_PAGERANK_MAX_VALUE
# TODO include pagerank in this

# 1. calculate TW for all NGOs (without PageRank score)
# 2. calculate PageRank for all NGOs


class TWRecalculator(TWCalculator):

    def __init__(self) -> None:
        self._raw_score_min_value = RAW_SCORE_AFTER_PAGERANK_MIN_VALUE
        self._raw_score_max_value = RAW_SCORE_AFTER_PAGERANK_MAX_VALUE

    def recalculate_with_pagerank(self, ngos: Iterable[Ngo], pagerank: Dict[str, float]) -> None:
        map(lambda ngo: self._update_tw_with_pagerank(ngo, pagerank), ngos)

    def _update_tw_with_pagerank(self, ngo: Ngo, pagerank: Dict[str, float]) -> None:
        pagerank_score = pagerank[ngo.name] * 2 if ngo.name in pagerank.keys() else 0
        ngo.tw_score.pagerank_score = pagerank_score

        tw_score = ngo.tw_score.total_tw_score
        tw_score_scaled = self._restrict_to_allowed_score_range(tw_score)
        ngo.tw_score.total_tw_score = tw_score_scaled
        ngo.save()