# Données

## Les enquêtes ne sont pas versionnées

Les enquêtes harmonisées CEQ-Afrique (fichiers Stata `.dta` de dépenses, revenus et
taxes indirectes) **ne sont pas incluses dans ce dépôt**. Elles sont chargées depuis
un emplacement local déclaré via `openfisca-survey-manager`.

Sans ces données, les tests d'intégration et les scénarios de simulation sont ignorés.

Pour le détail des variables et des tables attendues par pays, voir
[Description des tables d'entrée](description_donnees_input.md).

## Configuration `openfisca-survey-manager`

La configuration se fait dans le fichier `raw_data.ini` de `openfisca-survey-manager`
(typiquement `~/.config/openfisca-survey-manager/raw_data.ini`).

### Section `[ceq]`

Paramètres transverses à l'étude :

- `consumption_items_directory` : répertoire des nomenclatures de produits de
  consommation (COICOP harmonisées).
- `targets_file` : fichier des cibles macroéconomiques (revenus, taxes) utilisées
  pour la calibration.
- `country_codes` : correspondance pays → code ISO, p. ex.
  `senegal:SEN,mali:MLI,cote_d_ivoire:CIV`.

### Sections par pays

Une section par pays pointe vers les fichiers d'enquêtes `.dta` correspondants :

- `[senegal]`
- `[mali]`
- `[cote_d_ivoire]`

### Exemple indicatif

```ini
[ceq]
consumption_items_directory = /chemin/vers/nomenclatures
targets_file = /chemin/vers/cibles.xlsx
country_codes = senegal:SEN,mali:MLI,cote_d_ivoire:CIV

[senegal]
# chemins vers les fichiers .dta dépenses / revenus / taxes du Sénégal

[mali]
# chemins vers les fichiers .dta dépenses / revenus / taxes du Mali

[cote_d_ivoire]
# chemins vers les fichiers .dta dépenses / revenus / taxes de Côte d'Ivoire
```

!!! warning "Local uniquement"
    Ces chemins et ces données restent strictement locaux. Aucun fichier d'enquête
    n'est versionné dans ce dépôt.
