.PHONY: help install test run docker-build docker-up docker-down k8s-apply

help:
	@echo "🛠️ FastAPI DevOps Control Center"
	@echo "-----------------------------------"
	@echo "  make install        Install Python dependencies"
	@echo "  make test           Run Pytest suite"
	@echo "  make run            Run local development server"
	@echo "  make docker-build   Build production Docker container"
	@echo "  make docker-up      Start FastAPI + Postgres with Docker Compose"
	@echo "  make docker-down    Stop Docker Compose containers"
	@echo "  make k8s-apply      Deploy all Kubernetes manifests"

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest -v tests/

run:
	uvicorn app.main:app --reload --port 8000

docker-build:
	docker build -t simple-fastapi-api:latest .

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

k8s-apply:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/secret.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/postgres.yaml
	kubectl apply -f k8s/api.yaml
