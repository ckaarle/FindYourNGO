from findyourngo.restapi.models import Ngo
from findyourngo.trustworthiness_calculator.Pagerank import PageRank
from findyourngo.trustworthiness_calculator.TWCalculator import TWCalculator
from findyourngo.trustworthiness_calculator.TWRecalculator import TWRecalculator


class TWUpdater:

    def update(self) -> None:
        self._calculate_tw_without_pagerank()
        self._add_pagerank()

    def _calculate_tw_without_pagerank(self) -> None:
        for ngo in Ngo.objects.all():
            self._calculate_tw_without_pagerank_for_ngo(ngo)

    def _calculate_tw_without_pagerank_for_ngo(self, ngo: Ngo) -> None:
        ngo_tw_score = ngo.tw_score
        tw_calculator = TWCalculator()

        number_data_sources_score = tw_calculator.calculate_number_of_data_source_score(ngo.meta_data)
        credible_source_score = tw_calculator.calculate_data_source_credibility_score(ngo.meta_data)
        ecosoc_score = tw_calculator.calculate_ecosoc_score(ngo.accreditations.all())

        user_tw_factor = tw_calculator.calculate_user_tw_factor(ngo.id)

        ngo_tw_score.number_data_sources_score = number_data_sources_score
        ngo_tw_score.credible_source_score = credible_source_score
        ngo_tw_score.ecosoc_score = ecosoc_score

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
