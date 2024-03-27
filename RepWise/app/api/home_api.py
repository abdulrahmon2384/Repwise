from flask import Blueprint, jsonify, request
from RepWise.app import app, db
from RepWise.app.functions import *

api_home_bp = Blueprint('home', __name__)




@api_home_bp.route('/api/user-info')
def api():
	headers = request.headers
	if not headers:
		return jsonify({}), 400

	username = request.headers.get('X-Replit-User-Name')
	user_id = request.headers.get('X-Replit-User-Id')
	roles = request.headers.get('X-Replit-User-Roles')
	data = {"name": username, "id": user_id, "roles": roles, "test": "data"}
	return jsonify(data), 200


@app.route("/api/validate/<username>", methods=['GET'])
def CompletionStatus(username):
        if not username :
            return jsonify({"message": "Username is required"}), 400

        if username not in db.get('Users', {}):
            return jsonify({"message": "User not found"}), 400

        bool = isUserCompletionStatus(username)
        return jsonify({"CompletionStatus":bool})





@app.route('/api/checkbox-values', methods=['POST'])
def store_values():
    values = request.json.get('values', [])
    username = request.headers.get('X-Replit-User-Name')

    print('CHeckbox values', values)
    successfull = append_requirment_agreed([values, username])
    return jsonify({'message': 'Values stored successfully'}), 200






@app.route('/api/all-feeds', methods=['GET'])
def get_categories():
	try:
		categories_data = db.get("categories")
		categories_json = convert_to_dict(categories_data)
		
		if "eMPTy" in categories_json:
			return jsonify({"categories":{}}), 200
			
		return jsonify({"categories": categories_json}), 200
	except :
		return jsonify({}), 500




@app.route('/api/userAgreementId')
def agreement_id():
	username = request.headers.get('X-Replit-User-Name')
	user_data = db["Users"].get(username)
	
	if not user_data:
		return jsonify(
			{
			   "message": f"User {username} not found ",
			"agreementid": {}
			}), 400
		
	agreement_id = user_data.get('requirment_agreed',[])
	return jsonify({
		     "agreementid": 
		              {id:id for id in agreement_id if id}
	            }), 200

