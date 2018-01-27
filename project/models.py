from werzeug.security import generate_password_hash, check_password_hash

#用户模块
class User:
    #tablename is 'users'
    __tablename__ = 'users'
    #user_id is 16 characters
    __user_id = '123456789ABCDEF'
    __user_name = 'name'

    #为password加上修饰器@property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    #校验密码方法
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #返回用户的名字的方法
    def get_user_name (self):
        return self.__user_name

    #返回用户id的方法
    def get_user_id (self):
        return self.__user_id



