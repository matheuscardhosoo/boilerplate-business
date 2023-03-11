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

build:
	docker build -t boilerplate-business .

run:
	docker run -it --mount source=boilerplate-business,target=/app boilerplate-business

debug:
	export CONFIG_PATH="src/containers/system_configuration.yaml" && \
	export ENV="test" && \
	export SERVICE_NAME="boilerplate-business" && \
	poetry run uvicorn --host 127.0.0.1 --port 8000 --reload --log-level debug --app-dir src main:app
