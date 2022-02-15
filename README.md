# Stocks and Crypto Data Analyzer

This app fetches the historical data of 5 years for the requested Stock or Crypto options. This 
program has dependency on requests module which invokes the Yahoo Finance query engine and 
fetches all the requested data.

## Requirements

For building and running the application you need:

- [Python3](https://www.python.org/downloads/)

```shell
python3 -m pip install requests

python3 -m pip install bs4
```

## Running the application locally

You can run the main.py program to get started. This file has the __main__ method.

```shell
python main.py
```

## Build and Run using Docker

### Build image

```shell
docker build --tag <pawanj09/stocks-crypto-data:v1.0.0> .
```

### Run the container from built image

Here we use -it for interactive terminal since we have to input the city from user.

```shell
docker run --name <stocks-crypto-data> -p 1001:1001 -it <pawanj09/stocks-crypto-data:v1.0.0>
```

### Start the container if re-executing the image

```shell
docker start <stocks-crypto-data> -i
```

### Run using image from Docker hub

```shell
docker pull docker pull <pawanj09/stocks-crypto-data>

docker run --name <stocks-crypto-data> -p 1001:1001 -it <pawanj09/stocks-crypto-data>
```

