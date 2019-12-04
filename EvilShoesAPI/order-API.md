# order模块接口文档
## 一.通信协议
json
## 二.数据库结构
### 订单信息表
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
id|int | 订单id|
add_id | int | 收货地址id  |
total_money|decimal|商品总价 |
total_amount | int | 商品总数
create_time|datetime|订单创建时间
status|int|订单状态|
user | 外键|关联用户表

### 订单货物表
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
goods_id|char|商品id|
price|decimal|商品单价
count|int|商品数量
order|外键|关联订单信息表

## 三.接口说明
###1.生成订单接口
url:http:127.0.0.1:8000/order
####1.1请求方式
POST
####1.2请求格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
addr_id |int | 收货地址id | 
total_amount |int| 商品总数 | 
total_money| decimal | 订单总价
commodities| 【】| 商品信息 | 下面是commodities内的数据
id | char | 商品id | 
count| int| 商品数量
price|decimal|商品单价

请求例子：
{‘addr_id’：'1'，‘total_amount’1‘，’total_money:123,'commodities':[{'name':'xxx','count'1,'price':123},{}..]}

####1.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常由40100开始

响应例子：{'code':200}

## 2.查看订单接口
url:http://127.0.0.1:8000/order
###2.1请求方式
GET
###2.2请求格式
全量

###2.3响应格式
|字段名 | 类型 |  作用 | 备注|
|-|-|-|-|
code|int|状态|正常为200，异常由40200开始
all_order|[]|全部订单|下面是单个订单内的数据
id|int|订单id|
addr_id|int|收货地址id
total_amount|int|订单商品总数
total_money|decimal|订单总价
create_time|data|订单创建时间
status|int|订单状态
commodities|[]|订单商品信息|下面是订单商品信息内的数据
name|char|商品名称
price|decimal|商品价格
count|int|商品数量

响应例子：result = {'code': 200, 'all_order': [
            {'id': 1, 'addr_id': 1, 'total_amount': 1, 'total_money': 1, 'create_time': 111, 'status': 0,
             'commodities': [{'name': 'xxx', 'price': 1, 'count': 1}, {}, {}]}, {}, {}]
                  }
