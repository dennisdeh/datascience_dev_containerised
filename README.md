# Containerised data scientific development
#### A simple template to set up a containerised data scientific development environment using jupyter

The repository contains a Docker compose file to set up a useful containerised data scientific 
development environment with jupyter, that has a database for storing data and information
about various runs (db), an administration api (adminer) to access and administrate the database.

### Development
A python module called database.py is included in .\c1_python\app\utils
and allows for easily saving to or loading from the database and to see the
current data. A template workflow is found in main.ipynb\
Default usernames, passwords, tokens and ports are globally set in the .env file.

### To run
Navigate into the repository in the terminal and type
``
docker compose up
``.
Then go to your browser and navigate to
``http://localhost:8888/lab`` (or modify to what port you set in .env)
and enter the token you set in .env.

### Additional information
Images used for the containers are:
> db: mariadb:latest\
> jupyter: jupyter/scipy-notebook:latest (see https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html for other images for R and Julia)\
> adminer: adminer:latest

