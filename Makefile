test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .

setup:
	pipenv install --dev pylint
	pipenv install --dev black isort
	pre-commit install
