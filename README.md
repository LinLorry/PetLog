### **系统环境变量：**

PETSHOW\_SECRET\_KEY:密钥

PETSHOW\_CARD\_IMAGES:用户的图片的存储路径

### API：

#### 1.url:host:5000/api/Login                             methods:"POST"

##### params:

{

```
"username":username,str,

"password":password,str
```

}

##### return:

{

```
"status":1
"token":token,str
```

}

#### 2.url:host:5000/api/Upload/card\_images         methods:"POST"

##### success return:

{

```
"status":1,

"filename":filename,str
```

}

##### failed return:

{

```
"status":0,

"message":"failed"
```

}

### 3.url:host:5000/api/Post\_card            methods:"POST"

##### params:
{

```
"conntent":Text\[:any\],

"images":Array\[:text\],

"tags":Array\[:text\],

"time":\[:"YYYY年\(M\)M月DD日 hh:mm"\],

"status":pet_status\[:int\]
```

}

##### return: 

{

```
"status":1,

"message":"success"
```

}

