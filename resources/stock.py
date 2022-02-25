from flask import request, jsonify
from app import app
from model.stock import StockModel, StocksCodeModel, StockCurrentModel
from services.scrapedata import scrape_and_save, fetch_current_data
from schemas.stock import StockCurrentSchema


@app.route('/stocks/<name>', methods=['GET'])
def fetch_current_stock_listing(name):
    stock_code = StocksCodeModel.find_by_name(name)
    if stock_code is not None:
        sc = StockCurrentSchema()
        scm = fetch_current_data(stock_code)
        return sc.dump(scm)
    return jsonify({"message": f"Stock listings for {name} not found."}), 404


@app.route('/stocks/historical/<string:name>', methods=['GET'])
def fetch_stock_listings(name):
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if date_from is not None:
        if date_to is None:
            stock_listings = StockModel.fetch_listings_by_name_and_date(name, date_from)
        else:
            stock_listings = StockModel.fetch_listings_by_name_and_date(name, date_from, date_to)
        if stock_listings is not None:
            # Doing x[0] since list of tuple is returned
            return jsonify({"stocks": list(map(lambda x: x[0].json(), stock_listings))})
    else:
        stock_listings = StockModel.fetch_listings_by_name(name)
        if stock_listings is not None:
            return jsonify({"stocks": list(map(lambda x: x.json(), stock_listings))})
    return jsonify({"message": f"Stock listings for {name} not found."}), 404


@app.route('/stocks/refresh/<string:name>', methods=['POST'])
def refresh_stock_listings(name):
    stock = StocksCodeModel.find_by_name(name)
    if stock is not None:
        scrape_and_save(stock)
        return jsonify({"message": f"Stock {name} listings fetched and updated."})
    return jsonify({"message": f"Stock {name} not found. Please add entity using /stocks_code "
                               f"API."}), 404


@app.route('/stocks/<name>', methods=['DELETE'])
def delete_stock_listings(name):
    stock = StocksCodeModel.find_by_name(name)
    if stock is not None:
        StockModel.delete_from_db(stock)
        return jsonify({"message": f"Stock {name} listings deleted."})
    return jsonify({"message": f"Stock {name} not found."}), 404

