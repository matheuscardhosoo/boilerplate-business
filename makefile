all:
	poetry run isort src/ tests/
	poetry run black src/ tests/
	poetry run flake8 src/ tests/
	poetry run mypy src/ tests/ --install-types --non-interactive --show-error-codes
	poetry run pylint src/ tests/
	poetry run coverage run --source="src/" --module pytest tests/
	poetry run coverage report --show-missing

pre_commit:
	pre-commit install
	pre-commit autoupdate

requirements:
	poetry export -f requirements.txt > requirements.txt --without-hashes

run:
	export CONFIG_PATH="containers/system_configuration.yaml" && \
	poetry run gunicorn -w 3 -k uvicorn.workers.UvicornWorker --timeout 7000 --preload --capture-output --chdir src main:app

debug:
	export CONFIG_PATH="src/containers/system_configuration.yaml" && \
	poetry run uvicorn --host 127.0.0.1 --port 8000 --reload --log-level debug --app-dir src main:app
