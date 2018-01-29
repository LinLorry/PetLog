from flask import Blueprint
from flask_restful import Api
from .test import test

Test_blueprint = Blueprint('Test',__name__)
api = Api (Test_blueprint)
api.add_resource (test,"/testpostimage")