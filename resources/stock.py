from flask import request, jsonify
from app import app
from model.stock import StockModel, StocksCodeModel, StockCurrentModel
from services.scrapedata import scrape_and_save, fetch_current_data
from schemas.stock import StockCurrentSchema, StockSchema, StocksCodeSchema

scs = StocksCodeSchema()
sc_many = StockSchema(many=True)
stock_curr_schema = StockCurrentSchema()


@app.route('/stocks/<name>', methods=['GET'])
def fetch_current_stock_listing(name):
    stock_code_response = StocksCodeModel.find_by_name(name)
    if stock_code_response is not None and 'Item' in stock_code_response:
        stock_code = scs.load(stock_code_response['Item'])
        print(stock_code)
        print(type(stock_code))
        if stock_code:
            scm = fetch_current_data(stock_code)
            return stock_curr_schema.dump(scm)
    return jsonify({"message": f"Stock listings for {name} not found."}), 404


@app.route('/stocks/historical/<string:name>', methods=['GET'])
def fetch_stock_listings(name):
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from is not None:
        if date_to is None:
            stock_listings_response = StockModel.fetch_listings_by_name_and_date(name, date_from)
        else:
            stock_listings_response = \
                StockModel.fetch_listings_by_name_and_daterange(name,date_from, date_to)
    else:
        stock_listings_response = StockModel.fetch_listings_by_name(name)
    # process stock_listings_response response
    if stock_listings_response is not None and 'Items' in stock_listings_response:
        return {"stocks": sc_many.dump(stock_listings_response['Items'])}
    return jsonify({"message": f"Stock listings for {name} not found."}), 404


@app.route('/stocks/refresh/<string:name>', methods=['POST'])
def refresh_stock_listings(name):
    stock_code_response = StocksCodeModel.find_by_name(name)
    if stock_code_response is not None and 'Item' in stock_code_response:
        stock_code = scs.load(stock_code_response['Item'])
        if stock_code:
            scrape_and_save(stock_code)
            return jsonify({"message": f"Stock {name} listings fetched and updated."})
    return jsonify({"message": f"Stock {name} not found. Please add entity using /stocks_code "
                               f"API."}), 404


@app.route('/stocks/<name>', methods=['DELETE'])
def delete_stock_listings(name):
    stock_code_response = StocksCodeModel.find_by_name(name)
    if stock_code_response is not None and 'Item' in stock_code_response:
        stock_code = scs.load(stock_code_response['Item'])
        if stock_code:
            StockModel.delete_from_db(stock_code)
            return jsonify({"message": f"Stock {name} listings deleted."})
    return jsonify({"message": f"Stock {name} not found."}), 404

