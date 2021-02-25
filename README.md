# FindYourNGO

## Quick Start
- check setup guide to get up the database
- run `docker-compose -f docker-compose.prod.yml up --scale worker=4` to start the system in production mode
- run docker-compose up (-d) in the root folder
- localhost:8000 should be usable immediately (this is where the API lives)
- localhost (:80) will take a while to run

Refer to https://docs.docker.com/compose/django/ for a quick overview of how the infrastructure was built.

RestAPI guide: https://www.django-rest-framework.org/tutorial/quickstart/

django-admin can be used inside the cli with docker-compose exec web /bin/bash


## Setup Guide
- start docker containers
- start console in server container
	- python manage.py makemigrations
	- python manage.py migrate
		- this updates the database's schemes
- go to localhost:8000/dataImport
	- this imports the data if the database is currently empty (meaning once it is imported, it doesn't do anything)

To clean the database, go to localhost:8000/clearDatabase.


### Development: Typing
Install the MyPy-Plugin and run its scan. Examples for how to type python code can be found in /Backend/data/import/european_council.


### Development: Resetting the database
In case of incompatible migrations / an out-of-date state of the database, it can be rest in the following way:
- Clear the database first
- execute shell in the web container
	- python manage.py showmigrations -- lists all previously applied migrations
	- python manage.py migrate --fake restapi zero -- undos the migrations
	- python manage.py showmigrations -- make sure that all migrations on restapi have been set to unapplied
- delete the migration files in the backend (make sure to not delete __init__.py)
- execute shell in the web container
	- python manage.py showmigrations -- make sure all restapi-migrations have disappeared from the list
	- python manage.py makemigrations -- re-make initial migration
	- python manage.py migrate -- apply the initial migration
	
	In case the DB complains that tables already exist, simply drop them manually.
	

In case this does not fix the problem, you can reset the entire database:
- manually drop all restapi-tables in the database (!! only the tables starting with restapi_ !!)
- reset migrations as described above
- run makemigrations, migrate to let it detect that the database is clean
- put the model classes back in
- run makemigrations, migrate again to setup the database


### Postgres

#### Make Postgres Persistent
If you are using Windows, there might be an issue with file permissions using a local directory as a volume.

Instead, manually create a docker volume via the command: docker volume create findyourngovolume
The data will then be persisted into this volume.


#### Access Postgres DB from outside of docker
Postgres in docker is mapped to port 5433 (not the default 5432, since this can clash with local installations of postgres). Open the database menu in PyCharm, click on '+', 'PostgreSQL', enter correct port, username (postgres) and password (postgres). Use the 'test connection' button to make sure it actually works.
Alternatively, you can also connect via pgAdmin.

### Django Background Tasks
All tasks that have to be performed periodically (recalculation of TW, recalculation of PageRank, ...) are managed via the
database-backed work queue 'Django Background Tasks'. This queue is processed by calling 'python manage.py process_tasks' 
(this happens automatically by starting the tasks container).
It is reset every time the server is restarted to avoid double processing of tasks. It can be reset manually by calling 
localhost:8000/clearBackgroundTasks.
The recalculation of the TW score and PageRank is performed hourly. 
Additional background tasks should be initialized in background_tasks.py.
Django Background Tasks Docs: https://django-background-tasks.readthedocs.io/

## Architecture

TODO
Refer to https://docs.docker.com/compose/django/ for a quick overview of how the infrastructure was built.
RestAPI guide: https://www.django-rest-framework.org/tutorial/quickstart/
django-admin can be used inside the cli with docker-compose exec web /bin/bash


### Functionality

#### Trustworthiness Calculation
Please refer to [this](./Backend/findyourngo/README.md) document.



## References

https://unstats.un.org/unsd/methodology/m49/overview has been used to categorize ngos to correct countries, regions and sub-regions.
https://www.kaggle.com/paultimothymooney/latitude-and-longitude-for-every-country-and-state was used and modified to get coordinates for countries (modifications are the capitalized cells).
