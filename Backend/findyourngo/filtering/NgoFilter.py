import operator
from builtins import property
from functools import reduce

from django.db.models import QuerySet, Q

from findyourngo.filtering.filter_util import FilterConfig
from findyourngo.restapi.models import Ngo


class NgoFilter:

    def __init__(self, filter_config: FilterConfig):
        self._filter_config = filter_config

    def apply(self) -> QuerySet:
        query_set = self._add_all_filters()

        query_set = self._sort(query_set)
        return query_set

    def _add_all_filters(self) -> QuerySet:
        query_set = Ngo.objects.all()
        query_set = query_set.filter(self._filter_branches_condition)
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
        return query_set

    @property
    def _filter_branches_condition(self) -> Q:
        if self._filter_config.branches_to_include:
            return reduce(operator.or_, [Q(branches__country=b) for b in self._filter_config.branches_to_include])
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
        if self._filter_config.use_ecosoc:
            return Q(accreditations__accreditation__icontains='ECOSOC')
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
            return reduce(operator.or_, [Q(contact__address__country=c) for c in self._filter_config.hq_country_to_include])
        else:
            return self._default_condition

    @property
    def _filter_hq_cities_condition(self) -> Q:
        if self._filter_config.hq_city_to_include:
            return Q(contact__address__city=self._filter_config.hq_city_to_include)
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

    def _sort(self, query_set: QuerySet) -> QuerySet:
        query_set = query_set.order_by('name')

        if self._filter_config.trustworthiness_lower_bound is not None:
            # trustworthiness DESC, name ASC
            query_set = query_set.order_by('-tw_score__total_tw_score', 'name')

        return query_set