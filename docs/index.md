# OpenFisca CEQ — Études Afrique de l'Ouest

Études [Commitment to Equity (CEQ)](http://commitmentoequity.org) pour la **Côte
d'Ivoire**, le **Mali** et le **Sénégal**, bâties sur le cœur réutilisable
[openfisca-ceq](https://github.com/openfisca/openfisca-ceq) (≥ 2.0).

Ce dépôt a été extrait d'`openfisca-ceq` (avec son historique) lors de la scission
cœur / études de la version 2.0 : le cœur ne contient plus que les entités, les
variables de concepts CEQ et le framework générique de complétion ; les trois
études pays (notebooks, chargeurs de données d'enquêtes, scénarios de simulation,
calibration, résultats, correspondances de données) vivent désormais ici.

!!! note "Tunisie"
    La Tunisie est modélisée séparément dans
    [ceq-tunisie](https://github.com/openfisca/ceq-tunisie), qui ne consomme que le
    cœur.

## Écosystème

- **Cœur réutilisable** : [openfisca/openfisca-ceq](https://github.com/openfisca/openfisca-ceq)
  — entités, concepts CEQ, framework générique de complétion (`add_ceq_framework`).
- **Études Afrique de l'Ouest** (ce dépôt) : Côte d'Ivoire, Mali, Sénégal.
- **Étude Tunisie** : [openfisca/ceq-tunisie](https://github.com/openfisca/ceq-tunisie).

## Contenu

- `notebooks/` : notebooks des trois pays (`senegal`, `mali`, `cote_d_ivoire`) et
  utilitaires (`example`, `export`, `results`, `test`). Voir [Notebooks](notebooks.md).
- `openfisca_ceq_afrique_ouest/` : chargeurs de revenus/dépenses/cibles
  (`data/`), scénario d'enquête multi-pays (`survey_scenario.py`), calibration,
  résultats (`results/`), correspondances de données (`data_ceq_correspondence.py`).
- `openfisca_ceq_afrique_ouest/assets/` : coûts unitaires d'éducation, nomenclatures
  COICOP fusionnées.
- `openfisca_ceq_afrique_ouest/tests/` : tests d'intégration dépendant des données.

## Données

Les enquêtes harmonisées CEQ-Afrique (fichiers Stata `.dta`) **ne sont pas
versionnées**. Voir [Données](donnees/index.md) pour la configuration
`openfisca-survey-manager` attendue, et la
[description des tables d'entrée](donnees/description_donnees_input.md).

## Installation

```sh
uv sync --extra dev
```

Pour construire cette documentation :

```sh
uv sync --extra docs
mkdocs serve
```

## Licence

Ce dépôt est distribué sous licence [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html).
