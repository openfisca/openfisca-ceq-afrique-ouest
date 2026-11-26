# Pipeline de simulation

Cette page décrit comment un scénario d'enquête CEQ est construit pour un pays
d'Afrique de l'Ouest, et l'état connu du pipeline.

## Vue d'ensemble

Le point d'entrée est la fonction
[`build_ceq_survey_scenario`][openfisca_ceq_afrique_ouest.survey_scenario.build_ceq_survey_scenario]
du module `openfisca_ceq_afrique_ouest.survey_scenario` :

```python
from openfisca_ceq_afrique_ouest.survey_scenario import build_ceq_survey_scenario

scenario = build_ceq_survey_scenario("senegal", year=2011)
```

Elle enchaîne les étapes suivantes :

1. **Chargement paresseux du système socio-fiscal pays.**
   `country_tax_benefit_system_class(legislation_country)` importe à la demande le
   package pays (`openfisca-senegal`, `openfisca-mali` ou `openfisca-cote-d-ivoire`).
   Seul le pays demandé est importé : on peut travailler avec un seul package pays
   installé.

2. **Greffe du framework CEQ.** `ceq(CountryTaxBenefitSystem())` applique la réforme
   `ceq` du module `ceq_framework.py`. Cette réforme ajoute les variables
   d'enquête propres à l'étude (`cadre`, `labor_type`, `secteur_*`, `survey_income`,
   …) puis délègue au cœur via
   `openfisca_ceq.tools.tax_benefit_system_ceq_completion.add_ceq_framework`, qui
   injecte les concepts CEQ génériques (revenus de marché, transferts, etc.).

3. **Ajout des produits de consommation** (`add_coicop_item_to_tax_benefit_system`)
   et, optionnellement, d'une variable `consumable_income`
   (`adjust_indirect_taxation=True`).

4. **Chargement des données** d'enquête (`build_ceq_data`) : dépenses, revenus,
   cibles, via les chargeurs de `data/`.

5. **Construction du scénario** `CEQSurveyScenario` (sous-classe
   d'`AbstractSurveyScenario`) et, optionnellement, inflation vers les cibles de
   valeur ajoutée brute et de consommation (`inflate=True`).

## API côté cœur : `ceq` / `add_ceq_framework`

- `ceq` (dans ce dépôt, `ceq_framework.py`) est une réforme OpenFisca qui
  **câble** les variables d'enquête concrètes de l'étude.
- `add_ceq_framework` (dans le cœur `openfisca-ceq`) est l'API **générique** qui
  greffe les concepts CEQ sur un système socio-fiscal pays.

!!! note "Garde-fou"
    `add_ceq_framework` refuse un système socio-fiscal contenant déjà les variables
    CEQ calculées : il s'applique au système d'un *package pays*
    (openfisca-senegal / -mali / -cote-d-ivoire), pas au paquet CEQ lui-même.

Validation connue (voir `documentation/backlog.md`) : `ceq(SenegalTBS)` greffe
97 variables (19 → 116) ; `market_income`, `education_net_transfers`,
`health_net_transfers` et `in_kind_transfers` se calculent et sont conformes.

## État connu : run complet bloqué

!!! warning "Bloquant — dérive d'API openfisca-survey-manager"
    Le **run complet** du pipeline est actuellement **bloqué** par une dérive d'API
    d'`openfisca-survey-manager`. D'après `documentation/backlog.md` :

    - avec survey-manager 6.2 (tiré par le cœur 2.0), le module
      `openfisca_survey_manager.scenarios` est **déprécié** (→ `policy.scenarios`) ;
    - `set_tax_benefit_systems` prend désormais un **dict** `{nom: tbs}` ;
    - le flux d'initialisation (`init_from_data`) est réécrit.

    `CEQSurveyScenario` est écrit contre l'ancienne API et **casse à la
    construction** (après chargement réussi des `.dta`). Ce chantier de
    modernisation est **orthogonal** à la scission cœur/études.

    **Vérifié jusque-là** : la greffe CEQ, le chargement des `.dta` et la lecture des
    nomenclatures fonctionnent ; seul le wrapper de scénario reste à adapter. Une
    fois `CEQSurveyScenario` modernisé, `build_ceq_survey_scenario("senegal",
    year=2011)` doit calculer et comparer aux cibles.
