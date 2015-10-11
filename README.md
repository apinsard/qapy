# Qapy

## Conventions / Guide Lines

- Text width for Python, JS and CSS files is **79** characters
- Text width for HTML files is **99** characters
- Python code must pass flake8 checks
- Python, JS and CSS files are indented with 4 spaces
- HTML files are indented with 2 spaces
- Please distinguish "display strings" and 'identifier-strings':
    - strings intended for display are delimited by double quotes
    - other strings are delimited by simple quotes.
- In Python, [prefer `format()` method over `%` syntax](http://stackoverflow.com/a/5082482/1529346)
- Imports should be in alphabetical order, grouped by:
    1. standard (os, sys, ...)
    2. django (django.core, django.contrib, ...)
    3. third-party (unipath, psycopg2, ...)
    4. qapy
- All files must be UTF-8 encoded
- Do not leave trailing whitespaces lying (thanks)

## Install

### Environment

- Python 3.4.3
- Pip 7.1.2
- PostgreSQL 9.4.5
- SASS 3.4.18
- CoffeeScript 1.9.3

Install python dependencies via pip:

```console
pip install -r requirements/dev.txt
```

Setup PYTHONPATH and DJANGO\_SETTINGS\_MODULE:

```console
PYTHONPATH="/path/to/the/project:/path/to/the/virtualenv/lib/python3.4"
DJANGO_SETTINGS_MODULE="qapy.settings.dev"
```

### Create the database

```console
createuser -P qapy
createdb -O qapy qapy
```

### Define secret settings

Create a file `secrets.json` at project's root:

```json
{
    "SECRET_KEY": "randomlyGeneratedSecretKey",
    "DB_USER": "qapy",
    "DB_PASSWD": "qapy",
}
```

### Sync the database

```console
django-admin migrate
```

### Run the server

```console
django-admin runserver
```

### Setup a git hook for flake8 (Optional)

```console
flake8 --install-hook
```
