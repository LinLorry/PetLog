from flask import Blueprint
from flask_restful import Api
from .Auths import auth,use_auth
from .Registered import registered,verify_email, new_user_avatar
from .Card import get_tags, post_card,card_comment,praise_interface,card_comment,u_get_circle_of_friends,u_get_timeline,u_get_card_detail,u_get_hot_card
from .Card_images import upload_card_image,download_card_image
from .Business import follow_interface,upload_avatar
from .PetBusiness import create_pet, get_user_all_pet

API_blueprint = Blueprint('API',__name__)
api = Api (API_blueprint)

api.add_resource (registered,"/registered")
api.add_resource (new_user_avatar,"/registered/new_avatar")
api.add_resource (verify_email,"/registered/verify_code")

api.add_resource (auth,"/login")
api.add_resource (use_auth,"/auth")

api.add_resource (create_pet,"/user/create_pet")
api.add_resource (get_user_all_pet,"/user/all_pets")

api.add_resource (get_tags,"/tags")
api.add_resource (post_card,"/user/post_card")
api.add_resource (card_comment,"/user/post_comment")
api.add_resource (praise_interface,"/user/post_")
api.add_resource (u_get_card_detail,"/card")
api.add_resource (u_get_circle_of_friends,"/user/get_circle_of_friends")

api.add_resource (upload_card_image,"/upload/card_image")

api.add_resource (follow_interface,"/user/focus/")
