from typing import Dict, Iterable

from findyourngo.restapi.models import Ngo
from findyourngo.trustworthiness_calculator.TWCalculator import TWCalculator
from findyourngo.trustworthiness_calculator.trustworthiness_constants import TW_MAX_VALUE, PAGERANK_SCORE_MAX_VALUE, \
    PAGERANK_SCORE_MIN_VALUE
from findyourngo.trustworthiness_calculator.utils import round_value, round_to_two_decimal_places


class TWRecalculator(TWCalculator):

    def recalculate_with_pagerank(self, ngos, pagerank: Dict[str, float]) -> None:
        relevant_ngos = ngos.filter(name__in=pagerank.keys())
        for ngo in relevant_ngos:
            self._update_tw_with_pagerank(ngo, pagerank)

    def _update_tw_with_pagerank(self, ngo: Ngo, pagerank: Dict[str, float]) -> None:
        pagerank_score = self._calculate_pagerank_factor(ngo, pagerank)
        ngo.tw_score.pagerank_score = pagerank_score

        tw_score = ngo.tw_score.total_tw_score + pagerank_score
        tw_score_scaled = min(TW_MAX_VALUE, tw_score)
        ngo.tw_score.total_tw_score = round_to_two_decimal_places(tw_score_scaled)
        ngo.tw_score.save()

    def _calculate_pagerank_factor(self, ngo: Ngo, pagerank: Dict[str, float]):
        pagerank_raw_factor = len(pagerank.keys())

        score_unscaled = pagerank[ngo.name] * pagerank_raw_factor
        score_scaled = self._scale_pagerank_score(score_unscaled, pagerank_raw_factor)

        scale_factor = (TW_MAX_VALUE / (TW_MAX_VALUE - ngo.tw_score.total_tw_score)) if ngo.tw_score.total_tw_score != TW_MAX_VALUE else TW_MAX_VALUE
        score_factored = score_scaled / scale_factor

        return score_factored

    def _scale_pagerank_score(self, score_unscaled: float, raw_max_value: int) -> float:
        raw_min_value = 0
        raw_score_scaled_around_zero = (score_unscaled - raw_min_value) / (
                    raw_max_value - raw_min_value)
        range_of_target_interval = PAGERANK_SCORE_MAX_VALUE - PAGERANK_SCORE_MIN_VALUE

        score = raw_score_scaled_around_zero * range_of_target_interval + PAGERANK_SCORE_MIN_VALUE

        return round_value(score)