from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from RepWise.app.api.home_api import api_home_bp

api_blueprint.register_blueprint(api_home_bp)