from flask import request, jsonify
from database import db_session
from app import app


@app.route('/stocks/<string:name>', methods=['GET'])
def fetch_stock(name):
    return {"message": f"Fetching stocks for {name}"}


@app.route('/stocks/refresh/<string:name>', methods=['POST'])
def refresh_stock(name):
    return jsonify({"message": f"Fetching stocks for {name}"})
