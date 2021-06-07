DJANGO_SUPERUSER_USERNAME ?= admin
DJANGO_SUPERUSER_PASSWORD ?= admin
DJANGO_SUPERUSER_EMAIL ?= admin@site.example

all: install
.PHONY: all

install:
	poetry install
.PHONY: install

full-setup: createsuperuser
.PHONY: full-setup

makemigrations: install
	poetry run python manage.py makemigrations
.PHONY: makemigrations

migrate: install makemigrations
	poetry run python manage.py migrate
.PHONY: migrate

createsuperuser: migrate
	@echo "Creating superuser '$(DJANGO_SUPERUSER_USERNAME)':'*****' with email: '$(DJANGO_SUPERUSER_EMAIL)'"

	@echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$(DJANGO_SUPERUSER_USERNAME)', '$(DJANGO_SUPERUSER_EMAIL)', '$(DJANGO_SUPERUSER_PASSWORD)')" | poetry run python manage.py shell
.PHONY: createsuperuser

runserver:
	poetry run python manage.py runserver
.PHONY: runserver

test:
	poetry run pytest
.PHONY: test

unittest: unittest-blog
.PHONY: unittest

unittest-blog:
	poetry run pytest $(subst unittest-,,$@) --pdb
.PHONY: unittest-blog

functest:
	poetry run pytest test_functional.py --pdb
.PHONY: functest

clean-all: clean-db clean-venv
.PHONY: clean-all

clean-db:
	[ ! -e db.sqlite3 ] || rm db.sqlite3
.PHONY: clean-db

clean-venv:
	[ ! -e .venv ] || rm -r .venv
.PHONY: clean-venv
