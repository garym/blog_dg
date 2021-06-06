# A blog based on the DjangoGirls tutorial

## Installation and Setup

Installation requires Python and Poetry.

The following steps will install dependencies including development
dependencies, and complete the basic database setup:

```shell
poetry install
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser \
  --username=admin \
  --email=admin@site.example
```

## Development

For development purposes there is a shortcut for setup to allow things like
cleaning up of an sqlite database, and re-setting up:

To clean the db only:
```shell
make clean-db
```

The other `clean-venv` and `clean-all` targets will remove the poetry
environment which may not be desirable.

To install all the way to creating a superuser with an INSECURE admin
password:
```shell
make full-setup
```

The above is not idempotent in the sense that it will currently fail on the
final step if the admin user has already been created.

Running the development server:
```shell
make runserver
```

All tests can be run with:

```shell
make test
```
