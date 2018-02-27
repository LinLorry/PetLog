# !/bin/python3
# -*- coding:utf-8 -*-

from project import create_app
import os

app = create_app("")

if __name__ == "__main__" :
    print (os.getenv("PETLOG_SECRET_KEY"))
    print (os.getenv("PETLOG_CARD_IMAGES"))
    print (os.getenv("PETLOG_SALT"))
    print (os.getenv("PETLOG_DATABASE"))
    print (os.getenv("PETLOG_REGISER_KEY"))
    print (os.environ.get('PETLOG_MAIL_USERNAME'))
    print (os.environ.get('PETLOG_MAIL_PASSWORD'))
    print (os.environ.get('PETLOG_USER_AVATAR_FOLDER'))
    print (os.environ.get('PETLOG_PET_AVATAR_FOLDER'))
    app.run ()
