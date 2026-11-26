# Validation : génération des notebooks calculés (SN / ML / CI)

> But : avant de pousser ce dépôt études et avant de brancher le core 2.0 dans ceq-tunisie,
> reproduire la génération automatique des notebooks calculés **depuis des données locales
> externes** (les données ne sont PAS versionnées dans les dépôts).

## Mécanisme de génération (hérité d'openfisca-ceq)

- `make notebook-<pays>` → `papermill -p country <pays> notebooks/test.ipynb notebooks/<pays>.ipynb`
  (pays ∈ {cote_d_ivoire, mali, senegal}).
- `make notebook-results` → `jupyter nbconvert --execute --inplace notebooks/results.ipynb`.
- `test.ipynb` appelle `build_ceq_survey_scenario(legislation_country, year)`
  (`openfisca_ceq/tools/survey_scenario.py`), qui lit les données via
  `openfisca_ceq/tools/data/__init__.py` :
  - config : `~/.config/openfisca-survey-manager/raw_data.ini` (ou `$XDG_CONFIG_HOME`).
  - par pays, clés attendues : `consommation_<année>`, `revenus_harmonises_<année>`.
  - années : cote_d_ivoire=2014, mali=2011, senegal=2011.
- L'indirect (`tools/indirect_taxation/consumption_items_nomenclature.py`) lit
  `Produits_<CODE>.xlsx` dans un `consumption_items_directory` (section `[ceq]` de
  `config.ini` de survey-manager).

## Pré-requis externes (données HORS dépôt) — à fournir pour reproduire

1. Fichiers d'enquête harmonisés SN/ML/CI (consommation + revenus harmonisés) + entrées
   correspondantes dans `raw_data.ini` (`[senegal]`, `[mali]`, `[cote_d_ivoire]`).
2. Nomenclature produits COICOP : `Produits_*.xlsx` + section `[ceq]`
   `consumption_items_directory` dans `config.ini`.
3. Packages pays installés : `openfisca-senegal` (branche `ceq`), `openfisca-mali`,
   `openfisca-cote-d-ivoire`.
4. Dépendances notebooks : `papermill`, `jupyter`, `matplotlib`.

## RÉSULTAT (2026-11-26) : notebooks régénérés de bout en bout ✓

Les 3 notebooks (`senegal`, `mali`, `cote_d_ivoire`) s'exécutent via papermill **sans
aucune erreur**, agrégats cohérents (ceq_aggregates, Md monnaie locale) :

| variable | SEN | MLI | CIV |
|---|---|---|---|
| market_income | 5410 | 2160 | 10325 |
| net_market_income | 5204 | 2133 | 10233 |
| pensions | 59 | 0 (var. absente) | 354 |
| direct_taxes | 162 | 7 | 179 |

### Données locales branchées (hors dépôt) — `~/.config/openfisca-survey-manager/raw_data.ini`

```ini
[ceq]
consumption_items_directory = /home/benjello/Dropbox/Projet_Micro_Sim/wip/harmonisation_enquete-coicop
targets_file = /home/benjello/Dropbox/Projet_Micro_Sim/wip/harmonisation_fiscalite/recettes_fiscales_3P_ASR.xlsx

[senegal]
consommation_2011 = .../Projet_Micro_Sim/resultats/TaxeIneq_prdt_SEN.dta
revenus_harmonises_2011 = .../Projet_Micro_Sim/resultats/TaxeIneq_inc_harm_SEN.dta
[mali]       # idem *_MLI.dta, annee 2011
[cote_d_ivoire]  # idem *_CIV.dta, annee 2014
```
(`targets_file` = feuille `calage`, colonnes iso/year/DESC_3/montant.)

### Packages pays
`openfisca-senegal@ceq`, `openfisca-mali@master`, `openfisca-cote-d-ivoire@master`
installés en `--no-deps` (compatibles openfisca-core 44). + `openpyxl`, `ipykernel`.

