.PHONY: help build up down restart logs clean test frontend-install backend-install

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker containers
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: down up ## Restart all services

logs: ## View logs from all services
	docker-compose logs -f

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-scraper: ## View scraper logs
	docker-compose logs -f scraper

clean: ## Remove all containers, volumes, and images
	docker-compose down -v --rmi all

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-dev: ## Run frontend in development mode
	cd frontend && npm run dev

backend-install: ## Install backend dependencies
	cd backend && pip install -r requirements.txt

backend-migrate: ## Run Django migrations
	docker-compose exec backend python manage.py migrate

backend-makemigrations: ## Create Django migrations
	docker-compose exec backend python manage.py makemigrations

backend-shell: ## Open Django shell
	docker-compose exec backend python manage.py shell

backend-createsuperuser: ## Create Django superuser
	docker-compose exec backend python manage.py createsuperuser

scraper-run: ## Run the scraper manually
	docker-compose run --rm scraper

test: ## Run all tests
	cd frontend && npm test
	cd backend && python manage.py test

lint: ## Run linters
	cd frontend && npm run lint
	cd backend && flake8 .

format: ## Format code
	cd backend && black .

ps: ## Show running containers
	docker-compose ps

exec-frontend: ## Execute shell in frontend container
	docker-compose exec frontend sh

exec-backend: ## Execute shell in backend container
	docker-compose exec backend bash

exec-scraper: ## Execute shell in scraper container
	docker-compose run --rm scraper bash
