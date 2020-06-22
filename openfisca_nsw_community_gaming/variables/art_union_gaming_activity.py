# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, an Organisation…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


# This is used to calculate whether an organisation is eligible to conduct
# a calcutta
class art_union__gaming_activity_type(Variable):
    value_type = bool
    entity = Organisation
    definition_period = ETERNITY
    label = "Is it an art union gaming activity"
    reference = "Part 2 (4) - Community Gaming Regulation 2020"

    def formula(organisation, period, parameters):
        gt = organisation('gaming_activity_type', period)
        GT = gt.possible_values
        return gt == GT.art_union_gaming_activity


# This formula is used to calculate whether an organisation
# meets criteria for conducting an art union gaming activity
class art_union__game_meets_criteria(Variable):
    value_type = bool
    entity = Organisation
    definition_period = ETERNITY
    label = "The eligibility conditions for organising an art union gaming \
    activity are being met by the organisation"
    reference = "Part 2 (4) - Community Gaming Regulation 2020"

    def formula(organisation, period, parameters):

        return (
            organisation('art_union__gaming_activity_type', period)
            and (organisation(
                 'total_prize_value_of_all_prizes_from_gaming_activity',
                 period) > parameters(
                 period
                 ).permitted_games.
                 art_union_gaming_activity.
                min_total_value_of_all_prizes)
            and (organisation(
                 'proceeds_to_benefitting_organisation', period)
                 >= ((organisation('gross_proceeds_from_gaming_activity',
                  period)
                and parameters(period).permitted_games.
                art_union_gaming_activity.
                min_gross_proceeds_percent_to_benefit_org)))
            and (organisation(
                 'money_payable_as_separate_prize', period)
                 <= parameters(period).permitted_games.
                 art_union_gaming_activity.max_money_for_separate_prize)
            and organisation('is_art_union', period))


# This variable is only needed when the calcutta is a permitted gaming
# activity and is used to calculate whether an authority is required to conduct
# the art union gaming activity
class art_union_gaming__authority_required(Variable):
    value_type = bool
    entity = Organisation
    definition_period = MONTH
    default_value = True
    label = "If the art union gaming activity is a permitted gaming activity,\
    is an authority required to conduct it?"
    reference = "Part 2 (4) - Community Gaming Regulation 2020"