### Correctifs de code requis (migration survey-manager 6.2 + bug pré-existant)
1. `tools/survey_scenario.py` : `set_tax_benefit_systems({"baseline": tbs})` (dict nommé) ;
   `self.period = year` ; propriété compat `tax_benefit_system` -> `tax_benefit_systems["baseline"]` ;
   override `compute_pivot_table` (auto-résout `simulation=None`) ; `self.simulations["baseline"]`
   dans `reach_target`.
2. `tools/tax_benefit_system_ceq_completion.py` (**core**) : bug pré-existant dans
   `add_ceq_education_unit_cost` — les valeurs lues n'étaient pas liées aux noms de
   l'expression numexpr. Corrigé via un `local_dict` explicite
   (`ne.evaluate(expr, local_dict={"niveau": …, "public": …})`).

Reports effectués : `survey_scenario.py` -> ce dépôt études ; le correctif éducation
-> **commité sur `openfisca-ceq` master** (`819eae5`, bugfix autonome) dont hérite la
branche `scission-core`.

## État initial constaté le 2026-11-26 (avant branchement)

- `raw_data.ini` : sections présentes = `dsf`, `paraguay`, `enbcv`. **Aucune** section
  SN/ML/CI.
- `/home/benjello/data/` : aucune donnée SN/ML/CI.
- `config.ini` : **pas** de section `[ceq]` / `consumption_items_directory`.
- Packages pays : `openfisca_senegal`, `openfisca_mali`, `openfisca_cote_d_ivoire` **absents**.

**Conclusion** : la reproduction des notebooks calculés est **bloquée par l'absence de
données et de packages pays en local** (blocage externe, pas de code à écrire). Options :
(a) fournir les données + packages pour une validation complète ; (b) se rabattre sur une
validation *mécanique* (import du dépôt, câblage papermill, tout sauf l'exécution data).

## Reste à faire (backlog scission)

- **Phase 4 — ceq-tunisie** (quand le cœur 2.0 sera publié/adopté) :
  - relock sur `openfisca-ceq >= 2.0` ;
  - corriger `tests/unit/test_openfisca_ceq_import.py` : il importe
    `openfisca_ceq.tools.data_ceq_correspondence` (module parti aux études en 2.0) —
    le repointer sur un module du cœur (p. ex. vérifier le chargement des 72 variables).
  - Impact code attendu : nul (ceq-tunisie ne consomme que `CountryTaxBenefitSystem`).
- **Publication / push** (non fait, décision à prendre) :
  - `openfisca-ceq` : la scission vit sur la branche `scission-core` (PR + merge + release 2.0.0) ;
  - `openfisca-ceq-afrique-ouest` : dépôt local sans remote (créer le dépôt GitHub + push) ;
  - figer `uv.lock` côté études.
- **Générateur indirect** (`tools/indirect_taxation/consumption_items_nomenclature.py`, cœur) :
  code encore `country_code_by_country` (MLI/SEN/CIV) en dur — à paramétrer (pays + chemin)
  pour un cœur pleinement agnostique.
- **Packages pays** : installés depuis GitHub en `--no-deps` (`openfisca-senegal@ceq`,
  `-mali@master`, `-cote-d-ivoire@master`, compat core 44) — à déclarer/épingler proprement.

## Changements d'environnement effectués (machine benjello)

- `~/.config/openfisca-survey-manager/raw_data.ini` : sauvegarde `.bak-scission` ; ajout
  des sections `[ceq]` (`consumption_items_directory`, `targets_file`), `[senegal]`,
  `[mali]`, `[cote_d_ivoire]`.
- Kernels Jupyter installés : `ceq-venv`, `ceqao-venv`.
- Commits : cœur `openfisca-ceq` master `819eae5` (bugfix éducation) ; branche
  `scission-core` `351fd25` (API générique) + `4dc274c` (élagage + 2.0.0) ;
  dépôt études `fc167ee` (restructure) + `.gitignore`.
