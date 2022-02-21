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

## Usage

### Stocks Code base model CRUD operations

- GET http://127.0.0.1:5001/stocks_codes: Get all stock names and codes in system.
- GET http://127.0.0.1:5001/stocks_code/<name>: Get stock code by name.
- POST http://127.0.0.1:5001/stocks_code/<name>: Create new stock code in system.

```json
{
    "code": "FB-USD"
}
```

- PUT http://127.0.0.1:5001/stocks_code/<name>: Update existing stock code with the provided 
  name if it exists else create new.

```json
{
    "code": "FB"
}
```

- DELETE http://127.0.0.1:5001/stocks_code/<name>: Delete stock code and name from system.

### Stocks listings operations:

- GET http://127.0.0.1:5001/stocks/<name>: Get all listings of the requested stock from the system.
- GET http://127.0.0.1:5001/stocks/<name>?date_from=<yyyy-mm-dd>: Get all listings of the 
  requested stock from the date provided in the system.
- GET http://127.0.0.1:5001/stocks/<name>?date_from=<yyyy-mm-dd>&date_to=<yyyy-mm-dd>: Get all 
  listings of the requested stock from the date range in the system.
- POST http://127.0.0.1:5001/stocks/refresh/<name>: Fetch from web scraping and update listings of 
  the provided stock in the system.
- DELETE http://127.0.0.1:5001/stocks/<name>: Delete all listings of the provided stock from the 
  system.