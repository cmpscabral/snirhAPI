# :sweat_drops: SNIRH API

Transformation of [SNIRH](https://snirh.apambiente.pt/) platform data into an accessible RESTFull API.

## What is SNIRH?
[SNIRH](https://snirh.apambiente.pt/) is a website built in the mid90s for displaying all sorts of water resources data accross Portugal. It had little to no updates in the last 30 years.


## Motivation
- The user interface is pretty old and there's no easy access to the data.
- The main motivation is to access the data in a easy and standard format, through a REST API.
- On top of this API, a frontend modern application can be built.

## Development

This project consists of 2 main blocks:
- [**Crawler**](src/client) - fetches the data and transforms it into standart python formats.
- [**App**](#) - displays the data fetched in the crawler and creates RESTFull API for easy access.


### to setup in your local machine:
```
    git clone https://github.com/franciscobmacedo/snirhAPI
    cd  snirhAPI
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

### to run the app
```
    python3 app.py
```

### to run the crawler
the crawler is located inside [src/client](src/client).


# TODO
- Improve Swagger OpenAPI docs
- Improve this README
- Go live!