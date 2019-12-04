# user模块接口文档
## 一.通信协议
json
## 二.数据库结构
### 用户表
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
username|varchar(32) | 用户名|不可修改 
nickname | varchar(32) | 昵称  | 可修改,默认为username
password|varchar(32)|密码 |散列存储 
email | varchar(255) | 邮箱 
telephone|varchar(11)|手机号码
create_time|datetime|创建时间
updated_time|datetime|更新时间
login_time|datetime|登录时间
is_login|int|登录状态|

### 地址表
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
user|varchar(32)|用户|外键关联用户表
receiver|varchar(32)|收件人
address|varchar(648)|收货地址
receiver_phone|varchar(11)|收件人手机号码
is_default|bool|是否默认收货地址

## 三.接口说明
###1.注册接口
url:http:127.0.0.1:8000/user/register
####1.1请求方式
POST
####1.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
username |char | 用户名 | 必填
password_1 |char | 第一次输入密码 | 必填
password_2 | char | 第二次输入密码 | 必填
telephone | char | 手机号码 | 必填
email | char | 用户邮箱 | 选填

请求例子：
{‘username’：'zero'，‘email’：abc@qq.com‘，’password_1':'asdf','password_2':'asdf','telephone':1231231}

####1.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常由10100开始
username|char|用户名
data|{}|返回具体的数据|{token：xxx}用于保持会话

响应例子：{'code':200,'username':'zero','data':{'token':'fdsafdsa'}

## 2.登录接口
url:http://127.0.0.1:8000/user/login
###2.1请求方式
POST
###2.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
username|char|用户名
password|char|密码

请求例子：{'username':'zero','password':'213asdf'}

###2.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常由10200开始
username|char|用户名
data|{}|具体数据|{‘token’：‘fsadf'}

响应例子：{'code':200,'username':'zero','data':{'token':'fadsf'}

## 3.获取用户信息接口
url：http://127.0.0.1:8000/user/info
### 3.1请求方式
GET
### 3.2请求格式
获取全量数据

### 3.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|请求成功为200，异常码从10300开始
username|char|用户名
data|{}|具体数据

响应例子：{‘telephone':0123456789,'nickname':‘昵称’，’email‘：abc@qq.com}

## 4.修改用户信息接口
url:http:127.0.0.1:8000/user/info
### 4.1请求方式
PUT
### 4.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
nickname|char|昵称
email|char|邮箱
telephone|char|手机号码

请求例子：
{'nickname':'zero','telephone':0123456789,'email':'bac@qq.com','avatar':'sdaf.jpg'}

该请求需客户端在 HTTP header 里添加 token,
格式如下:
Authorization : token

### 4.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常码从10400开始
username|char|用户名

## 5.获取用户收货地址信息接口
url:127.0.0.1:8000/user/address
### 5.1请求方式
GET
### 5.2请求格式
获取全量数据
### 5.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常码从10500开始
data|{}|具体数据|

响应例子：
{’code‘：200，’data‘：[{'id':1,'receiver':'zero','address':'xxx','telephone':0123456789,'is_default':'True'},{},{}]

## 6.t添加用户收货地址信息接口
url:127.0.0.1:8000/user/address
### 6.1请求方式
POST
### 6.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
username|char|用户名
receiver|char|收件人
address|char|收货地址
telephone|char|收件人电话
is_default|bool|是否为默认地址

### 6.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|成功为200，异常码从10600开始
username|char|用户名

## 7.删除用户收货地址信息接口
url:127.0.0.1:8000/user/address
### 7.1请求方式
DELETE
### 7.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
addr_id|int|地址id

该请求需客户端在 HTTP header 里添加 token,
Authorization : token

### 7.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|200|正常为200，异常码从10700开始

## 8.修改默认地址接口
url:127.0.0.1:8000/user/address
### 8.1请求方式
PUT
### 8.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
addr_id|int|地址id

### 8.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|200|正常为200，异常码从10800开始










































