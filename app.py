from flask import Flask
from flask_restful import Api
from resources.stockscode import StocksNameResource, StocksListResource


app = Flask(__name__)

api = Api(app)
api.add_resource(StocksNameResource, '/stocks_code/<string:name>')
api.add_resource(StocksListResource, '/stocks_codes')

import resources.stock