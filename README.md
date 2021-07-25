# Geoloc backend

Django-based REST API allowing to store the geolocalization data based on the IP from the IPStack.com.

Currently POST, GET and DELETE APIs are implemented.

Before local usage, add the ACCESS KEY to the IPStack in the `.env` file.

## Development

### Local environment

1. Create local settings

   ```shell script
   cp geoloc/settings/local.py geoloc/settings/local_settings.py
   ```

1. Install Docker ≥ 18.09 and docker-compose.

1. Build docker image for backend with command:

   ```shell script
   DOCKER_BUILDKIT=1 docker build --ssh default -t geoloc_backend .
   ```

1. Bootstrap project

   ```shell script
   docker-compose run --rm backend bootstrap
   ```

1. Run the app and verify that all services are up:

   ```shell script
   docker-compose up -d
   docker-compose ps
   ```

1. At the end stop all running containers:

   ```shell script
   docker-compose down
   ```

1. If you want to remove all changes from the database, delete the database volume:

   ```shell script
   docker volume rm geoloc_db-data
   ```

### Users

To log in use of of the following roles:

| Username | Email           | Password |
| -------- | --------------- | -------- |
| admin    | admin@admin.com | password |


## Local tests

To test the app you can use any platform for API development (Postman, HTTPie etc.).

First you need to generate token using `/api/token/` endpoint and pass the username and password for the existing user to mimic the behaviour of frontend.

For example in HTTPie:

```
http POST localhost:8000/api/token/ username=admin password=password
```


The result of the query will contain json-based dictionary with the token required to access other APIs:

```
{
   "access": "XXXXXXXXXXX",
   "refresh": "XXXXXXXXXXX"
}

```

The token is valid for 5 minutes.

The token has to be then attached as an authorization request header to access Geoloc APIs.

All implemented APIs can be accessed via `/localization/` endpoint. The APIs require `ip_address` to be specified as the parameter. If the parameter is not specified, 400 status code is returned.

#### GET API

```
http GET localhost:8000/localization/ "Authorization: Bearer XXXXXXXXXXXXX" ip_address=134.201.250.155
```

The successfull query results in the json containing basic information about the geolocalization associated with the given IP address:

```
{
    "city": "Los Angeles",
    "continent_code": "NA",
    "continent_name": "North America",
    "country_code": "US",
    "country_name": "United States",
    "id": 1,
    "ip": "134.201.250.155",
    "latitude": 34.0655517578125,
    "longitude": -118.24053955078125,
    "region_code": "CA",
    "region_name": "California",
    "zip_code": "90012"
}
```

#### POST API

```
http POST localhost:8000/localization/ "Authorization: Bearer XXXXXXXXXXXXX" ip_address=134.201.250.155
```

The successful query returns 201 status code and information about adding the entry to the database.

#### DELETE API

```
http DELETE localhost:8000/localization/ "Authorization: Bearer XXXXXXXXXXXXX" ip_address=134.201.250.155
```

The successful query returns 200 status code and information about removing the entry from the database.


### Heroku 

The backend is also accessible on Heroku:

```
https://geoloc-django.herokuapp.com
```

### Users

To log in use of of the following roles:

| Username | Email           | Password |
| -------- | --------------- | -------- |
| admin    | admin@admin.com | QWE123asd |
