# Makefile commands to fast run

help h:
	@printf "[HELP]\n"
	@printf "Commands:\n"
	@printf "	start: start assembled containers and show logs.\n"
	@printf "	run: build containers and run.\n"
	@printf "	rerun: stop, rebuild containers to set changes and run again.\n"
	@printf "	build: assemble project to run.\n"
	@printf "	down: stop and remove docker containers.\n"
	@printf "	stop: stop docker containers.\n"
	@printf "	logs: show docker compose logs or if set a target shows logs from target container.\n"
	@printf "	linter: run installed linter (as default set mypy)"
	@printf "	env-up/env-down: startup or shutdown development container (use for database or cache in container\n"
	@printf "	local-run: run application\n"
	@printf "	migrate: make django migrations\n"
	@printf "   test: run application tests"


start: up logs

run: linter build up

rerun: down run

build:
	@docker compose build

up:
	@docker compose up -d

down:
	@docker compose down

stop:
	@docker compose stop

logs:
	@docker compose logs -f

linter: # correct path to virtual environment directory if needs
	@source .venv/bin/activate && python3 -m mypy app

env-up:
	@docker compose -f dev/docker-compose.dev.yaml --env-file dev/.env up -d

env-down:
	@docker compose -f dev/docker-compose.dev.yaml --env-file dev/.env down

local-run:
	@source .venv/bin/activate && cd app/ && python3 manage.py runserver

migrate:
	@source .venv/bin/activate && cd app/ && python3 manage.py makemigrations && python manage.py migrate

test:
	@source .venv/bin/activate && cd app/ && python3 manage.py test
