# RESTless

A super simple RESTful API made with flask and sqlalchemy.

## Install

    make init

## Run

    make

## API

GET     /users - Gets all users

response

    {
        "data": [
            {
                "first_name": "Ada",
                "last_name": "Lovelace",
                "username": "Ada",
                "email": "ada@example.com",
                "uuid": "00000000-0000-0000-0000-000000000000",
                "created": "01/01/1970 00:00:00",
                "modified": "01/01/1970 00:00:00"
            },
            {
                ...
            },
        ]
    }

GET     /users/<uuid> - Gets a user

response

    uuid = 00000000-0000-0000-0000-000000000000
    {
        "data": {
            "first_name": "Ada",
            "last_name": "Lovelace",
            "username": "Ada",
            "email": "ada@example.com",
            "uuid": "00000000-0000-0000-0000-000000000000",
            "created": "01/01/1970 00:00:00",
            "modified": "01/01/1970 00:00:00"
        }
    }

POST    /users - Creates a new user.

data

    {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "username": "Ada",
        "email": "ada@example.com"
    }

response

    {
        "data": {
            "first_name": "Ada",
            "last_name": "Lovelace",
            "username": "Ada",
            "email": "ada@example.com",
            "uuid": "00000000-0000-0000-0000-000000000000",
            "created": "01/01/1970 00:00:00",
            "modified": "01/01/1970 00:00:00"
        }
    }

PATCH /users/<uuid>

data

    uuid = 00000000-0000-0000-0000-000000000000
    {
        "first_name": "Tupac",
        "last_name": "Shakur",
        "username": "2Pac",
        "email": "makaveli@example.com"
    }

response

    {
        "data": {
            "first_name": "Tupac",
            "last_name": "Shakur",
            "username": "2Pac",
            "email": "makaveli@example.com"
            "uuid": "00000000-0000-0000-0000-000000000000",
            "created": "01/01/1970 00:00:00",
            "modified": "01/01/1970 00:00:01"
        }
    }

DELETE /users/<uuid>

response

    {}
