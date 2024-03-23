from flask import Blueprint, jsonify, request
from RepWise.app import app, db
from RepWise.app.functions import *
import json

api_home_bp = Blueprint('home', __name__)


@api_home_bp.route('/api/user-info')
def api():
	headers = request.headers
	if 'X-Replit-User-Name' not in headers or 'X-Replit-User-Id' not in headers or 'X-Replit-User-Roles' not in headers:
		return jsonify({}), 400

	username = request.headers.get('X-Replit-User-Name')
	user_id = request.headers.get('X-Replit-User-Id')
	roles = request.headers.get('X-Replit-User-Roles')

	data = {"name": username, "id": user_id, "roles": roles, "test": "data"}
	return jsonify(data), 200





@app.route('/api/validate')
def validate():
	whitelist = db['whitelist']
	username = request.headers.get('X-Replit-User-Name')
	
	if username in whitelist:
		return jsonify({"valid": True}), 200
	else:
		return jsonify({"valid": False}), 200


@app.route('/api/store-values', methods=['POST'])
def store_values():
    data = request.json
    values = data.get('values', [])
    print(values)
    if not values or len(values) != 2:
        return jsonify({'message': "Values can't be empty"}), 400
    
    store_values_in_db(values)
    return jsonify({'message': 'Values stored successfully'}), 200



@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories_data = db["categories"]
    categories_json = convert_to_dict(categories_data)
    return jsonify({"categories": categories_json}), 200
	


