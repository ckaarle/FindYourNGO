from typing import List, Optional


class FilterConfig:

    def __init__(
            self,
            branches_to_include: List[str] = None,
            topics_to_include: List[str] = None,
            use_ecosoc: bool = False,
            use_credible_source: bool = False,
            hq_country_to_include: List[str] = None,
            hq_city_to_include: str = '',
            use_contact_possible: bool = False,
            types_of_organization_to_include: List[str] = None,
            working_languages_to_include: List[str] = None,
            funding_to_include: List[str] = None,
            trustworthiness_lower_bound: Optional[float] = None,
    ):
        self._language_translations = {
            'English': ['Anglais', 'Englisch'],
            'French': ['Français', 'Französisch'],
            'German': ['Allemand', 'Deutsch'],
        }

        self.branches_to_include = branches_to_include if branches_to_include is not None else []
        self.topics_to_include = topics_to_include if topics_to_include is not None else []
        self.use_ecosoc = use_ecosoc
        self.use_credible_source = use_credible_source
        self.hq_country_to_include = hq_country_to_include if hq_country_to_include is not None else []
        self.hq_city_to_include = hq_city_to_include if hq_city_to_include is not None else []
        self.use_contact_possible = use_contact_possible
        self.types_of_organization_to_include = types_of_organization_to_include if types_of_organization_to_include is not None else []
        self.working_languages_to_include = self._add_translations(working_languages_to_include) if working_languages_to_include is not None else []
        self.funding_to_include = funding_to_include if funding_to_include is not None else []
        self.trustworthiness_lower_bound = trustworthiness_lower_bound

    def _add_translations(self, languages: List[str]) -> List[str]:
        if languages is None or not languages:
            return []
        else:
            languages_with_translations = []
            for language in languages:
                language = language.upper()

                for key, values in self._language_translations.items():
                    if key.upper() == language:
                        languages_with_translations.append(key)
                        languages_with_translations.extend(values)

            return languages_with_translations
