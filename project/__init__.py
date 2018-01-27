from flask import Flask

#参数config_name还没完成
def create_app(config_name):
    app = Flask(__name__)

    #max post 最大上传文件大小16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    #Buleprint
    from .api import API
    app.register_blueprint (API)

    return app
