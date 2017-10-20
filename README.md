# CS411F17 Project

We'll be using [Django](https://www.djangoproject.com/) for our project, running Python 3.4

## Setting up a development environment

1. [Get Python 3](https://docs.djangoproject.com/en/1.11/intro/install/#install-python)
2. Install [virtualenv](https://virtualenv.pypa.io/en/stable/); this is to avoid conflict package versions between your system Python and the packages we're using for the project.
3. Once you've finished 2,  run `mkvirtualenv cs411-project -p /path/to/your/python3` 
4. Run `pip install -r requirements.txt`; this will install all of the packages, pinned to a specific version, within the requirements file.
5. [Setup a database](https://docs.djangoproject.com/en/1.11/topics/install/#database-installation)
6. Edit your `db_settings.py` and change the `db_url` to point to your local copy of PostgreSQL
7. Run `python manage.py runserver`; your Python app will then run on `localhost:8000` in your browser
8. Done!