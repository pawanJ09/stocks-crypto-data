from bs4 import BeautifulSoup
from stock import Stock
import requests
import globals
import time
import csv


def start():
    """
    This method triggered from main is the starting point for the processing
    """
    entity_code = user_input()
    period_start, period_end = date_criteria()
    response = fetch_data(entity_code, period_start, period_end)
    generate_data(entity_code, response)


def user_input():
    """
    This method takes the entity name from the user and looks up the dictionary to find the code.
    This code is then returned for the data to be fetched.
    :return: str entity_code
    """
    print(f'Stocks and Cryptos currently supported {", ".join(globals.entity_dict.keys())}')
    while True:
        entity_code = ''
        try:
            entity_input = input("Enter any of the stocks or cryptos that you would like "
                                 "to search for: ")
            if globals.entity_dict[entity_input.capitalize()]:
                entity_code = globals.entity_dict[entity_input.capitalize()]
        except KeyError as error:
            continue
        else:
            return entity_code


def date_criteria():
    """
    This method generates the start and end criteria in seconds that will be appended to the url
    :return: (period_start, period_end)
    """
    period_start = round((time.time()) - (5 * 365.25) * 24 * 60 * 60)
    period_end = round(time.time())
    return period_start, period_end


def fetch_data(entity_code, period_start, period_end):
    """
    This method generates the url as per the provided args, invokes the url and returns the response
    :param entity_code: str code
    :param period_start: time in seconds
    :param period_end: time in seconds
    :return: requests.models.Response object
    """
    url = globals.url.format(entity_code, period_start, period_end)
    header = globals.headers
    print(f'Fetching data for {entity_code}')
    response = requests.get(url=url, headers=header)
    return response


def generate_data(entity_code, response):
    """
    This method parses the response from the invoked url and writes the contents to a csv file
    named as the crypto code
    :param entity_code: str code
    :param response: requests.models.Response object
    :return:
    """
    soup = BeautifulSoup(response.text, "html.parser")
    content_list = str(soup).split("\n")
    crypto_list = [generate_entity_object(c) for i, c in enumerate(content_list) if i > 0]
    print(f'Writing data for {entity_code}')
    with open(entity_code + '.csv', 'w') as csv_file:
        header = 'Date,Open,High,Low,Close,Adj Close,Volume'
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(header.split(','))
        for crypto in crypto_list:
            csv_writer.writerow(crypto.__str__().split('|'))


def generate_entity_object(content):
    """
    This method parses the line content and converts it to Crypto object
    :param content: str row from response
    :return: com.Entity.Entity object
    """
    return Stock(content.split(","))



