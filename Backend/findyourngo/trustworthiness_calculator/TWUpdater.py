from findyourngo.restapi.models import Ngo, NgoTWDataPoint
from findyourngo.trustworthiness_calculator.Pagerank import PageRank
from findyourngo.trustworthiness_calculator.TWCalculator import TWCalculator
from findyourngo.trustworthiness_calculator.TWRecalculator import TWRecalculator

from datetime import datetime


class TWUpdater:

    def update_single_ngo(self, ngo: Ngo) -> None:
        self._calculate_tw_without_pagerank_for_ngo(ngo)

    def update(self) -> None:
        self._calculate_tw_without_pagerank()
        self._add_pagerank()

    def store(self) -> None:
        self.update()
        self.store_daily_tw()

    def store_daily_tw(self) -> None:
        for ngo in Ngo.objects.all():
            ngo_tw_score = ngo.tw_score

            if not ngo_tw_score.tw_series.filter(date=datetime.today()).exists():
                last_tw_entry = ngo_tw_score.tw_series.all().last()
                if last_tw_entry is None or not last_tw_entry.daily_tw_score == ngo_tw_score.total_tw_score:

                    daily_tw = NgoTWDataPoint.objects.create(daily_tw_score=ngo_tw_score.total_tw_score,
                                                             date=datetime.today())
                    ngo_tw_score.tw_series.add(daily_tw)

    def _calculate_tw_without_pagerank(self) -> None:
        for ngo in Ngo.objects.all():
            self._calculate_tw_without_pagerank_for_ngo(ngo)

    def _calculate_tw_without_pagerank_for_ngo(self, ngo: Ngo) -> None:
        ngo_tw_score = ngo.tw_score
        tw_calculator = TWCalculator()

        number_data_sources_score = tw_calculator.calculate_number_of_data_source_score(ngo.meta_data)
        credible_source_score = tw_calculator.calculate_data_source_credibility_score(ngo.meta_data)
        ecosoc_score = tw_calculator.calculate_ecosoc_score(ngo.accreditations.all())
        ngo_account_score = tw_calculator.calculate_ngo_account_score(ngo.id)

        user_tw_factor = tw_calculator.calculate_user_tw_factor(ngo.id)

        ngo_tw_score.number_data_sources_score = number_data_sources_score
        ngo_tw_score.credible_source_score = credible_source_score
        ngo_tw_score.ecosoc_score = ecosoc_score
        ngo_tw_score.ngo_account_score = ngo_account_score

        ngo_tw_score.base_tw_score = tw_calculator.calculate_base_tw_from_ngo_tw_score(ngo_tw_score)
        ngo_tw_score.user_tw_score = tw_calculator.calculate_user_tw_from_ngo_id(ngo.id)
        ngo_tw_score.total_tw_score = tw_calculator.calculate_tw_from_ngo_tw_scores(ngo.id, ngo_tw_score,
                                                                                    user_tw_factor)
        ngo_tw_score.save()

    def _add_pagerank(self) -> None:
        ngos = Ngo.objects.all()
        pagerank = PageRank(ngos).personalized_pagerank()

        if pagerank is not None:
            TWRecalculator().recalculate_with_pagerank(ngos, pagerank)
