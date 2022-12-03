# CS480 - Team Vision API

## Installation
1. Install pipenv
```
pip install --user pipenv
```
2. Install project requirements
```
pipenv install
```

## Adding secrets
Refer to `.env.example` and add your secrets to `.env`

## Running the Application
```
pipenv run start
```

## Complying to the pep8 standard
```
pipenv run lint
```

## Running via Docker
```
make build
make up
```