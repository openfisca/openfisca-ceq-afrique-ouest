all: test

# Les notebooks lisent les données d'enquête HORS dépôt via la config
# openfisca-survey-manager (~/.config/openfisca-survey-manager/raw_data.ini).
# Voir documentation/validation-notebooks.md.

notebook-all: notebook-cote_d_ivoire notebook-mali notebook-senegal

notebook-cote_d_ivoire:
	rm -f notebooks/cote_d_ivoire.ipynb
	papermill -p country cote_d_ivoire notebooks/test.ipynb notebooks/cote_d_ivoire.ipynb

notebook-mali:
	rm -f notebooks/mali.ipynb
	papermill -p country mali notebooks/test.ipynb notebooks/mali.ipynb

notebook-senegal:
	rm -f notebooks/senegal.ipynb
	papermill -p country senegal notebooks/test.ipynb notebooks/senegal.ipynb

notebook-results:
	jupyter nbconvert --execute --to notebook --inplace notebooks/results.ipynb

check-style:
	ruff check openfisca_ceq_afrique_ouest

format-style:
	ruff format openfisca_ceq_afrique_ouest
	ruff check --fix openfisca_ceq_afrique_ouest

# Les tests nécessitent les données d'enquête locales (cf. documentation/).
test:
	pytest openfisca_ceq_afrique_ouest/tests
