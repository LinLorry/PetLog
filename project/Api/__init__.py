from flask import Blueprint
from flask_restful import Api
from .Auths import auth

API_blueprint = Blueprint('API',__name__)
api = Api (API_blueprint)
api.add_resource (auth,"/Login")