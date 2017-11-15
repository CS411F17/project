# CS411F17 Project

We'll be using [Django](https://www.djangoproject.com/) for our project, running Python 3.6

## Setting up a development environment

This is the Entity Relationship Diagram
![Alt text](https://github.com/CS411F17/project/master/ERD.png "Title")

### macOS

1. [Install Git](http://git-scm.com/download/mac) if you haven't done so already
2. Clone this repo using `git clone git@github.com:CS411F17/project.git`
3. [Get Python 3.6](https://docs.djangoproject.com/en/1.11/intro/install/#install-python) for your specific OS
4. Install [virtualenv](https://virtualenv.pypa.io/en/stable/); this is to avoid conflict package versions between your system python and the packages we're using for the project. Here's a good [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) from Kenneth Reitz
5. Once you've finished 4,  run `mkvirtualenv cs411-project -p /path/to/your/python3`
6. `cd` into this project repo
7. Run `pip install -r requirements.txt`; this will install all of the packages, pinned to a specific version, within the requirements file.
8. Migrate the databse schema to a sqlite file using `python manage.py migrate`
9. Run `python manage.py runserver`; your Python app will then run on `localhost:8000` in your browser

### Windows

1. [Install Git](http://git-scm.com/download/win) if you haven't done so already; it runs using [MINGW64](http://www.mingw.org/)
2. Open Git Bash
3. Clone this repo using `git clone git@github.com:CS411F17/project.git`
4. [Get Python 3.6](https://docs.djangoproject.com/en/1.11/intro/install/#install-python) for your specific OS
5. Install [virtualenv](https://virtualenv.pypa.io/en/stable/); this is to avoid conflict package versions between your system python and the packages we're using for the project. Here's a good [guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) from Kenneth Reitz
6. Once you've finished 4,  run `mkvirtualenv cs411-project -p /path/to/your/python3`
7. To workon the virtualenv, run `source /path/to/virtualenv/Scripts/activate`
8. `cd` into this project repo
9. Run `pip install -r requirements.txt`; this will install all of the packages, pinned to a specific version, within the requirements file.
10. Migrate the databse schema to a sqlite file using `python manage.py migrate`
11. Run `python manage.py runserver`; your Python app will then run on `localhost:8000` in your browser
