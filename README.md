# CU There

`CS 4300` final project

am2269, ac962, jma353, dl743

## Live App!

[HERE!](http://cu-there.herokuapp.com/)

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


### Data Collection

To collect event JSON data, use the following:

````bash
$ python data_collection/get_data.py <num_years>
````

where `<num_years>` is an optional argument representing the number of years of data you wish to obtain (for example, 3 or 0.67). If no `<num_years>` argument is provided, the script will obtain 7 years of data. The script processes data at a rate of approximately 3 seconds per day of data (which is about 18 minutes per data-year).

This will store events in a collection of JSON files. To combine these files, run

````bash
$ python data_collection/consolidate.py
````

When running `get_data.py`, you may encounter an error such as this one:

````
Traceback (most recent call last):
  File "data_collection/get_data.py", line 1, in <module>
    from app import EventSearch
ImportError: No module named app
````

To fix this, run the following:

````bash
$ export PYTHONPATH=${PYTHONPATH}:/path/to/cu-there
````

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

## Configure front end
`cd` into the `front` directory. Install all dependencies with:

````bash
npm install
````

### Development
Run the webpack dev server with:

````bash
npm run dev
````

### Production

`Heroku` is used for this project's production environment.

`Webpack` must be run locally so it is pushed to `Heroku`

````bash
git checkout heroku
git merge master
cd front
webpack
cd ..
git add .
git commit -m "Heroku push"
git push -f heroku heroku:master
git checkout master
````
