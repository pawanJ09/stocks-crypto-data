from model.stockscode import StocksCodeModel
from flask_restful import Resource, reqparse
from database import db_session


class StocksNameResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('code',
                        type=str,
                        required=True,
                        help='Code cannot be left empty'
                        )

    def get(self, name):
        stock = db_session.query(StocksCodeModel).filter(StocksCodeModel.name == name).first()
        if stock is not None:
            return stock.json()
        return {"message": "Not found"}, 404

    def post(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = db_session.query(StocksCodeModel).filter(StocksCodeModel.name == name).first()
        if stock is None:
            stock = StocksCodeModel(name, data['code'])
            db_session.add(stock)
            db_session.commit()
            return self.get(name)
        else:
            return {"message": f"{name} already exists"}, 400

    def put(self, name):
        data = StocksNameResource.parser.parse_args()
        stock = db_session.query(StocksCodeModel).filter(StocksCodeModel.name == name).first()
        if stock is None:
            stock = StocksCodeModel(name, data['code'])
        else:
            stock.code = data['code']
        db_session.add(stock)
        db_session.commit()
        return self.get(name)

    def delete(self, name):
        stock = db_session.query(StocksCodeModel).filter(StocksCodeModel.name == name).first()
        if stock is not None:
            db_session.delete(stock)
            db_session.commit()
            return {"message": f"{name} deleted"}, 200
        return {"message": "Not found"}, 404


class StocksListResource(Resource):

    def get(self):
        return {"stocks": list(map(lambda x: x.json(), db_session.query(StocksCodeModel).all()))}
