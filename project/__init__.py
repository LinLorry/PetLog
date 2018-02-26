import os
from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

#参数config_name还没完成
def create_app(config_name):
    app = Flask(__name__)
    if config_name == "test":
        app.config['SECRET_KEY'] = "key"
        app.config['CARD_IMAGES_FOLDER'] = "自己决定"
        app.config['SALT'] = "salt"
        app.config['SQLALCHEMY_DATABASE_URI'] = \
                    r"mysql://username:password@hostname/database"
        app.config['REGISER_CODE'] = "asd"
        from .Api import API_blueprint
        app.register_blueprint (API_blueprint,url_prefix='/testapi')
        
    else:
        app.config['SECRET_KEY'] = os.getenv("PETLOG_SECRET_KEY")
        app.config['CARD_IMAGES_FOLDER'] = os.getenv("PETLOG_CARD_IMAGES")
        app.config['SALT'] = os.getenv("PETLOG_SALT")
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("PETLOG_DATABASE")
        app.config['REGISER_CODE'] = os.getenv("PETLOG_REGISER_KEY")
        #Buleprint
        from .Api import API_blueprint
        app.register_blueprint (API_blueprint,url_prefix='/api')
    
    #email
    app.config['IMAGE_ALLOWED_EXTENSIONS'] = set(['jpg', 'png', 'jpeg'])
    app.config['MAIL_SERVER'] = 'smtp.lenconda.top'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = os.environ.get('PETLOG_MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('PETLOG_MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'PETLOG <noreply@lenconda.top>'  
    mail.init_app(app)

    #max post 最大上传文件大小16MB
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['USER_AVATAR_FOLDER'] = os.environ.get('PETLOG_USER_AVATAR_FOLDER')
    app.config['PET_AVATAR_FOLDER'] = os.environ.get('PETLOG_PET_AVATAR_FOLDER')
    db.init_app(app)
    
    return app


