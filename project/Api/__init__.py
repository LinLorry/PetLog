from flask import Blueprint
from flask_restful import Api
from .Auths import auth,use_auth
from .Registered import registered,verify_code
from .Card import post_card,card_comment,user_get_card,guest_get_card
from .Card_images import upload_card_image,download_card_image
from .Business import follow_interface

API_blueprint = Blueprint('API',__name__)
api = Api (API_blueprint)

api.add_resource (auth,"/login")
api.add_resource (use_auth,"/auth")

api.add_resource (registered,"/registered")
api.add_resource (verify_code,"/registered/verify_code")

api.add_resource (post_card,"/user/post_card")
api.add_resource (card_comment,"/user/post_comment")

api.add_resource (user_get_card,"/user/get_card")
api.add_resource (guest_get_card,"/guest/get_card")

api.add_resource (upload_card_image,"/upload/card_image")
api.add_resource (download_card_image,"/download/card_image/<string:filename>")

api.add_resource (follow_interface,"/user/focus/")
