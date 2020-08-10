# FSND Capstone Project: Casting Agency

## Motivation

The _pretextual_ motivation for this project is to develop an API that enables an unnamed casting agency to manage their day-to-day operations, which involve casting actors in movies. But the true purpose here is to wrap up and demonstrate the technical skills learned over the course of Udacity's Full Stack Web Developer Nanodegree Program, including data modeling using SQLAlchemy, API development using Flask, third-party authentication using Auth0, and app deployment using Heroku.

## Dependencies

For local development and testing, you will need python and postgres. The minimal set of python dependencies you may need are included in `requirements.txt`, and you can install them by running:
```
pip install -r requirements.txt
```

## Running locally

To run the app in your local environment, update the database URLs specified in `setup.sh` to point to your local database and then export the environment variables:
```
source setup.sh
```

These variables also include the authentication tokens needed to make successful API calls, corresponding to specific roles. See the [API Endpoints](#api-endpoints) section below for details.

Starting the development server is as simple as running:
```
python app.py
```

To run the included unit test suite:
```
python test_app.py
```

The app is currently hosted on Heroku and can be accessed via this link: https://fsnd-castingagency.herokuapp.com/

## API Endpoints

The following requests have limited access based on user roles. The relevant roles are Casting Assistant, Casting Director, and Executive Producer. Generally, an Executive Producer has permission to make any request, while a Casting Director can not add or delete movies. A Casting Assistant **only** has permission to view actors and movies.

[`GET /movies`](#get-movies)\
[`GET /actors`](#get-actors)\
[`POST /movies`](#post-movies)\
[`POST /actors`](#post-actors)\
[`PATCH /movies/<movie_id>`](#patch-moviesmovie_id)\
[`PATCH /actors/<actor_id>`](#patch-actorsactor_id)\
[`DELETE /movies/<movie_id>`](#delete-moviesmovie_id)\
[`DELETE /actors/<actor_id>`](#delete-actorsactor_id)

### GET /movies
- View details about all movies
- Returns: List of movies, each having a title and release date
```
curl <app_domain>/movies -H "Authorization: Bearer <token>"
```

### GET /actors
- View details about all actors
- Returns: List of actors, each having a name, age, and gender
```
curl <app_domain>/actors -H "Authorization: Bearer <token>"
```

### POST /movies
- Create a new movie with a title and a release date
```
curl <app_domain>/movies -H "Authorization: Bearer <token>" -X POST -d {'title':'<title>', 'release_date':'<yyyy-mm-dd>'}
```

### POST /actors
- Create a new actor with a name, age, and gender
```
curl <app_domain>/actors -H "Authorization: Bearer <token>" -X POST -d {'name':'<name>', 'age':<age>, 'gender':'<gender>'}
```

### PATCH /movies/<movie_id>
- Update a movie's attributes by referencing the movie's id
```
curl <app_domain>/movies/<movie_id> -H "Authorization: Bearer <token>" -X PATCH -d {'release_date':'<yyyy-mm-dd>'}
```

### PATCH /actors/<actor_id>
- Update an actor's attributes by referencing the actor's id
```
curl <app_domain>/actors/<actor_id> -H "Authorization: Bearer <token>" -X PATCH -d {'age':<age>}
```

### DELETE /movies/<movie_id>
- Delete a movie by referencing the movie's id
```
curl <app_domain>/movide/<movie_id> -H "Authorization: Bearer <token>" -X DELETE
```

### DELETE /actors/<actor_id>
- Delete an actor by referencing the actor's id
```
curl <app_domain>/actors/<actor_id> -H "Authorization: Bearer <token>" -X DELETE
```
