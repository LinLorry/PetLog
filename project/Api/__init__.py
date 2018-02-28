from flask import Blueprint
from flask_restful import Api
from .Auths import auth, use_auth
from .Registered import registered, verify_email, user_avatar
from .Card import get_tags, post_card, card_comment, praise_interface
from .Card import u_get_circle_of_friends, u_get_timeline, u_get_card_detail
from .Card import get_hot_card, get_other_all_cards
from .Card_images import upload_card_image
from .Business import follow_interface, upload_avatar, get_followers, get_followings
from .Business import user_profile_summary, user_profile, update_user, user_other_profile
from .PetBusiness import create_pet, get_user_all_pet, pet_avatar, get_pet_detail, update_pet

API_blueprint = Blueprint('API', __name__)
api = Api(API_blueprint)

api.add_resource(auth, "/login")
api.add_resource(use_auth, "/auth")

api.add_resource(registered, "/registered")
api.add_resource(verify_email, "/registered/verify_code")
api.add_resource(user_avatar, "/user/avatar")
api.add_resource(update_user, "/user/update")

api.add_resource(get_tags, "/tags/get_tags")
api.add_resource(post_card, "/user/post_card")
api.add_resource(card_comment, "/user/post_comment")
api.add_resource(praise_interface, "/user/post_praise")
api.add_resource(upload_card_image, "/upload/card_image")

api.add_resource(u_get_timeline, "/user/get_timeline/")
api.add_resource(u_get_circle_of_friends, "/user/get_circle_of_friends")
api.add_resource(u_get_card_detail, "/card/")
api.add_resource(get_hot_card, "/get_hot")
api.add_resource(get_other_all_cards, "/get_cards")

api.add_resource(follow_interface, "/user/focus/")
api.add_resource(get_followers, "/user/get_followers")
api.add_resource(get_followings, "/user/get_followings")

api.add_resource(user_profile_summary, "/user/profile_summary")
api.add_resource(user_profile, "/user/profile")
api.add_resource(user_other_profile, "/user/profile_other")

api.add_resource(update_pet, "/user/pet/update")
api.add_resource(create_pet, "/user/pet/create_pet")
api.add_resource(get_user_all_pet, "/user/pet/all_pets")
api.add_resource(pet_avatar, "/user/pet/avatar")
api.add_resource(get_pet_detail, "/user/pet/detail/")
