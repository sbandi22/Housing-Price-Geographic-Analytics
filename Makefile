.PHONY: install db ingest preprocess train dashboard report test lint clean docker-up docker-down

install:
	pip install -r requirements.txt

db:
	psql -U postgres -c 'CREATE DATABASE housing;' || true
	psql -U postgres -d housing -f sql/schema.sql
	psql -U postgres -d housing -f sql/seed.sql
	psql -U postgres -d housing -f sql/views.sql

ingest:
	python -m src.etl.ingest

preprocess:
	python -m src.etl.preprocess

train:
	python -m src.models.price_predictor

dashboard:
	python dashboards/app.py

report:
	python -m src.reports.report_generator

test:
	pytest tests/ -v --cov=src

lint:
	ruff check src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down -v
