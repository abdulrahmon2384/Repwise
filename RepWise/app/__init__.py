from flask import Flask, render_template, jsonify, request
from replit import db
import json


app = Flask(__name__, template_folder='templates')



from RepWise.app import routes, api, functions
from RepWise.app.routes import routes_blueprint
from RepWise.app.api import api_blueprint


app.register_blueprint(routes_blueprint)
app.register_blueprint(api_blueprint)


from RepWise.app.functions import initialize_database
initialize_database(db)

db["categories"] = {}


