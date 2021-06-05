# A blog based on the DjangoGirls tutorial

## Installation and Setup

Installation requires Python and Poetry

The following steps will install dependencies including development
dependencies, and complete the basic database setup:

```shell
poetry install
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser --username=admin --email=admin@site.example
```

## Development

Running the development server:

```shell
poetry run python manage.py runserver
```

Running all tests requires the development server to be running:

```shell
poetry run pytest 
```
