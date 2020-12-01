# FindYourNGO

## Quick Start
- check setup guide to get up the database
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


### Postgres

#### Make Postgres Persistent
If you are using Windows, there might be an issue with file permissions using a local directory as a volume.

Instead, manually create a docker volume via the command: docker volume create findyourngovolume
The data will then be persisted into this volume.


#### Access Postgres DB from outside of docker
Postgres in docker is mapped to port 5433 (not the default 5432, since this can clash with local installations of postgres). Open the database menu in PyCharm, click on '+', 'PostgreSQL', enter correct port, username (postgres) and password (postgres). Use the 'test connection' button to make sure it actually works.
Alternatively, you can also connect via pgAdmin.


## Architecture

TODO
Refer to https://docs.docker.com/compose/django/ for a quick overview of how the infrastructure was built.
RestAPI guide: https://www.django-rest-framework.org/tutorial/quickstart/
django-admin can be used inside the cli with docker-compose exec web /bin/bash


### Functionality

#### Trustworthiness Calculation
Please refer to [this](./Backend/findyourngo/README.md) document.

