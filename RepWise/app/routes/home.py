from flask import Flask, render_template, jsonify, request, Blueprint
from RepWise.app import app, db
from RepWise.app.functions import *

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
		username = request.headers.get("X-Replit-User-Name")

		whitelist = db.get('whitelist', {}).keys()
		if username not in whitelist:
			return render_template('home/notallow.html', username=username)


		isempty = is_database_empty(db)
		json_data = db.get('categories', {})
		latest_requirement = get_latest_values_by_category(json_data, username)
		latest = get_latest_values_by_category(json_data)
		last_updated = time_since_last_update(latest)

		return render_template('home/index.html',
							   username=username,
							   latest_requirement=latest_requirement,
							   last_updated=last_updated,
							   isempty=isempty,
							   db=db)
