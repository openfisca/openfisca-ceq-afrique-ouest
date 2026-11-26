# Notebooks

Les notebooks de ce dépôt (`notebooks/`) servent à explorer les données, construire
les scénarios pays et produire les résultats. Ils **ne sont pas exécutés** lors de la
construction de cette documentation (ils dépendent de données d'enquêtes non
versionnées — voir [Données](donnees/index.md) — et du pipeline encore partiellement
bloqué, voir [Pipeline](pipeline.md)).

Leurs imports ont été réadaptés au package `openfisca_ceq_afrique_ouest`
(+ `labor_type_by_index` depuis `ceq_framework`) ; les imports cœur sont
conservés et le JSON est valide. Leur **exécution** reste à faire (bloquée par la
dérive survey-manager et par la disponibilité des packages pays Mali / Côte d'Ivoire).

## Notebooks pays

| Notebook | Rôle |
| --- | --- |
| [`senegal.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/senegal.ipynb) | Construction et analyse du scénario CEQ Sénégal (65 cellules). |
| [`mali.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/mali.ipynb) | Construction et analyse du scénario CEQ Mali (65 cellules). |
| [`cote_d_ivoire.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/cote_d_ivoire.ipynb) | Construction et analyse du scénario CEQ Côte d'Ivoire (65 cellules). |

## Notebooks utilitaires

| Notebook | Rôle |
| --- | --- |
| [`example.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/example.ipynb) | Exemple minimal d'utilisation de l'API (`build_ceq_survey_scenario`). |
| [`export.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/export.ipynb) | Export des données / résultats. |
| [`results.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/results.ipynb) | Agrégation et présentation des résultats (inégalités, taxes). |
| [`test.ipynb`](https://github.com/openfisca/openfisca-ceq-afrique-ouest/blob/master/notebooks/test.ipynb) | Notebook de mise au point / vérifications. |

!!! note "Rendu dans la documentation"
    Le plugin `mkdocs-jupyter` est déclaré dans l'extra `docs` et permet de rendre
    les notebooks (`execute: false`) si on les ajoute au `nav`. Ils sont ici
    simplement listés et liés pour garder la documentation légère et ne pas dupliquer
    des sorties lourdes ; voir le dépôt pour les ouvrir.
