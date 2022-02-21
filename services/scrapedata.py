from bs4 import BeautifulSoup
from model.stock import StockModel
from sqlalchemy.exc import DataError
import requests
from globals import url, headers
import time
import csv


def scrape_and_save(stock_code):
    period_start, period_end = date_criteria()
    response = scrape_data(stock_code, period_start, period_end)
    generate_data(stock_code, response)


def date_criteria():
    """
    This method generates the start and end criteria in seconds that will be appended to the url
    :return: (period_start, period_end)
    """
    period_start = round((time.time()) - (5 * 365.25) * 24 * 60 * 60)
    period_end = round(time.time())
    return period_start, period_end


def scrape_data(stock_code, period_start, period_end):
    """
    This method generates the url as per the provided args, invokes the url and returns the response
    :param stock_code: mode.stockscode.StocksCodeModel object
    :param period_start: time in seconds
    :param period_end: time in seconds
    :return: requests.models.Response object
    """
    local_url = url.format(stock_code.code, period_start, period_end)
    print(f'Fetching data for {stock_code.name}')
    response = requests.get(url=local_url, headers=headers)
    return response


def generate_data(stock_code, response):
    """
    This method parses the response from the invoked url and writes the contents to a csv file
    named as the crypto code
    :param stock_code: mode.stockscode.StocksCodeModel object
    :param response: requests.models.Response object
    :return:
    """
    soup = BeautifulSoup(response.text, "html.parser")
    content_list = str(soup).split("\n")
    stock_listings = [generate_stockmodel_object(stock_code.id, c) for i, c in enumerate(
        content_list) if i > 0]
    try:
        for listing in stock_listings:
            listing.save_to_db()
    except DataError as error:
        write_to_file(stock_code.code, stock_listings)


def generate_stockmodel_object(stock_code_id, content):
    """
    This method parses the line content and converts it to StockModel object
    :param stock_code_id: int id from stocks_code table
    :param content: str row from response
    :return: model.stock.StockModel object
    """
    return StockModel(stock_code_id, content.split(","))


def write_to_file(entity_code, stock_listings):
    """
    This method writes the fetched contents to file in case there is an error writing to database
    :param entity_code: str code
    :param stock_listings: List of com.stock.StockModel objects
    """
    print(f'Writing data for {entity_code}')
    with open(entity_code + '.csv', 'w') as csv_file:
        header = 'stock_id,stock_date,open_val,high_val,low_val,close_val,adj_close_val,volume'
        csv_writer = csv.writer(csv_file, delimiter='|')
        csv_writer.writerow(header.split(','))
        for listing in stock_listings:
            csv_writer.writerow(listing.__str__().split(','))



