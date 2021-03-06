# CU There

`CS 4300` final project

`am2269, ac962, jma353, dl743`

`CU There` utilizes historic Cornell University event data from Facebook
to help users optimize their event planning efforts.  

This project won the [`Cornell BOOM 2017 Statistics Award`](https://boom.cornell.edu/students-and-faculty/awards/).

## Live App!

Check it out [`here!`](http://cu-there.herokuapp.com/)

## Server Configuration

### Virtual Environment Setup
Run the following arguments to setup the virtual environment necessary to maintain packages

````bash
[sudo] pip install virtualenv # to update virtualenv
virtualenv venv # to create virtualenv
````

Once the `venv` is created, you can activate it by running the following:

````bash
source venv/bin/activate
````

Once you have activated `venv`, run the following to install all package requirements

````bash
pip install -r requirements.txt
````

At this point, if you run `pip freeze`, **only** packages in `requirements.txt` should be shown.

### Database Setup
This app uses `PostgreSQL` (or `Postgres`). `Postgres` can be installed a multitude of ways, but if you’re on `OSX` I recommend utilizing the [`Postgres App`](https://postgresapp.com/).

Once you have Postgres setup and have your [`$PATH`](https://postgresapp.com/documentation/cli-tools.html) configured accordingly, run the following:

````bash
# Enter postgres command line interface
$ psql
# Create your database
CREATE DATABASE cu_there_db;
# Quit out
\q
````

### Autoenv
For environment variable loading, we run [`autoenv`](https://github.com/kennethreitz/autoenv)

To set this up, run the following:

````bash
deactivate # if you're running your venv
pip install autoenv # to install if you haven't already installed it
touch .env
````

The `.env` file is where you can declare environment variables specific to this app.  These variables are loaded on `cd`-ing into the directory with the `.env` file.  Your `.env` file should look like this:

````bash
export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL=postgresql://localhost/cu_there_db
...
````

### Required Environment Variables

````bash
APP_SETTINGS
DATABASE_URL
FB_CLIENT_ID
FB_CLIENT_SECRET
EVENTBRITE_TOKEN
export PYTHONPATH=${PYTHONPATH}:pwd
````

### Migrating the DB
To migrate your local `DB`:

````bash
# Initialize migrations
python manage.py db init
# Create a migration
python manage.py db migrate
# Apply it to the DB
python manage.py db upgrade
````

## Client Configuration
`cd` into the `front` directory. Install all dependencies with:

````bash
npm install
````

### Development
Run the webpack dev server with:

````bash
npm run dev
````

## Production

* `Heroku` is used for this project's production environment.

* `Webpack` must be run locally so it is pushed to `Heroku`

* `Pickle` file must be generated locally to avoid preprocessing occurring on the `Heroku` server

````bash
git checkout heroku
git merge master
rm -r preprocessed.p
python remake_dill.py
cd front
webpack
cd ..
git add .
git commit -m "Heroku push"
git push --force heroku heroku:master
git checkout master
````
