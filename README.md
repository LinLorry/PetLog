### url为:host:5000/api/user/......  的接口需要验证登陆的请求,请求头上带上"Authorization":token\[:str\],过期时间为600s

#### token过期会返回

{

"status":0

"message":"failed"

}

### **系统环境变量：**

PETLOG\_SALT:保存密码使用的“盐”

PETLOG\_DATABASE:数据库URL

PETLOG\_SECRET\_KEY:密钥

PETLOG\_REGISER\_KEY:注册用户时的加密密钥

PETLOG\_CARD\_IMAGES:用户的图片的存储路径

PETLOG\_MAIL\_USERNAME:邮箱系统账号

PETLOG\_MAIL\_PASSWORD:邮箱系统密码

### API：

#### url:host:5000/api/login                                                  methods:"POST"

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

#### url:host:5000/api/registered                           methods:"POST"

##### params:

`{`

`"email":user_email[:str],`

`"password":"user_password[:str]`

`"phonenumber":user_phonenumber[:str],`

`"user_nickname":user_nickname[:str],`

`"address":user_address[:str],`

`"gender":user_gender[:str],`

`"joined_time":"2018-10-01 21:45:54",`

`"motto":""`

`}`

##### return:

{

```
"status":1,
"message":"success"
```

}

#### url:host:5000/api/user/create\_pet               methods="POST"

params:

`{`

`"gender":pet_gender[:str],`

`"pet_name":pet_name[:str]`

`"category":category[:str],`

`"detailed_category":detailed_category[:str],`

`“pet_avatar_path“：pet_avatar_path[:str],`

`"time":time`

`}`

#### url:host:5000/api/upload/card\_images                        methods:"POST"

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

#### url:host:5000/api/user/post\_card                                methods:"POST"

##### params:

{

```
"conntent":Text[:any],

"images":Array[:text],

"pet_id":pet_id[:str],

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

#### url:host:5000/api/user/post\_comment                         methods:"POST"

##### params:

`{`

`"id":card_id[:text],`

`"comment":comment[:text],`

`"remind":@user_email[:array]`

`}`

##### return:

`{`

`"status":1,`

`"message":"success"`

`}`

#### url:host:5000/api/user/post\_praise                              methods:"POST"

##### params:

`{`

`"id":card_id[:text]`

`}`

##### return:

##### `{`

`"status":1,`

`"message":"success"`

`}`

#### url:host:5000/api/user/del\_praise                             methods:"POST"

##### params:

`{`

`"id":card_id[:text]`

`}`

##### return:

##### `{`

`"status":1,`

`"message":"success"`

`}`

