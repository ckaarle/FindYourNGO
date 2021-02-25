import decimal
from typing import Iterable
from django.db.models import Sum, Q

from findyourngo.restapi.controllers.ngo_controller import SELF_REPORTED_DATA_SOURCE
from findyourngo.restapi.models import NgoTWScore, NgoDataSource, NgoMetaData, NgoAccreditation, NgoReview, NgoAccount
from findyourngo.trustworthiness_calculator.trustworthiness_constants import RAW_SCORE_MIN_VALUE, RAW_SCORE_MAX_VALUE, \
    TW_MIN_VALUE, TW_MAX_VALUE, VALID_ACCREDITATIONS
from findyourngo.type_variables import TWScore


class TWCalculator:

    def __init__(self) -> None:
        self._raw_score_min_value = RAW_SCORE_MIN_VALUE
        self._raw_score_max_value = RAW_SCORE_MAX_VALUE

    def calculate_number_of_data_source_score(self, meta_data: NgoMetaData) -> TWScore:
        return len(meta_data.info_source.all())

    def calculate_data_source_credibility_score(self, meta_data: NgoMetaData) -> TWScore:
        if meta_data.info_source.filter(credible=True):
            return self._data_source_count() * 2 + 1
        else:
            return 0

    def calculate_ecosoc_score(self, accreditations: Iterable[NgoAccreditation]) -> TWScore:
        if any(filter(lambda acc: self._contains_valid_accreditation(acc.accreditation.upper()), accreditations)):
            return self._data_source_count()
        return 0

    def _contains_valid_accreditation(self, accreditations):
        return any(acc in accreditations for acc in VALID_ACCREDITATIONS)

    def _calculate_raw_base_score(
            self,
            number_data_sources_score: float,
            credible_source_score: float,
            ecosoc_score: float,
            ngo_account_score: float,
    ) -> float:
        return number_data_sources_score + credible_source_score + ecosoc_score + ngo_account_score

    def calculate_base_tw_from_partial_scores(
            self,
            number_data_sources_score: float,
            credible_source_score: float,
            ecosoc_score: float,
    ) -> TWScore:
        raw_score = self._calculate_raw_base_score(number_data_sources_score, credible_source_score, ecosoc_score, 0)
        return self._restrict_to_allowed_score_range_base(raw_score)

    def calculate_base_tw_from_ngo_tw_score(self, ngo_tw_score: NgoTWScore) -> TWScore:
        number_data_sources_score = ngo_tw_score.number_data_sources_score
        credible_source_score = ngo_tw_score.credible_source_score
        ecosoc_score = ngo_tw_score.ecosoc_score
        ngo_account_score = ngo_tw_score.ngo_account_score

        raw_score = self._calculate_raw_base_score(number_data_sources_score, credible_source_score, ecosoc_score, ngo_account_score)
        return self._restrict_to_allowed_score_range_base(raw_score)

    def calculate_user_tw_from_ngo_id(self, ngo_id: int) -> TWScore:
        amount_review_ratings = self._review_count(ngo_id)
        if amount_review_ratings == 0:
            return 0
        else:
            sum_review_ratings = self._review_rating_sum(ngo_id)
            return self._restrict_to_allowed_score_range_user(sum_review_ratings, amount_review_ratings)

    def calculate_tw_from_ngo_tw_scores(self, ngo_id: int, ngo_tw_score: NgoTWScore, user_tw_factor) -> TWScore:
        base_tw = ngo_tw_score.base_tw_score
        user_tw = ngo_tw_score.user_tw_score
        if self._review_count(ngo_id) == 0:
            return base_tw
        else:
            return base_tw * (1 - user_tw_factor) + user_tw * user_tw_factor

    def calculate_user_tw_factor(self, ngo_id: int) -> float:
        total_reviews = self._total_review_count()
        if total_reviews == 0:
            return 0
        ngo_reviews = self._review_count(ngo_id)
        return ngo_reviews / total_reviews

    def _restrict_to_allowed_score_range_user(self, sum_commenter_ratings: int, amount_commenter_ratings: int) -> float:
        user_raw_score = sum_commenter_ratings / amount_commenter_ratings
        raw_score_scaled = user_raw_score / (amount_commenter_ratings * TW_MAX_VALUE)
        range_of_target_interval = TW_MAX_VALUE - TW_MIN_VALUE

        score = raw_score_scaled * range_of_target_interval + TW_MIN_VALUE

        return self._round(score)

    def _restrict_to_allowed_score_range_base(self, base_raw_score: float) -> TWScore:
        raw_score_scaled_around_zero = (base_raw_score - self._raw_score_min_value) / (self._raw_score_max_value - self._raw_score_min_value)
        range_of_target_interval = TW_MAX_VALUE - TW_MIN_VALUE

        score = raw_score_scaled_around_zero * range_of_target_interval + TW_MIN_VALUE

        return self._round(score)

    def _data_source_count(self) -> int:
        return NgoDataSource.objects.exclude(source=SELF_REPORTED_DATA_SOURCE).count()

    def _total_review_count(self) -> int:
        return NgoReview.objects.count()

    def _review_count(self, ngo_id: int) -> int:
        return NgoReview.objects.filter(ngo=ngo_id).count()

    def _review_rating_sum(self, ngo_id: int) -> int:
        return NgoReview.objects.filter(ngo=ngo_id).aggregate(sum=Sum('rating'))['sum'] or 0

    # why is this function necessary when the python-native round() function exists?
    # since Python 3, this function implements banker's rounding:
    # round(0.5) == 0, round(1.5) == 2
    def _round(self, value: float) -> float:
        return float(decimal.Decimal(value).quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_HALF_UP))

    def calculate_ngo_account_score(self, ngo_id) -> float:
        accounts = NgoAccount.objects.filter(ngo_id=ngo_id, user__is_active=True)

        if len(accounts) > 0:
            return 1
        else:
            return 0

