from model.stockscode import StocksCodeModel
from datetime import datetime


class StockModel:

    def __init__(self, stock_code_id, *args):
        self.stock_id = stock_code_id
        self.stock_date = datetime.strptime(args[0][0], '%Y-%m-%d').date()
        self.open_val = float(args[0][1])
        self.high_val = float(args[0][2])
        self.low_val = float(args[0][3])
        self.close_val = float(args[0][4])
        self.adj_close_val = float(args[0][5])
        self.volume = int(args[0][6])

    def __str__(self):
        return f'{self.stock_id},{self.stock_date},{self.open_val},{self.high_val},' \
               f'{self.low_val}, {self.close_val},{self.adj_close_val},{self.volume}'

    def json(self):
        return {"id": self.id, "stock_id": self.stock_id,
                "stock_date": self.stock_date.strftime('%Y-%m-%d'),
                "open_val": float(self.open_val), "high_val": float(self.high_val),
                "low_val": float(self.low_val),
                "close_val": float(self.close_val), "adj_close_val": float(self.adj_close_val),
                "volume": int(self.volume)}

    def __repr__(self):
        return f"StockModel(id={self.id!r}, stock_id={self.stock_id!r}, " \
               f"stock_date={self.stock_date!r}), open_val={self.open_val!r}), high_val=" \
               f"{self.high_val!r}), low_val={self.low_val!r}), close_val={self.close_val!r})," \
               f"adj_close_val={self.adj_close_val!r}), volume={self.volume!r})"

    @classmethod
    def fetch_listings_by_name(cls, name):
        stock_code = StocksCodeModel.find_by_name(name)
        if stock_code is not None:
            # This is ORM 1.x style
            return cls.query.filter(StockModel.stock_id == stock_code.id)\
                .order_by(StockModel.stock_date)

    @classmethod
    def fetch_listings_by_name_and_date(cls, name, *args):
        pass

    @classmethod
    def fetch_listing_max_date(cls, stock_code):
        """
        This method fetches the listing max date for the requested stock
        :param stock_code: models.stockscode.StocksCodeModel object
        :return row: max date
        """
        pass

    def save_to_db(self):
        pass

    @classmethod
    def delete_from_db(cls, stock_code):
        pass


class StockCurrentModel:

    def __init__(self, current_price, price_change, market_change):
        self.current_price = current_price
        self.price_change = price_change
        self.market_change = market_change

    def __repr__(self):
        return f'StockCurrentModel({self.current_price}, {self.price_change}, {self.market_change})'
