# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

# This is used to calculate whether an organisation is eligible to conduct a progressive lottery


class progressive_lottery__game_meets_criteria(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    label = "The eligibility conditions for organising a progessive lottery are being met by the organisation"

    def formula(organisation, period, parameters):
        return (
            (organisation('value_of_individual_prize', period) <= parameters(period).permitted_games.progressive_lottery.max_value_of_individual_prize))


class progressive_lottery__authority_required(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    default_value = False
    label = "If the progressive lottery is a permitted gaming activity, is an authority required to conduct it?"

    def formula(organisation, period, parameters):
        return (
            (organisation('total_prize_value_of_all_prizes_from_gaming_activity', period) > parameters(period).permitted_games.progressive_lottery.total_prize_value_threshold))
