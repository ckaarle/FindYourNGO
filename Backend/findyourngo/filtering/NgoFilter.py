import operator
from builtins import property
from functools import reduce

from django.db.models import QuerySet, Q

from findyourngo.filtering.filter_util import FilterConfig
from findyourngo.restapi.models import Ngo
from findyourngo.trustworthiness_calculator.trustworthiness_constants import VALID_ACCREDITATIONS
from findyourngo.type_variables import SortingOption


class NgoFilter:

    def __init__(self, filter_config: FilterConfig):
        self._filter_config = filter_config

    def apply(self, sorting_option: SortingOption) -> QuerySet:
        query_set = self._add_all_filters()

        query_set = self._sort(query_set, sorting_option)
        return query_set

    def _add_all_filters(self) -> QuerySet:
        query_set = Ngo.objects.filter(confirmed=True)
        query_set = query_set.filter(self._filter_name_condition)
        query_set = query_set.filter(self._filter_branches_condition)
        query_set = query_set.filter(self._filter_regions_condition)
        query_set = query_set.filter(self._filter_topics_condition)
        query_set = query_set.filter(self._filter_ecosoc_condition)
        query_set = query_set.filter(self._filter_credible_source_condition)
        query_set = query_set.filter(self._filter_hq_countries_condition)
        query_set = query_set.filter(self._filter_hq_cities_condition)
        query_set = query_set.filter(self._filter_contact_possible_condition)
        query_set = query_set.filter(self._filter_types_of_organization_condition)
        query_set = query_set.filter(self._filter_working_languages_condition)
        query_set = query_set.filter(self._filter_funding_condition)
        query_set = query_set.filter(self._filter_trustworthiness_condition)
        return query_set.distinct()

    @property
    def _filter_name_condition(self) -> Q:
        if self._filter_config.name_to_include:
            return Q(name__icontains=self._filter_config.name_to_include)
        else:
            return self._default_condition

    @property
    def _filter_branches_condition(self) -> Q:
        if self._filter_config.branches_to_include:
            return reduce(operator.or_, [Q(branches__country__name=b) for b in self._filter_config.branches_to_include])
        else:
            return self._default_condition

    @property
    def _filter_regions_condition(self) -> Q:
        if self._filter_config.regions_to_include:
            return reduce(operator.or_, [Q(branches__country__region=r) for r in self._filter_config.regions_to_include])
        else:
            return self._default_condition

    @property
    def _filter_topics_condition(self) -> Q:
        if self._filter_config.topics_to_include:
            return reduce(operator.or_, [Q(topics__topic__icontains=t) for t in self._filter_config.topics_to_include])
        else:
            return self._default_condition

    @property
    def _filter_ecosoc_condition(self) -> Q:
        if self._filter_config.use_accreditations:
            return reduce(operator.or_, [Q(accreditations__accreditation__icontains=acc) for acc in VALID_ACCREDITATIONS])
        else:
            return self._default_condition

    @property
    def _filter_credible_source_condition(self) -> Q:
        if self._filter_config.use_credible_source:
            return Q(meta_data__info_source__credible=True)
        else:
            return self._default_condition

    @property
    def _filter_hq_countries_condition(self) -> Q:
        if self._filter_config.hq_country_to_include:
            return reduce(operator.or_, [Q(contact__address__country__name=c) for c in self._filter_config.hq_country_to_include])
        else:
            return self._default_condition

    @property
    def _filter_hq_cities_condition(self) -> Q:
        if self._filter_config.hq_city_to_include:
            return reduce(operator.or_, [Q(contact__address__city=c) for c in self._filter_config.hq_city_to_include])
        else:
            return self._default_condition

    @property
    def _filter_contact_possible_condition(self) -> Q:
        if self._filter_config.use_contact_possible:
            return reduce(operator.or_, [
                Q(contact__ngo_phone_number__isnull=False),
                Q(contact__ngo_email__isnull=False),
                Q(contact__representative__isnull=False),
            ])
        else:
            return self._default_condition

    @property
    def _filter_types_of_organization_condition(self) -> Q:
        if self._filter_config.types_of_organization_to_include:
            return reduce(operator.or_, [Q(stats__type_of_organization__type=t) for t in self._filter_config.types_of_organization_to_include])
        else:
            return self._default_condition

    @property
    def _filter_working_languages_condition(self) -> Q:
        if self._filter_config.working_languages_to_include:
            return reduce(operator.or_, [Q(stats__working_languages__icontains=l) for l in self._filter_config.working_languages_to_include])
        else:
            return self._default_condition

    @property
    def _filter_funding_condition(self) -> Q:
        if self._filter_config.funding_to_include:
            return reduce(operator.or_, [Q(stats__funding__icontains=t) for t in self._filter_config.funding_to_include])
        else:
            return self._default_condition

    @property
    def _filter_trustworthiness_condition(self) -> Q:
        if self._filter_config.trustworthiness_lower_bound is not None:
            return Q(tw_score__total_tw_score__gte=self._filter_config.trustworthiness_lower_bound)
        else:
            return self._default_condition

    @property
    def _default_condition(self) -> Q:
        return Q()

    def _sort(self, query_set: QuerySet, sorting_option: SortingOption) -> QuerySet:
        sorting_option_value = sorting_option["keyToSort"]
        
        if sorting_option_value == "name":
            query_set = self._sort_by_default_condition(query_set, sorting_option)
        elif sorting_option_value == "countries":
            query_set = self._sort_by_default_condition(query_set, self._get_ngo_address_condition(sorting_option, "country__name"))
        elif sorting_option_value == "cities":
            query_set = self._sort_by_default_condition(query_set, self._get_ngo_address_condition(sorting_option, "city"))
        elif sorting_option_value == "trustworthiness":
            query_set = self._sort_by_tw_value(sorting_option, query_set)
        elif sorting_option_value == 'reviewNumber':
            query_set = self._sort_by_ngo_number_of_reviews(sorting_option, query_set)
        else:
            query_set = self._sort_by_default_condition(query_set, sorting_option)

        # always sort if trustworthiness filter is applied
        if self._filter_config.trustworthiness_lower_bound is not None and sorting_option_value != "trustworthiness":
            query_set = query_set.order_by('-tw_score__total_tw_score', 'name')

        return query_set

    def _sort_by_default_condition(self, query_set: QuerySet, sorting_option: SortingOption) -> QuerySet:
        return query_set.exclude(**{sorting_option["keyToSort"]: ''}).order_by(f'{"-" if sorting_option["orderToSort"] =="desc" else ""}{sorting_option["keyToSort"]}')

    def _get_ngo_address_condition(self, sorting_option: SortingOption, parameter_name: str) -> SortingOption:
        sorting_option["keyToSort"] = f'contact__address__{parameter_name}'
        return sorting_option

    def _get_trustworthiness_condition(self, sorting_option: SortingOption) -> SortingOption:
        sorting_option["keyToSort"] = 'tw_score__total_tw_score'
        return sorting_option

    def _sort_by_ngo_number_of_reviews(self, sorting_option: SortingOption, query_set: QuerySet) -> QuerySet:
        return query_set.order_by(f'{"-" if sorting_option["orderToSort"] =="desc" else ""}number_of_reviews')

    def _sort_by_tw_value(self, sorting_option: SortingOption, query_set: QuerySet) -> QuerySet:
        return query_set.order_by(f'{"-" if sorting_option["orderToSort"] =="desc" else ""}tw_score__total_tw_score')





