# Nanny API

API to run inside Nanny project.


## Getting started

```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install pipenv
```

```bash
pipenv update
pipenv run alembic upgrade head
pipenv run uvicorn api.main:app --port=8080 --reload
```

Run the application on the browser `http://localhost:8080`.


## Development

### Prerequisites
**Python version**
* `3.8`
```bash
sudo apt install python3.8
```

**System packages**
* `pip`
* `python3-dev`
```
sudo apt install python3-pip python3-dev
# sudo apt install python3.8-pip python3.8-dev
```

**Python modules**
* `pipenv`
```bash
pip install pipenv
```

### Prepare environment
```bash
pipenv update --dev
```

### Running local
```bash
pipenv run alembic upgrade head
pipenv run uvicorn api.main:app --port=8080 --reload
```

### Running tests
```bash
pipenv run pytest api/tests/test_*
```


## Documentation

### Draw database entity-relation schema
```bash
sudo apt update
sudo apt install libgraphviz-dev
pipenv run python docs/generate_database_graph.py
```