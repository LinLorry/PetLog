### url为:host:5000/api/user/......  的接口需要验证登陆的请求,请求头上带上"Authorization":token\[:str\],过期时间为600s

#### token过期会返回

{

"status":0

"message":"failed"

}

### **系统环境变量：**

PetLog\_SALT:保存密码使用的“盐”

PetLog\_DATABASE:数据库URL

PetLog\_SECRET\_KEY:密钥

PetLog\_REGISER\_KEY:注册用户时的加密密钥

PetLog\_CARD\_IMAGES:用户的图片的存储路径

PetLog\_MAIL\_USERNAME:邮箱系统账号

PetLog\_MAIL\_PASSWORD:邮箱系统密码

### API：

#### 1.url:host:5000/api/login                                                  methods:"POST"

##### params:

{

```
"username":username[:str]

"password":password[:str]
```

}

##### return:

{

```
"status":1
"token":token[:str]
```

}

#### 2.url:host:5000/api/upload/card\_images                        methods:"POST"

##### success return:

{

```
"status":1,

"filename":filename[:str]
```

}

##### failed return:

{

```
"status":0,

"message":"failed"
```

#### }

#### 3.url:host:5000/api/user/post\_card                                methods:"POST"

##### params:

{

```
"conntent":Text[:any],

"images":Array[:text],

"tags":Array[:text],

"time":[:"YYYY年(M)M月DD日 hh:mm"]
```

}

##### return:

{

```
"status":1,

"message":"success"
```

}

#### 4.url:host:5000/api/user/post\_comment                         methods:"POST"

##### params:

{

"id":card\_id\[:text\]

"comment":comment\[:text\]

"remind":@user\_email\[:array\]

}

##### return:

{

"status":1

"message":"success"

}

#### 5.url:host:5000/api/user/post\_praise                              methods:"POST"

##### params:

{

"_id":card\_id\[:text\]_

}

##### return: {

"status":1

"message":"success"

}

#### 6.url:host:5000/api/user/del\_praise                             methods:"POST"

##### params:

{

"id":card\_id\[:text\]

}

##### return: {

 "status":1

"message":"success"

}

