from flask import Flask, render_template, jsonify, request, Blueprint
from RepWise.app import app, db
from RepWise.app.functions import *

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
	username = request.headers.get("X-Replit-User-Name")
	whitelist = db.get("Users", {}).keys()
	if username not in whitelist:
		add_user(username)

	last_updated = time_since_last_update(db)
	return render_template('home/index.html',
	                       username=username,
	                       last_updated=last_updated)
