# Swagger generated server

[![Build Status](https://app.travis-ci.com/ivansarno/Users-Service.svg?token=fxpsXuNqp2cTBY7rRspr&branch=master)](https://app.travis-ci.com/ivansarno/Users-Service)
[![Coverage Status](https://coveralls.io/repos/github/ivansarno/Users-Service/badge.svg?t=Op1rfW)](https://coveralls.io/github/ivansarno/Users-Service)

## Overview
This is a microservice designed to handle the users' data for the MyMessageInABottle application,
developed in group during the Advanced Software Engineering course at University of Pisa.
This server was generated by the swagger-codegen using an
OpenAPI-Spec and use Connexion library on top of Flask to run.

## Requirements
Python 3.9

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

and open your browser to here:

```
http://localhost:5001//ui/
```

Your Swagger definition lives here:

```
http://localhost:5001//swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 5001:5001 swagger_server
```
