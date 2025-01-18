# TRADES API

## TRADES API DOCUMENTATION

Trades api is build on top of Uvicorn and FastAPI.

## START API

To start the trades_api, there are two main steps.

Step one: start all containers needed:

```bash
docker compose up --build -d mongo_db
```

if you already build the container from your image you can also start the containers as:

```bash
docker compose start mongo_db
```

and when the containers are available, we can start the api with:


```bash

cd ./apps/trades_api
poetry run uvicorn main:app --workers 8 --port 8010 --host 0.0.0.0

```