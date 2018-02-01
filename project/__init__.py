from flask import Flask,Blueprint
import os

#参数config_name还没完成
def create_app(config_name):
    app = Flask(__name__)
    if config_name == "test":
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        app.config['SECRET_KEY'] = "key"
        app.config['CARD_IMAGES_FOLDER'] = "自己决定"
        app.config['SALT'] = "salt"
        app.register_blueprint (Test_blueprint,url_prefix='/testapi')
        from .Test import Test_blueprint
    else:
        #max post 最大上传文件大小16MB
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

        app.config['SECRET_KEY'] = os.getenv("PETSHOW_SECRET_KEY")
        app.config['CARD_IMAGES_FOLDER'] = os.getenv("PETSHOW_CARD_IMAGES")
        app.config['SALT'] = os.getenv("PETSHOW_SALT")
    
        #Buleprint
        from .Api import API_blueprint
        app.register_blueprint (API_blueprint,url_prefix='/api')
    
    return app
