# Stocks and Crypto Data Analyzer

This app fetches the historical data of 5 years for the requested Stock or Crypto options. This 
program has dependency on requests module which invokes the Yahoo Finance query engine and 
fetches all the requested data. The exposed APIs are created using Flask-RESTful and 
Flask-SQLAlchemy.

## Requirements

For building and running the application you need:

- [Python3](https://www.python.org/downloads/)

```shell
pip3 install -r requirements.txt
```

## Running the application locally

You can run the main.py program to get started. This file has the __main__ method.

```shell
python main.py
```

## Build and Run using Docker

### Build image

```shell
docker-compose build
```

### Run the container from built image

```shell
docker-compose up
```

