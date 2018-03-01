# PetLog  
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

## API说明：

### 用户注册及登录:
#### url: host:5000/api/registered  (注册)
##### methods:"POST"
Request:
```
{
    "email": Text,
    "password": Text,
    "user_nickname": Text,
    "address": Text,
    "gender": Text[male/female],
    "register_key": MD5 SHA1-32
}
```
Response:
```
{
    "status":1/0
    "message":"success"/"failed"
}
```
#### url: host:5000/api/registered/verify_code  (邮箱认证）
##### methods:"POST"
Request:
```
{
    "email":Text
}
```
Response:
```
{
    "status":1               “status":0
    "code":                  "message":failed
}
```

#### url: host:5000/api/auth  (检查是否登录状态下)
##### methods:"GET"
Request:
```

```

Response:
```
{
    "status":1/0,
    "message: "ok"/"failed"
}
```
#### url: host:5000/api/login (登录）  
##### methods:"POST"
Request:
```
{
    "email":Text,
    "password":Text
}
```

Response:
```
{
    "status":1,         "status":0,
    "token":            "message":"failed"
}
```
### 用户个人信息查询及更改
#### url: host:5000/api/user/profile(个人信息获取)
##### methods:"GET"
Response:
```
{
    ”status:1/0 （是否登录）
    "message:
    "user":{
        "name":Text,
        "avatar":Text,
        "motto":Text,
        "gender":Text,
        "birth_day":YYYY-MM-DD,
        "location":Text
    }
}
```
#### url: host:5000/api/user/avatar(头像上传）
##### methods:"POST"
Request:
```
{
    multipart/form-data
}
```

Response:
```
{
    "status":1,                 "status":0,
    "filename":                 "message":"faied"
}
```
#### url: host:5000/api/user/update(修改用户个人资料)
##### methods:"POST"
Request:
```
{
    "name":Text,
    "avatar":Text,
    "motto":Text,
    "gender":Text,
    "birth_day":YYYY-MM-DD,
    "location":Text
}
```

Response:
```
{
    "status":1,                   "status":0,
    "message":"success"           "message":"failed"
}
```
### 用户操作
#### url: host:5000/tags/get_tags(获取所有Tag)
##### methods:"GET"
Response:
```
{
    "status":1,        "status":0,
    "tags":Array       "tags":Array
}
```
#### url: host:5000/user/post_card(发布动态)
##### methods:"POST"
Request:
```
{
    "content":Text,
    "status":Text,
    "tags":Array,
    "images":Array,
    "for":Text
}
```

Response:
```
{
    "status":1,     "status":0,
    "message":"success"   "message":"failed"
}
```
#### url: host:5000/api/user/post_comment(发表评论）
##### methods:"POST"
Requuest:
```
{
    "card_id":Text,
    "to_author":Bool,
    "reply_to":Text,
    "content":Text
}
```

Response:
```
{
    "status":1,          "status":0,
    "message":
    "time":
}
```
#### url: host:5000/api/user/post_praise(点赞）
##### methods:"POST"
Request:
```
{
    "id",Text,
    "action":1/0
}
```

Response:
```
{
    "status":1/0,
    "message":"success"/"fail"
}
```
#### url: host:5000/api/upload/card_image(上传卡片的图片）
##### methods:"POST"
Request:
```
{
    multipart/form-data
}
```

