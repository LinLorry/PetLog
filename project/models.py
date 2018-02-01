from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import time
import uuid
from . import db

#关于这个库，上面的itsdangerous的使用时差不多效果的，所以就使用上面那个了
''' import hashlib '''

#加载程序配置用到current_app
from flask import current_app,g

#用户模块
#现在先优先完成用户的注册方法和卡片的创造方法
class User(db.Model):
    #tablename is 'users'
    __tablename__ = 'users'
    #限制变量的访问，加"__"
    __id = db.Column(db.String(16),primary_key=True,nullable=False)
    __user_name = db.Column(db.String(20),unique=True,nullable=False)
    __user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    __password_hash = db.Column(db.String(128),nullable=False)
    __phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    __gender = db.Column(db.String(1),nullable=True)
    __head_portrait_path = db.Column(db.String(128),nullable=True)
    __motto = db.Column(db.String(256),nullable=True)
    __address = db.Column(db.String(30),nullable=True)
    __joined_time = db.Column(db.Datetime,nullable=False,default=datetime.now)
    __grade = db.Column(db.Integer,nullable=False,default=1)

    #user_id is 16 characters
    #__user_id = '123456789ABCDEF'

    #构造函数，接口使用的时候要通过这个确定用户
    def __init__(self,username,user_id = None):
        #如果没有user_id就使用username来构造对象
        if user_id is None:
            self.__user_name = username
            #这个是为了测试，所以将密码设置的和用户名一样
            self.password = username
        else:
            self.__id = user_id

        #根据username 或者 id 初始化一个用户对象......

    #添加新用户的方法
    #参数是用户信息得到字典
    def __init__(self,user_dict):

        
        
        #生产用户的唯一id
        self.__id = uuid.uuid1()
        #用户生成的时间，姑且先用时间戳的形式存着，不知道后面会不会用到
        self.__joined_time = time.time()

        #对于必须拥有的变量调用赋值即可
        self.__user_name = user_dict['username']
        self.__user_nickname = user_dict['user_nickname']
        self.password = user_dict['password']
        
        #对于不一定拥有的变量调用set设置器
        #有些设置器还未写,需要补充
        self.set_user_gender(user_dict)
        self.set_phonenumber(user_dict)
        self.set_motto(user_dict)
        #......
        
        ''' str1 = user_name
        str2 = time.time()
	    str3 = "new people"
        str4 = str1+str(str2)+str3
	    raw = hashlib.md5()
	    raw.update(str4.encode("utf8"))
	    result = raw.hexdigest()[8:-8] '''

        #插入数据的操作......

        return True

    
    class __card(db.Model):
        #用户的私有类:卡片
        #还没完善,插入的方法还没有......

        #用于用户查找他的卡片的方法
        def __init__(self,user_name):
            #这里应该是用用户名去查找表中的user_id ，然后再赋值给user_id
            self.__user_id = user_name

        #创造用户卡片的方法
        def __init__(self,content,images,tags):
            
            #卡片id的生成
            self.__id = uuid.uuid1()

            ''' str1 = user_id
            str2 = time.time()
	        str3 = "new card"
	        str4 = str1+str(str2)+str3
	        raw = hashlib.md5()
	        raw.update(str4.encode("utf8")
	        result = raw.hexdigest()[8:-8] '''

            self.__content = content
            self.__images = images
            self.__tags = tags
            self.__time = time.time()

        #def insert(self):......

    class Pet(db.Model):
        #用户的私有类:宠物

        #宠物的构造函数，用于查找一个宠物
        def __init__(self,pet_name):
            self.__pet_anme = pet_name

        #宠物的构造函数，用于查找一个用户的宠物
        def __init__(self,user_name,pet_name):
            #这里应该是用用户名去查找表中的user_id ，然后再赋值给user_id
            self.__user_id = user_name
            self.__pet_anme = pet_name

        #宠物的构造函数,用于创建一个宠物
        #pet_dict时一个包含宠物信息的字典
        #接口已经调用了构造函数生成用户对象，可以直接self.xxx来取变量值
        #这个方法要将动物信息插入表中，具体有什么信息请查看产品数据要求
        def __init__(self,\
                pet_id,\
                category,\
                pet_name,\
                user_id,\
                gender):

            #宠物唯一id的生成
            #新方法
            self.__id = uuid.uuid1()
            #旧方法
            ''' str1 = self.__id
            str2 = time.time()
            str3 = "new pet"
    	    str4 = str1+str(str2)+str3
	        raw = hashlib.md5()
	        raw.update(str4.encode("utf8"))
	        result = raw.hexdigest()[8:-8] '''

    
    #为password加上修饰器@property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #稍微修改了密码的hash算法
    #密码hash用"密码+用户名+salt"的方法来算
    @password.setter
    def password(self,password):
        self.__password_hash = pwd_context.encrypt(password + \
                                            self.__user_name + \
                                            current_app.config['SALT'])
    
    #校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(password + \
                                self.__user_name + \
                                current_app.config['SALT'],\
                                self.password_hash)
    
    #返回用户的名字的方法
    def get_user_name (self):
        return self.__user_name

    #返回用户id的方法
    def get_user_id (self):
        return self.__user_id

    #设置用户的性别的方法
    #查看字典是否有该属性
    def set_user_gender (self,user_dict):
        if user_dict['gender'] == '':
            user_dict['gender'] = None
        self.__gender = user_dict['gender']
        return True

    #设置用户的电话号码
    def set_phonenumber (self,user_dict):
        if user_dict['phonenumber'] == '':
            user_dict['phonenumber'] = None
        self.__gender = user_dict['phonenumber']
        return True
            
    #获取token的方法，默认时间是10分钟(10*60秒)
    #密钥使用配置属性，配置属性来自系统变量在project.__init__.py里
    #加上用户名好在检查token结束后，构造用户对象
    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'],\
                    expires_in = expiration)
        return s.dumps({ 'id': self.__id ,\
                        'username':self.__user_name})



    #用户创造卡片的方法
    def create_card(self,card_dict):

        #创造卡片对象
        card = self.__card(card_dict['content'],\
                        card_dict['images'],\
                        card_dict['tags'])

        #插入数据的方法可以为card类加方法
        #card.insert()

        return True

    #计算用户当前等级的方法
    def grade_now(self,grade,user_id,comment_number,praise_number):
	    #具体计算待定
	    return grade
