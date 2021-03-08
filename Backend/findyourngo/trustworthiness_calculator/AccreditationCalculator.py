from findyourngo.restapi.models import Ngo
from findyourngo.trustworthiness_calculator.trustworthiness_constants import VALID_ACCREDITATIONS


class AccreditationCalculator:

    def has_valid_accreditation_and_wango_code_of_ethics(self, ngo: Ngo):
        has_accreditation = False
        wango_code_of_ethics = False

        for accreditation in ngo.accreditations.all():
            acc = accreditation.accreditation.upper()
            has_accreditation = has_accreditation or self._contains_valid_accreditation(acc)
            wango_code_of_ethics = wango_code_of_ethics or self._contains_wce(acc)

        return has_accreditation, wango_code_of_ethics

    def _contains_valid_accreditation(self, accreditation):
        return any(acc in accreditation for acc in VALID_ACCREDITATIONS)

    def _contains_wce(self, accreditation):
        return 'WCE' in accreditation
