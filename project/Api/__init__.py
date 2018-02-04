from flask import Blueprint
from flask_restful import Api
from .Auths import auth
from .Registered import registered,verify_code
from .Card import post_card,user_get_card,guest_get_card
from .Card_images import upload_card_images,download_card_images

API_blueprint = Blueprint('API',__name__)
api = Api (API_blueprint)

api.add_resource (auth,"/login")

api.add_resource (registered,"/registered")
api.add_resource (verify_code,"/registered/verify_code")

api.add_resource (post_card,"/user/post_card")
api.add_resource (user_get_card,"/user/get_card")
api.add_resource (guest_get_card,"/guest/get_card")

api.add_resource (upload_card_images,"/upload/card_images")
api.add_resource (download_card_images,"/download/card_images")
