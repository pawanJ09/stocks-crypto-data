from flask import Flask
from flask_restful import Api
from database import init_db
from resources.stockscode import StocksNameResource, StocksListResource
from resources.stock import StockResource


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

api = Api(app)
api.add_resource(StocksNameResource, '/stocks_code/<string:name>')
api.add_resource(StocksListResource, '/stocks_codes')
api.add_resource(StockResource, '/stocks/refresh')


if __name__ == '__main__':
    init_db()
    app.run(port=5001, host='0.0.0.0')