"""Câblage CEQ pour les études Afrique de l'Ouest.

Ce module porte ce qui était historiquement codé en dur dans le cœur openfisca-ceq et
qui est en réalité propre à l'étude CEQ-Afrique :

- les variables d'enquête concrètes (secteur_activite, survey_income, categorie_cgu, …),
- la table des types d'activité ``labor_type_by_index``,
- la réforme ``ceq`` qui greffe le framework générique du cœur
  (:func:`openfisca_ceq.tools.tax_benefit_system_ceq_completion.add_ceq_framework`) en lui
  injectant les données de l'étude : mapping de revenus harmonisés, variables ``custom``
  multi-pays, variables d'enquête ci-dessous et coûts unitaires d'éducation par pays.
"""

import logging

from openfisca_core.model_api import Enum, not_, select, Variable, YEAR
from openfisca_core.reforms import Reform

from openfisca_ceq import entities
from openfisca_ceq.tools.tax_benefit_system_ceq_completion import (
    add_ceq_framework,
    add_ceq_education_unit_cost,
)

from openfisca_ceq_afrique_ouest.data_ceq_correspondence import (
    multi_country_custom_ceq_variables,
    non_ceq_input_by_harmonized_variable,
)
from openfisca_ceq_afrique_ouest.data.education_unit_cost import (
    build_unit_cost_by_category_by_country,
)


log = logging.getLogger(__name__)


unit_cost_by_category_by_country = build_unit_cost_by_category_by_country()

MALI_PART_INFORMEL_NON_SALARIE = 1.0


class cadre(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu est un cadre salarié"


class categorie_cgu(Variable):
    # prod A: revendeurs de ciments et de denrées alimentaires
    # prod B: autres commerçants ou revendeurs (CGU )
    # [CGU comm/prod A < CGU comm/prod B < CGU service] -> 0, 1 ,2
    # NaNs are -1
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "Index de la catgeorie CGU de l'individu"


labor_type_by_index = {
    0: "Inactive",
    1: "Formal public wage worker",
    2: "Formal private wage worker",
    3: "Informal wage worker",
    4: "Informal independent worker",
    5: "Agricultural worker",
}


class TypesLaborType(Enum):
    __order__ = "inactive formal_public_wage_worker formal_private_wage_worker informal_wage_worker informal_independent_worker agricultural_worker"
    inactive = ("Inactive",)
    formal_public_wage_worker = ("Formal public wage worker",)
    formal_private_wage_worker = ("Formal private wage worker",)
    informal_wage_worker = ("Informal wage worker",)
    informal_independent_worker = ("Informal independent worker",)
    agricultural_worker = ("Agricultural worker",)


class labor_type(Variable):
    value_type = Enum
    possible_values = TypesLaborType
    default_value = TypesLaborType.inactive
    entity = entities.Household
    definition_period = YEAR
    label = "Activité de la personne de référence du ménage"

    def formula(household, period):
        secteur_activite = household.personne_de_reference("secteur_activite", period)
        # Actif agricole < Salarie/dependant formel < Salarie/dependant informel <Independant
        secteur_public = household.personne_de_reference("secteur_public", period)
        return select(
            [
                secteur_activite == -1,  # Inactif ?
                (secteur_activite == 1) & secteur_public,  # Formal public wage worker
                (secteur_activite == 1)
                & not_(secteur_public),  # Formal private wage worker
                secteur_activite == 2,  # Informal wage worker
                secteur_activite == 3,  # Informal independent worker
                secteur_activite == 0,  # Agricultural worker
            ],
            [
                0,
                1,
                2,
                3,
                4,
                5,
            ],
        )


class number_of_people_per_household(Variable):
    value_type = int
    entity = entities.Household
    definition_period = YEAR
    label = "Nombre d'individus par ménage"

    def formula(household, period):
        return household.nb_persons()


class revenu_non_salarie_total(Variable):
    value_type = float
    entity = entities.Person
    definition_period = YEAR
    label = "Revenu non salarié total"

    def formula(person, period):
        return person("revenu_informel_non_salarie", period) + person(
            "revenu_non_salarie", period
        )


class secteur_activite(Variable):
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "Secteur d'activité de l'individu"
    # [Actif agricole < Salarie/dependant formel < Salarie/dependant informel <Independant]


class secteur_formel(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "Secteur formel"


class secteur_public(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu est un salarié du secteur public"


class survey_income(Variable):
    value_type = float
    entity = entities.Household
    definition_period = YEAR
    label = "Revenus produits par l'enquête"

    def formula(household, period):
        return (
            household("autoconsumption", period)  # "rev_i_autoconsommation"
            + household.sum(household.members("other_income", period))  # "rev_i_autres"
            + household.sum(
                household.members("gifts_sales_durables", period)
            )  # "rev_i_autres_transferts"
            + household("imputed_rent", period)  # "rev_i_loyers_imputes"
            + household("direct_transfers", period)  # "rev_i_transferts_publics"
            + household.sum(
                household.members("revenu_agricole", period)
            )  # "rev_i_agricoles"
            + household.sum(
                household.members("autres_revenus_du_capital", period)
            )  # "rev_i_autres_revenus_capital"
            + household.sum(
                household.members("revenu_informel_non_salarie", period)
            )  # "rev_i_independants_Ntaxe"
            + household.sum(
                household.members("revenu_non_salarie", period)
            )  # "rev_i_independants_taxe"
            + household.sum(
                household.members("revenu_locatif", period)
            )  # "rev_i_locatifs"
            + household.sum(
                household.members("pension_retraite", period)
            )  # "rev_i_pensions"
            + household.sum(
                household.members("salaire", period)
            )  # "rev_i_salaires_formels"
            + household.sum(
                household.members("revenu_informel_salarie", period)
            )  # "rev_i_salaires_informels"
        )


class urbain(Variable):
    value_type = bool
    entity = entities.Person
    definition_period = YEAR
    label = "L'individu vit en milieu urbain (par opposition à rural)"


# For matching with original data


class hh_id(Variable):
    value_type = int
    entity = entities.Household
    definition_period = YEAR
    label = "hh_id"


class pers_id(Variable):
    value_type = int
    entity = entities.Person
    definition_period = YEAR
    label = "pers_id"


# Variables d'enquête de l'étude, injectées dans le framework générique du cœur.
AFRIQUE_OUEST_SURVEY_VARIABLES = [
    revenu_non_salarie_total,
    cadre,
    categorie_cgu,
    labor_type,
    secteur_public,
    secteur_activite,
    secteur_formel,
    survey_income,
    urbain,
    number_of_people_per_household,
    hh_id,
    pers_id,
]


class ceq(Reform):
    name = "CEQ enhanced tax and benefit system"

    def apply(self):
        add_ceq_framework(
            self,
            harmonized_income_mapping=non_ceq_input_by_harmonized_variable,
            custom_variables=multi_country_custom_ceq_variables,
            extra_variables=AFRIQUE_OUEST_SURVEY_VARIABLES,
        )
        assert self.legislation_country is not None
        add_ceq_education_unit_cost(
            self, unit_cost_by_category_by_country[self.legislation_country]
        )
