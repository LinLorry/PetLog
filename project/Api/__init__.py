from flask import Blueprint
from flask_restful import Api
from .Auths import auth
from .Card import post_card,user_get_card,guest_get_card
from .Card_images import upload_card_images,download_card_images

API_blueprint = Blueprint('API',__name__)
api = Api (API_blueprint)

api.add_resource (auth,"/Login")

api.add_resource (post_card,"/user/Post_card")
api.add_resource (user_get_card,"/user/Get_card")
api.add_resource (guest_get_card,"/guest/Get_card")

api.add_resource (upload_card_images,"/Upload/card_images")
api.add_resource (download_card_images,"/Download/card_images")
