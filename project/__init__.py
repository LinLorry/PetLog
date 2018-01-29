from flask import Flask,Blueprint
import os

#参数config_name还没完成
def create_app(config_name):
    app = Flask(__name__)

    #max post 最大上传文件大小16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['SECRET_KEY'] = os.getenv("PETSHOW_SECRET_KEY")

    #Buleprint
    from .Test import Test_blueprint
    from .Api import API_blueprint
    app.register_blueprint (Test_blueprint,url_prefix='/testapi')
    app.register_blueprint (API_blueprint,url_prefix='/api')
    
    return app