Response:
```
{
    "status":1/0,
    "filename":
}
```
#### url: host:5000/user/get_timeline/(时间轴内容）
##### methods:"GET"
Response:
```
{
    "status" : 0,
    "message" : "你没有权限获得该宠物的时间轴"/
    "status"1,
    message: Text, 
    name: Text, //宠物昵称
    age: Int, //根据添加宠物时提供的出生日期计算
    avatar: Text, //宠物头像
    motto: Text, //宠物简介
    items: [
        {
            // 非年份时
            date: (M)M-(D)D,
            is_year: false,
            items: [
                {
                    content: Text,
                    images: Array,
                    status: Text,
                    id: Text
                },
                {
                    ...
                }
            ]
        },
        {
            //是年份时， “”、[]均代表空值
            date: "",
            items: [],
            is_year: true,
            year: Int
        }
    ]
}
```
#### url: host:5000/user/get_circle_of_friends(获取朋友圈内容)
##### methods:"GET"
Response:
```
{
    status: 1/0, //用户是否登录的标识符
    infinited: Bool, //如果取完所有卡片，返回true，否则返回false
    cards: [
        {
            id: Text,
            author: {
                name: Text,
                id: Text,
                avatar: Text,
                followed: Bool
            },
            liked: Bool,
            post: {
                time: YYYY年(M)M月(M)M日 hh:mm，
                content: Text,
                status: Text, //记录宠物状态
                tags: Array,
                likes: Int,
                images: Array
            },
            comments: Int //评论数
        }
    ]
}
```
#### url: host:5000/card/(卡片详情)
##### methods:"GET"
Response:
```
{
    id: Text,
    author: {
        name: Text,
        id: Text,
        avatar: Text,
        followed: Bool
    },
    liked: Bool,
    post: {
        time: YYYY年(M)M月(M)M日 hh:mm，
        content: Text,
        status: Text, //记录宠物状态
        tags: Array,
        likes: Int,
        images: Array
    },
    comments: [
        {
            id: Text,
            author: {
                name: Text,
                id: Text,
                avatar: Text
            },
            to_author: Bool, //标识被回复人是否是作者
            reply_to: Text, //被回复人昵称
            time: YYYY-M-D, //如果年份与当前年份相等，只显示M-D
            content: Text
        }
    ]
}
```
#### url: host:5000/get_hot
##### methods:"GET"
Response:
```
{
    status: 1/0, //是否获取成功的标识符
    infinited: Bool, //如果取完所有卡片，返回true，否则返回false
    cards: [
        {
            id: Text,
            author: {
                name: Text,
                id: Text,
                avatar: Text,
                followed: Bool
            },
            liked: Bool,
            post: {
                time: YYYY年(M)M月(M)M日 hh:mm，
                content: Text,
                status: Text, //记录宠物状态
                tags: Array,
                likes: Int,
                images: Array
            },
            comments: Int //评论数
        }
    ]
}
```
#### url: host:5000/get_cards
##### methods:"GET"
Response:
```
{
}
```
#### url: host:5000/user/focus/
##### methods:"GET"
Request:
```
{
    "id":Text,
    "action":1/0
}
```

Response:
```
{
    "status":1/0,
    "message":"关注成功"/"取消关注成功"
}
```    
#### url: host:5000/user/get_followers
##### methods:"GET"
Response:
```
{
    status: 1/0, //用于判断用户是否登录
    message: Text,
    followers: [
        {
            name: Text, //用户昵称
            id: Text,
            avatar: Text,
            motto: Text,
            followed: Bool
        }
    ]
}
```
#### url: host:5000/user/get_followings
##### methods:"GET"
Response:
```
{
 status: 1/0, //用于判断用户是否登录
    message: Text,
    followers: [
        {
            name: Text, //用户昵称
            id: Text,
            avatar: Text,
            motto: Text,
            followed: Bool
        }
    ]
}
```
#### url: host:5000/user/profile_summary
##### methods:"GET"
Request:
```
{
    
}
```

Response:
```
{
    status: 1/0, //用于标识用户是否登录
    message: Text,
    user: {
        name: Text,
        avatar: Text,
        followers: Int,
        following: Int,
        motto: Text
    }
}
```
#### url: host:5000/user/profile
##### methods:"GET"
Request:
```
{
    status: 1/0, //用于标识用户是否登录
    message: Text,
    user: {
        name: Text,
        avatar: Text,
        motto: Text,
        gender: Text[male/female],
        birth_day: YYYY-MM-DD,
        location: Text
    }
}
```
#### url: host:5000/user/profile_other
##### methods:"GET"
Response:
```
{

    status: 1/0, //用于标识用户是否登录
    message: Text,
    user: {
        name: Text,
        avatar: Text,
        motto: Text,
        gender: Text[male/female],
        birth_day: YYYY-MM-DD,
        location: Text
    }
}
```
#### url: host:5000/user/pet/update
##### methods:"POST"
Request:
```
{
    status: 1/0, //用于判断该宠物是否属于当前用户
    message: Text,
    id: Text,
    name: Text,
    motto: Text,
    avatar: Text,
    gender: Text[male/female],
    birth_day: YYYY-MM-DD,
    meet_day: YYYY-MM-DD,
    variety: Text
}
```
Response:
```
{
    "status":1/0,
    "message":"success"/"failed"
}
```
#### url: host:5000/user/pet/create_pet
##### methods:"POST"
Request:
```
{
    name: Text,
    motto: Text,
    avatar: Text,
    gender: Text[male/female],
    birth_day: YYYY-MM-DD,
    meet_day: YYYY-MM-DD,
    variety: Text
}
```

Response:
```
{
    status: 1/0,
    message: Text,
    id: Text
}
```
#### url: host:5000/user/pet/detail
##### methods:"GET"
Request:
```
{
    "id":Text
}
```

Response:
```
{
    status: 1/0, //用于判断该宠物是否属于当前用户
    message: Text,
    name: Text,
    motto: Text,
    avatar: Text,
    gender: Text[male/female],
    birth_day: YYYY-MM-DD,
    meet_day: YYYY-MM-DD,
    variety: Text
}
```
