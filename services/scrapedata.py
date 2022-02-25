from bs4 import BeautifulSoup
from model.stock import StockModel, StockCurrentModel
from sqlalchemy.exc import DataError
from globals import url, headers, current_data_url
from datetime import datetime
import requests
import time
import csv


def scrape_and_save(stock_code):
    period_start, period_end = date_criteria(stock_code)
    response = scrape_data(stock_code, period_start, period_end)
    generate_data(stock_code, response)


def date_criteria(stock_code):
    """
    This method generates the start and end criteria in seconds that will be appended to the url
    :param stock_code: model.stockscode.StocksCodeModel object
    :return: (period_start, period_end)
    """
    max_date = StockModel.fetch_listing_max_date(stock_code)
    if max_date is not None:
        if datetime.now().date() == max_date:
            # if both are equal then no need to fetch latest data
            return 0, 0
        else:
            # Add 1 day to max_date to start fetching from next date
            period_start = round(datetime(max_date.year, max_date.month, max_date.day).timestamp()
                                 + (24*60*60))
    else:
        period_start = round((time.time()) - (5 * 365.25) * 24 * 60 * 60)
    period_end = round(time.time())
    return period_start, period_end


def scrape_data(stock_code, period_start, period_end):
    """
    This method generates the url as per the provided args, invokes the url and returns the response
    :param stock_code: model.stockscode.StocksCodeModel object
    :param period_start: time in seconds
    :param period_end: time in seconds
    :return: requests.models.Response object
    """
    local_url = url.format(stock_code.code, period_start, period_end)
    print(f'url {local_url}')
    print(f'Fetching data for {stock_code.name}')
    response = requests.get(url=local_url, headers=headers)
    return response


def generate_data(stock_code, response):
    """
    This method parses the response from the invoked url and writes the contents to a csv file
    named as the crypto code
    :param stock_code: model.stockscode.StocksCodeModel object
    :param response: requests.models.Response object
    :return:
    """
    if response.status_code == 200:
        print(f'Parsing response for {stock_code.name}')
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


def fetch_current_data(stock_code):
    """
    This method fetches the current stock listing for the requested stock code
    :param stock_code: model.stockscode.StocksCodeModel object
    :return current_stock: model.stock.StockCurrentModel object
    """
    response = scrape_current_stock_data(stock_code)
    current_stock = parse_current_stock_data(stock_code, response)
    return current_stock


def scrape_current_stock_data(stock_code):
    """
    This method generates the url as per the provided args, invokes the url and returns the
    response with current stock data in html format
    :param stock_code: model.stockscode.StocksCodeModel object
    :return: requests.models.Response object
    """
    current_url = current_data_url.format(stock_code.code)
    print(f'url {current_url}')
    print(f'Fetching data for {stock_code.name}')
    response = requests.get(url=current_url, headers=headers)
    return response


def parse_current_stock_data(stock_code, response):
    """
    This method parses the response from the invoked url and returns the current model object
    :param stock_code: model.stockscode.StocksCodeModel object
    :param response: requests.models.Response object
    :return s: model.stock.StockCurrentModel object
    """
    soup = BeautifulSoup(response.text, "html.parser")
    stock_component = soup.find('div', attrs={'class': 'D(ib) Mend(20px)'})
    cp_component = stock_component.find('fin-streamer', attrs={'data-field': 'regularMarketPrice'})
    pc_component = stock_component.find('fin-streamer', attrs={'data-field': 'regularMarketChange'})
    mc_component = stock_component.find('fin-streamer',
                                         attrs={'data-field': 'regularMarketChangePercent'})

    s = StockCurrentModel(cp_component['value'], pc_component.span.text,
                          mc_component.span.text[1:-1])
    return s
