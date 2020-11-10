# Nanny API

API to run inside Nanny project.


## Getting started
Install required packages:
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install pipenv
```

Setup the database:
```bash
docker-compose up -d
```

Run the app:
```bash
pipenv update
pipenv run alembic upgrade head
pipenv run uvicorn api.main:app --port=8080 --reload
```


## Development

### Setup workspace
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install pipenv
pipenv update --dev
```

### Run locally
This section use docker database called `nanny`.
```bash
docker-compose up -d
pipenv run alembic upgrade head
pipenv run uvicorn api.main:app --port=8080 --reload
```

### Run tests
This section use docker database called `nanny_test`.
```bash
docker-compose up -d
pipenv run pytest app/tests/crud/test_user.py -v -s
```
