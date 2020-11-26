# FindYourNGO

Refer to https://docs.docker.com/compose/django/ for a quick overview of how the infrastructure was built.
RestAPI guide: https://www.django-rest-framework.org/tutorial/quickstart/
django-admin can be used inside the cli with docker-compose exec web /bin/bash



# Postgres

## Make Postgres Persistent
If you are using Windows, there might be an issue with file permissions using a local directory as a volume.

Instead, manually create a docker volume via the command: docker volume create findyourngovolume
The data will then be persisted into this volume.


## Access Postgres DB from outside of docker
Postgres in docker is mapped to port 5433 (not the default 5432, since this can clash with local installations of postgres). Open the database menu in PyCharm, click on '+', 'PostgreSQL', enter correct port, username (postgres) and password (postgres). Use the 'test connection' button to make sure it actually works.
Alternatively, you can also connect via pgAdmin.
