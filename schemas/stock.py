from marshmallow import Schema, fields, INCLUDE


class StockCurrentSchema(Schema):
    class Meta:
        unknown = INCLUDE
    current_price = fields.Float()
    price_change = fields.Str()
    market_change = fields.Str()

