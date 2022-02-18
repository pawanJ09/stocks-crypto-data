from flask import Flask, jsonify, request
import globals


app = Flask(__name__)


@app.route('/entities')
def fetch_all_entities():
    return jsonify(globals.entity_dict)


@app.route('/entity/<string:name>')
def fetch_entity_by_name(name):
    if name in globals.entity_dict:
        return {f"{name}": f"{globals.entity_dict[name]}"}
    return {"message": f"{name} not found"}, 404


@app.route('/entity/<string:name>', methods=['POST'])
def add_entity_by_name(name):
    data = request.get_json()
    globals.entity_dict[name] = data['code']
    return {f"{name}": f"{globals.entity_dict[name]}"}, 201


@app.route('/entity/<string:name>', methods=['DELETE'])
def delete_entity_by_name(name):
    if name in globals.entity_dict:
        globals.entity_dict.pop(name, 'Not found')
        return {"message": f"{name} deleted"}
    return {"message": f"{name} not found"}, 404


app.run(port=5000, debug=True)




