<meta name="google-site-verification" content="h8-Bfstpt11Qx1tYnzjOlUrz7z4u1CjM6qJOGmAc9u0" />

# Stocks and Crypto Data Analyzer

This app fetches the current and historical data of 5 years for the requested Stock or Crypto. 
The program has dependency on requests and BeautifulSoup module which invokes the Yahoo 
Finance query engine, scrapes requested data and stores it in PostgreSQL. The APIs are created 
and exposed using Flask, Flask-RESTful, Flask-SQLAlchemy and Marshmallow.

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

- GET http://127.0.0.1:5001/stocks_codes : Get all stock names and codes in system.
- GET http://127.0.0.1:5001/stocks_code/:stock_name : Get stock code by name.
- POST http://127.0.0.1:5001/stocks_code/:stock_name : Create new stock code in system.

```json
{
    "code": "FB-USD"
}
```

- PUT http://127.0.0.1:5001/stocks_code/:stock_name : Update existing stock code with the provided 
  name if it exists else create new.

```json
{
    "code": "FB"
}
```

- DELETE http://127.0.0.1:5001/stocks_code/:stock_name : Delete stock code and name from system.

### Stocks listings operations:

- GET http://127.0.0.1:5001/stocks/:stock_name : Get current listings of the requested stock 
  from source.
- GET http://127.0.0.1:5001/stocks/historical/:stock_name : Get all listings of the requested 
  stock from the system.
- GET http://127.0.0.1:5001/stocks/historical/:stock_name?date_from=:yyyy-mm-dd : Get all 
  listings of the requested stock from the date provided in the system.
- GET http://127.0.0.1:5001/stocks/historical/:stock_name?date_from=:yyyy-mm-dd&date_to=:yyyy-mm-dd : Get all listings of the requested stock from the 
  date range in the system.
- POST http://127.0.0.1:5001/stocks/refresh/:stock_name : Fetch from web scraping and update 
  listings of the provided stock in the system.
- DELETE http://127.0.0.1:5001/stocks/:stock_name : Delete all listings of the provided stock 
  from the system.

### Connecting to AWS

Use host as stocks-crypto-data-alb-708152569.us-east-2.elb.amazonaws.com for the above endpoints 
to access these services directly on AWS Cloud.
