from flask_restful import Api, Resource, reqparse
from database import db_session
from model.stockscode import StocksCodeModel


class StocksNameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('code',
                        type=str,
                        required=True,
                        help='Code cannot be left empty'
                        )

    def get(self, name):
        stock = StocksCodeModel.find_by_name(name)
        if stock is not None:
            return stock.json()
        return {"message": "Not found"}, 404

    def post(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = StocksCodeModel.find_by_name(name)
        if stock is None:
            stock = StocksCodeModel(name, data['code'])
            stock.save_to_db()
            return self.get(name)
        else:
            return {"message": f"{name} already exists"}, 400

    def put(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = StocksCodeModel.find_by_name(name)
        if stock is None:
            stock = StocksCodeModel(name, data['code'])
        else:
            stock.code = data['code']
        stock.save_to_db()
        return self.get(name)

    def delete(self, name):
        stock = StocksCodeModel.find_by_name(name)
        if stock is not None:
            stock.delete_from_db()
            return {"message": f"{name} deleted"}, 200
        return {"message": "Not found"}, 404


class StocksListResource(Resource):

    def get(self):
        return {"stocks": list(map(lambda x: x.json(), db_session.query(StocksCodeModel).all()))}


