from flask_restful import Resource, reqparse
from model.stockscode import StocksCodeModel
from random import sample
from schemas.stock import StocksCodeSchema

scs = StocksCodeSchema()
scs_many = StocksCodeSchema(many=True)


class StocksNameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('code',
                        type=str,
                        required=True,
                        help='Code cannot be left empty'
                        )

    def get(self, name):
        stock = StocksCodeModel.find_by_name(name)
        if stock['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Item' in stock:
            return scs.dump(stock['Item'])
        return {"message": f"{name} not found"}, 404

    def post(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = StocksCodeModel.find_by_name(name)
        if stock is not None and 'Item' not in stock:
            stock_id = sample(range(1, 200), 1)
            stock = StocksCodeModel(int(stock_id[0]), name, data['code'])
            stock.save_to_db()
            return self.get(name)
        else:
            return {"message": f"{name} already exists"}, 400

    def put(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = StocksCodeModel.find_by_name(name)
        if stock is not None and 'Item' not in stock:
            stock_id = sample(range(1, 200), 1)
            stock = StocksCodeModel(int(stock_id[0]), name, data['code'])
            stock.save_to_db()
            return self.get(name)
        elif stock is not None:
            StocksCodeModel.update_in_db(stock['Item']['stock_name'], data['code'])
            return self.get(name)
        else:
            return {"message": f"{name} create/update failed"}, 400

    @classmethod
    def delete(cls, name):
        stock = StocksCodeModel.find_by_name(name)
        if stock is not None and 'Item' in stock:
            StocksCodeModel.delete_from_db(stock['Item']['stock_name'])
            return {"message": f"{name} deleted"}, 200
        return {"message": f"{name} not found"}, 404


class StocksListResource(Resource):

    @classmethod
    def get(cls):
        StocksCodeModel.fetch_all()
        return {"stocks": scs_many.dump(StocksCodeModel.fetch_all()['Items'])}


