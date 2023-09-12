# SWD Django Demo

The project can be used as a reference for the SWD lab course.
This project consists of several apps with a focus on loose coupling and dependency injection.
A good article about separation of concerns in Django projects can be found `https://emcarrio.medium.com/business-logic-in-a-django-project-a25abc64718c`.
Good Django tutorials can be found `https://www.djangoproject.com/start/` or `https://cs50.harvard.edu/web/2020/weeks/3/`.

## Installation

1. Clone the repository. `git clone https://its-git.fh-salzburg.ac.at/SWD/djangodemo.git`
2. Install Poetry: `https://python-poetry.org/docs/#installation`
   - Mac/Linux: `curl -sSL https://install.python-poetry.org | python3 -`
   - Windows (Powershell): `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
 
## Usage

1. Install dependencies within the projects main directory: `poetry install`.
   If you run into an error like "failed to query /usr/bin/python ... invalid syntax", then poetry is run using python 2. Tell poetry which python version to use: `poetry env use python3.11`
2. Activate the virtual environment: `poetry shell`.
3. Create the database tables: `python manage.py migrate`
4. Create an admin user: `python manage.py createsuperuser`
5. Run unit tests: `python manage.py test -v 2`
6. Run the development server: `python manage.py runserver`.
7. Open the website in your browser: `http://localhost:8000/admin`, `http://localhost:8000/products`.

## Dependency Injection

This project uses the python dependency injection module, which is not part of Django itself.
`https://python-dependency-injector.ets-labs.org/examples/django.html`



