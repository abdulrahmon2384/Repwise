from flask import Blueprint
from RepWise.app import app

routes_blueprint = Blueprint('routes', __name__)

from RepWise.app.routes.home import home_bp

routes_blueprint.register_blueprint(home_bp)