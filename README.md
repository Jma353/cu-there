# CU There

`CS 4300` final project

## Virtual Environment Setup
Run the following arguments to setup the virtual environment necessary to maintain packages

```bash
[sudo] pip install virtualenv # to update virtualenv
virtualenv venv # to create virtualenv
```

Once the `venv` is created, you can activate it by running the following:

```bash
source venv/bin/activate
```

Once you have activated `venv`, run the following to install all package requirements

```bash
pip install -r requirements.txt
```

At this point, if you run `pip freeze`, **only** packages in `requirements.txt` should be shown.


## Database Setup
This app uses `PostgreSQL` (or `Postgres`). `Postgres` can be installed a multitude of ways, but if you’re on `OSX` I recommend utilizing the [`Postgres App`](https://postgresapp.com/).

Once you have Postgres setup and have your [`$PATH`](https://postgresapp.com/documentation/cli-tools.html) configured accordingly, run the following:

```bash
# Enter postgres command line interface
$ psql
# Create your database
CREATE DATABASE cu_there_db;
# Quit out
\q
```

## Autoenv
For environment variable loading, we run [`autoenv`](https://github.com/kennethreitz/autoenv)

To set this up, run the following:

```bash
deactivate # if you're running your venv
pip install autoenv # to install if you haven't already installed it
touch .env
```

The `.env` file is where you can declare environment variables specific to this app.  These variables are loaded on `cd`-ing into the directory with the `.env` file.  Your `.env` file should look like this:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/cu_there_db"
...
```

## Required Environment Variables

```
APP_SETTINGS
DATABASE_URL
FB_CLIENT_ID
FB_CLIENT_SECRET
```
