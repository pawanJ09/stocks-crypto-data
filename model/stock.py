from model.stockscode import StocksCodeModel
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from schemas.stock import StocksCodeSchema
from decimal import Decimal
from database import resource

table = resource.Table('stocks-dd')

scs = StocksCodeSchema()


class StockModel:

    def __init__(self, stock_code_id, *args):
        self.stock_id = stock_code_id
        self.stock_date = args[0][0]
        self.open_val = Decimal(args[0][1])
        self.high_val = Decimal(args[0][2])
        self.low_val = Decimal(args[0][3])
        self.close_val = Decimal(args[0][4])
        self.adj_close_val = Decimal(args[0][5])
        self.volume = Decimal(args[0][6])

    def __str__(self):
        return f'{self.stock_id},{self.stock_date},{self.open_val},{self.high_val},' \
               f'{self.low_val}, {self.close_val},{self.adj_close_val},{self.volume}'

    def json(self):
        return {"stock_id": self.stock_id,
                "stock_date": self.stock_date.strftime('%Y-%m-%d'),
                "open_val": float(self.open_val), "high_val": float(self.high_val),
                "low_val": float(self.low_val),
                "close_val": float(self.close_val), "adj_close_val": float(self.adj_close_val),
                "volume": int(self.volume)}

    def __repr__(self):
        return f"StockModel(stock_id={self.stock_id!r}, " \
               f"stock_date={self.stock_date!r}), open_val={self.open_val!r}), high_val=" \
               f"{self.high_val!r}), low_val={self.low_val!r}), close_val={self.close_val!r})," \
               f"adj_close_val={self.adj_close_val!r}), volume={self.volume!r})"

    @classmethod
    def fetch_listings_by_name(cls, name):
        stock_code_response = StocksCodeModel.find_by_name(name)
        if stock_code_response is not None and 'Item' in stock_code_response:
            stock_code = scs.load(stock_code_response['Item'])
            if stock_code:
                response = table.query(
                    KeyConditionExpression=Key('stock_id').eq(stock_code.stock_id)
                )
                return response

    @classmethod
    def fetch_listings_by_name_and_date(cls, name, *args):
        stock_code_response = StocksCodeModel.find_by_name(name)
        if stock_code_response is not None and 'Item' in stock_code_response:
            stock_code = scs.load(stock_code_response['Item'])
            if stock_code:
                response = table.query(
                    KeyConditionExpression=Key('stock_id').eq(stock_code.stock_id) & Key(
                        'stock_date').gte(args[0])
                )
                return response

    @classmethod
    def fetch_listings_by_name_and_daterange(cls, name, *args):
        stock_code_response = StocksCodeModel.find_by_name(name)
        if stock_code_response is not None and 'Item' in stock_code_response:
            stock_code = scs.load(stock_code_response['Item'])
            if stock_code:
                response = table.query(
                    KeyConditionExpression=Key('stock_id').eq(stock_code.stock_id) & Key(
                        'stock_date').between(args[0], args[1])
                )
                return response

    @classmethod
    def fetch_listing_max_date(cls, stock_code):
        """
        This method fetches the listing max date for the requested stock
        :param stock_code: models.stockscode.StocksCodeModel object
        :return row: max date
        """
        response = table.query(
            KeyConditionExpression=Key('stock_id').eq(stock_code.stock_id),
            ScanIndexForward=False, Limit=1
        )
        if response is not None and 'Items' in response and response['Count'] > 0:
            return response['Items'][0]['stock_date']

    def save_to_db(self):
        try:
            response = table.put_item(
                Item={
                    'stock_id': self.stock_id,
                    'stock_date': self.stock_date,
                    'open_val': self.open_val,
                    'high_val': self.high_val,
                    'low_val': self.low_val,
                    'close_val': self.close_val,
                    'adj_close_val': self.adj_close_val,
                    'volume': self.volume
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

    @classmethod
    def delete_from_db(cls, stock_code):
        stock_code_response = StockModel.fetch_listings_by_name(stock_code.stock_name)
        with table.batch_writer() as batch:
            for item in stock_code_response['Items']:
                batch.delete_item(
                    Key={
                        'stock_id': item['stock_id'],
                        'stock_date': item['stock_date']
                    }
                )


class StockCurrentModel:

    def __init__(self, current_price, price_change, market_change):
        self.current_price = current_price
        self.price_change = price_change
        self.market_change = market_change

    def __repr__(self):
        return f'StockCurrentModel({self.current_price}, {self.price_change}, {self.market_change})'
