# Containerised data scientific development
#### A simple template to set up a containerised data scientific development environment using python

The repository contains a Docker compose file to set up a useful containerised data scientific 
development environment, that has a database for storing data and information
about various runs (db), an administration api (adminer) to access the databases,
and finally python container (py) where python code can be executed.

### To develop python programs
A python module called database.py is included in ./c1_python/app/utils
and allows for easily saving to or loading from the database. Python
files should be put in ./c1_python/app/ and will be copied into the container,
with main.py being run as default.

### To run
Navigate into the repository in the terminal and type:\
docker compose up

### Additional information
Default usernames, passwords and ports are globally set in the .env file.

Images used for the containers are:\
    db: mariadb:latest\
    py: python:3.9-slim (can also be changed to an image with jupyter if required)\
    adminer: adminer:latest
