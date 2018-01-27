#测试上传图片的api

from flask import request,send_from_directory
from . import API
from werkzeug import secure_filename
import os

#上传文件的限制格式
ALLOWED_EXTENSIONS = set (['jpg','png','jpeg'])

#限制上传文件的格式函数
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#上传图片的接口
@API.route ("/api/postimage",methods = ['GET','POST'])
def postimage ():
    #get无意义
    if request.method == 'GET':
        return "sss"
    else:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save (os.path.join(os.getenv("PET_USER_IMAGES"),filename))
            #文件上传成功，返回"success"
            return "success"
        #没有文件或文件格式不是允许的文件格式，返回"f",失败
        return "f"

#获取上传文件的接口
@API.route ("/api/getimage/<filename>",methods = ['GET'])
def getimage (filename):
    return send_from_directory(os.path.join(os.getenv("PET_USER_IMAGES"),filename))


