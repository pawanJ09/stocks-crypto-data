from marshmallow import Schema, fields, INCLUDE, post_load
from model.stockscode import StocksCodeModel


class StockCurrentSchema(Schema):
    class Meta:
        unknown = INCLUDE
    current_price = fields.Float()
    price_change = fields.Str()
    market_change = fields.Str()


class StocksCodeSchema(Schema):
    class Meta:
        unknown = INCLUDE
    stock_id = fields.Int()
    stock_name = fields.Str()
    stock_code = fields.Str()

    @post_load
    def return_obj(self, data, **kwargs):
        return StocksCodeModel(**data)


class StockSchema(Schema):
    class Meta:
        unknown = INCLUDE
    stock_id = fields.Int()
    stock_date = fields.Str()
    open_val = fields.Float()
    high_val = fields.Float()
    low_val = fields.Float()
    close_val = fields.Float()
    adj_close_val = fields.Float()
    volume = fields.Number(precision=20)
