# :sweat_drops: SNIRH API

Transformation of [SNIRH](https://snirh.apambiente.pt/) platform data into an accessible RESTFull API.

running at https://snirhapi.herokuapp.com/

## What is SNIRH?
[SNIRH](https://snirh.apambiente.pt/) (Sistema Nacional de Informação de Recursos Hídricos - National Information System for Water Resources) is a website built in the mid90s that gives access to all sorts of water resources data accross Portugal. It had little to no updates in the last 30 years.


## Motivation
- The user interface is pretty old and hard to get multiple station's data.
- Provide access the data in a easy and standard format, through a REST API.
- On top of this API, a frontend modern application can be easily built.

## Development

This project consists of 2 main blocks:
- [**Crawler**](src/client) - fetches the data and transforms it into standart python formats.
- [**App**](#) - usess the fetched data and creates a RESTFull API interface for easy access.


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
