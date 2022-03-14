As this program uses a database, there is a bit more initial setup involved.
 You'll need Postgres installed locally so that you can host the database when you are developing
 You will also need to get a database running on Heroku to store information. Heroku offers a free database that can store up to 10,000 rows

* First, install Postgres (https://www.robinwieruch.de/postgres-sql-macos-setup is a reasonable guide) and initdb

* Make sure you have the Python libraries we will need (check requirements.txt). Use PIP to install any missing ones
 (If you've been following along, you will need flask_heroku, SQLAlchemy, flask_SQLAlchemy, flask_compress, psycopg2 )

* Check to make sure your postgres db service is running by following a postgres tutorial

** You may need to set up an environment variable to tell SQLAlchemy where to find your database
  If you configured things using default settings, the following environment commands should work
  CAUTION: if you already use SQLAlchemy, this may wipe important settings
In a command line:
 for Mac: export SQLALCHEMY_DATABASE_URI=postgres://localhost
 for Win: SET SQLALCHEMY_DATABASE_URI=postgresql://localhost

**  DEPRECATED (THESE DETAILS ARE INCLUDED IN CASE OF OLDER ENVIRONMENTS  **
* Make sure you have set an environment variable for your database, DATABASE_URL
This is what Heroku uses to tell your app where the database lives, so you also need to have it on your own computer if you intend to run things locally
 for Mac: export DATABASE_URL=postgres://localhost
 for Win: SET DATABASE_URL=postgresql://localhost
(note, you may need to adjust this based on your local configuration. see https://stackoverflow.com/questions/19204548/how-do-you-connect-to-local-postgresql-in-heroku )
** END DEPRECATED **

* Code up your app.py

* Once you've made your new database class (such as Entry in the example code), you need to build the table within your own local database
The easiest way to do this is to run a python interpreter (e.g. python3 in the command line), then import your app and call db.create_all()
But first, if you created a SQLALCHEMY_DATABASE_URI environment variable, then import it using os.getenv()
For example, if you are in then project directory
 python3
 >> import os
 >> os.getenv('SQLALCHEMY_DATABASE_URI')
 >> from app import db
 >> db.create_all()
 
* If create_all() returns an error, it is likely because the path to your database in DATABASE_URL is incorrect, or postgres is not running. Check both of those things

* Now test app.py locally and see if it works as expected

* Now we need to do the same thing on Heroku
* First push all of your new files to a new Heroku app using git
  (Recall these commands:  git init
                           heroku create <PROJECT NAME, e.g. jmr395-info4310-hw1>
                            * add things to repo *
                           git push remote heroku master 
                           heroku ps:scale web=1
                           heroku open                    )

* The procfile can stay the same, but be sure to update your requirements.txt!

* Then create a free DB on Heroku (limit 10000 rows)
 heroku addons:create heroku-postgresql:hobby-dev -a APPNAMEHERE
 
* Finally, we run the Heroku equivalent of the create_all() command to build your database
First, access the python interpreter for your heroku dyno, then import your site and call create_all()
 heroku run python -a APPNAMEHERE
 >> from app import db
 >> db.create_all()
