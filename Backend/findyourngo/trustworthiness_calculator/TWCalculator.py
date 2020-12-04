import decimal
from typing import Iterable

from findyourngo.restapi.models import NgoTWScore, NgoDataSource, NgoMetaData, NgoAccreditation
from findyourngo.trustworthiness_calculator.trustworthiness_constants import RAW_SCORE_MIN_VALUE, RAW_SCORE_MAX_VALUE, \
    TW_MIN_VALUE, TW_MAX_VALUE
from findyourngo.type_variables import TWScore


class TWCalculator:

    def calculate_number_of_data_source_score(self, meta_data: NgoMetaData) -> TWScore:
        return len(meta_data.info_source.all()) / 1

    def calculate_data_source_credibility_score(self, meta_data: NgoMetaData) -> TWScore:
        if meta_data.info_source.filter(credible=True):
            return self._data_source_count() * 2 + 1
        else:
            return 0

    def calculate_ecosoc_score(self, accreditations: Iterable[NgoAccreditation]) -> TWScore:
        if any(filter(lambda acc: 'ECOSOC' in acc.accreditation.upper(), accreditations)):
            return self._data_source_count()
        return 0

    def _calculate_raw_score(
            self,
            number_data_sources_score: float,
            credible_source_score: float,
            ecosoc_score: float,
    ) -> float:
        return number_data_sources_score + credible_source_score + ecosoc_score

    def calculate_tw_from_partial_scores(
            self,
            number_data_sources_score: float,
            credible_source_score: float,
            ecosoc_score: float,
    ) -> TWScore:
        raw_score = self._calculate_raw_score(number_data_sources_score, credible_source_score, ecosoc_score)
        return self._restrict_to_allowed_score_range(raw_score)

    def calculate_tw_from_ngo_tw_score(self, ngo_tw_score: NgoTWScore) -> TWScore:
        number_data_sources_score = ngo_tw_score.number_data_sources_score
        credible_source_score = ngo_tw_score.credible_source_score
        ecosoc_score = ngo_tw_score.ecosoc_score

        raw_score = self._calculate_raw_score(number_data_sources_score, credible_source_score, ecosoc_score)
        return self._restrict_to_allowed_score_range(raw_score)

    def _restrict_to_allowed_score_range(self, raw_score: float) -> TWScore:
        raw_score_scaled_around_zero = (raw_score - RAW_SCORE_MIN_VALUE) / (RAW_SCORE_MAX_VALUE - RAW_SCORE_MIN_VALUE)
        range_of_target_interval = TW_MAX_VALUE - TW_MIN_VALUE

        score = raw_score_scaled_around_zero * range_of_target_interval + TW_MIN_VALUE

        return self._round(score)

    def _data_source_count(self) -> int:
        return NgoDataSource.objects.count()

    # why is this function necessary when the python-native round() function exists?
    # since Python 3, this function implements banker's rounding:
    # round(0.5) == 0, round(1.5) == 2
    def _round(self, value: float) -> float:
        return float(decimal.Decimal(value).quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_HALF_UP))
