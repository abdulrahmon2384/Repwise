from flask import Flask, render_template, jsonify, request
from replit import db


app = Flask(__name__, template_folder='templates')



from RepWise.app import routes, api, functions
from RepWise.app.routes import routes_blueprint
from RepWise.app.api import api_blueprint


app.register_blueprint(routes_blueprint)
app.register_blueprint(api_blueprint)


if len(db.keys()) == 0:
    db['whitelist'] = dict()
    db['categories'] = dict()


#Uncomment below code for generating fake requirements 
#from RepWise.app.generate_fake_data import data
#db["categories"] = data


