# 购物车 API 文档

[TOC]

## 数据表结构设计

- 购物车表

  <table>
      <tr>
      	<th>字段</th>
      	<th>类型</th>
      	<th>verbose_name</th>
          <th>备注</th>
      </tr>
      <tr>
      	<td>name</td>
          <td>char</td>
          <td>商品名称</td>
          <td></td>
      </tr>
      <tr>
      	<td>count</td>
          <td>int</td>
          <td>商品数量</td>
          <td>数量</td>
      </tr>
      <tr>
      	<td>unit_price</td>
          <td>dicimal(6,2)</td>
          <td>价格</td>
          <td>小计价格</td>
      </tr>
      <tr>
      	<td>user</td>
          <td>ForeignKey</td>
          <td>所属用户</td>
          <td>购物车所属用户ID</td>
      </tr>
  </table>
  
  

## 功能

### 1、显示购物车

#### 			1.1描述

​			获取请求后返回当前用户的购物车数据

​			请求头中携带Authorization，其中存储着用户ID，由此验证用户身份

#### 	1.2 URL  
<u>			http://127.0.0.1:8000/cart</u>

  #### 	1.3 请求方式

  		GET

  #### 	1.4 请求格式

​		**请求示例**		

​		<u>http://127.0.0.1:8000/cart</u>

  #### 	1.5 响应格式

​		JSON参数表

<table>
    <tr>
    	<th>字段</td>
        <th>类型</td>
        <th>含义</td>
        <th>备注</td>
    </tr>
    <tr>
    	<td>code</td>
        <td>int</td>
        <td>状态</td>
        <td>默认正常为200，错误代码详情见1.6</td>
    </tr>
	<tr>
    	<td>data</td>
        <td>{}</td>
        <td>返回的数据</td>
        <td>{'goods':[{'good1':[name,count,unit_price,total_price]},
            	'good2':[name,count,unit_price,total_price]]}</td>
    </tr>
</table>

​	**响应示例**：{'code': 200,'data': {'goods':[{'good1':[name,count,unit_price,total_price]},
            	'good2':[name,count,unit_price,total_price]]}}

  #### 	1.6 异常状态码

​		格式： 30xxx

<table>
    <tr>
    	<th>状态码</th>
        <th>含义</th>
    </tr>
    <tr>
    	<td>30101</td>
        <td>请求头中没有携带Authorization</td>
    </tr>
</table>

### 2、商品加入购物车

#### 			2.1描述

​		情况：用户在登录状态下将商品加入购物车

​				用户**登录**状态将商品加入购物车后将购物车对象的数据缓存到**Redis**中，限时**24小时**，到期后未结算则持久化

#### 		2.2 URL

​		<u>http://127.0.0.1:8000/cart/add</u>

#### 	2.3 请求方式

​		POST

#### 	2.4 请求格式

​		JSON参数如下

<table>
    <tr>
    	<th>字段</th>
        <th>类型</th>
        <th>含义</th>
        <th>备注</th>
    </tr>
    <tr>
    	<td>name</td>
        <td>char</td>
        <td>商品名字</td>
        <td></td>
    </tr>
    <tr>
    	<td>price</td>
        <td>decimal</td>
        <td>商品价格</td>
        <td></td>
    </tr>
        <tr>
    	<td>count</td>
        <td>int</td>
        <td>商品数量</td>
        <td></td>
    </tr>
</table>

**请求实例**: {'name': 'AJ', 'price': 123.04, 'count': 99}

#### 	2.5 响应格式

​		**响应实例**: {'code': 200}

#### 2.6 异常状态码

  相应实例: {'code': 30106, 'error': 'Please give me data'}

<table>
    <tr>
    	<th>状态码</th>
        <th>含义</th>
    </tr>
    <tr>
    	<td>30107</td>
        <td>找不到商品名字</td>
    </tr>
    <tr>
    	<td>30108</td>
        <td>找不到价格</td>
    </tr>
        <tr>
    	<td>30109</td>
        <td>找不到数量</td>
    </tr>
</table>

### 3、修改数量

#### 	3.1 描述

​		提供购物车对应商品数量的修改接口，可增加或减少，增加后将实时数据同步至Redis，限时24小时，未结算则持久化		

#### 	3.2 URL

​		<u>http://127.0.0.1:8000/cart/change</u>

#### 	3.3 请求方式

​		PUT

#### 	3.4 请求格式

<table>
    <tr>
    	<th>字段</th>
        <th>类型</th>
        <th>含义</th>
        <th>备注</th>
    </tr>
    <tr>
    	<td>name</td>
        <td>char</td>
        <td>商品名字</td>
        <td></td>
    </tr>
    <tr>
    	<td>count</td>
        <td>int</td>
        <td>当前商品的数量</td>
        <td></td>
    </tr>
</table>
**请求实例**：{'name': 'AJ','count': 2}

#### 	3.5 响应格式

<table>
    <tr>
    	<th>字段</td>
        <th>类型</td>
        <th>含义</td>
        <th>备注</td>
    </tr>
    <tr>
    	<td>code</td>
        <td>int</td>
        <td>状态</td>
        <td>默认正常为200，错误代码详情见1.6</td>
    </tr>
	<tr>
    	<td>data</td>
        <td>{}</td>
        <td>返回的数据</td>
        <td>{'name': 'AJ','count': 2}</td>
    </tr>
</table>

#### 	3.6 异常状态码

<table>
    <tr>
    	<th>状态码</th>
        <th>含义</th>
    </tr>
    <tr>
    	<td>30100</td>
        <td>找不到data</td>
    </tr>
        <tr>
    	<td>30102</td>
        <td>找不到数量</td>
    </tr>
        <tr>
    	<td>30103</td>
        <td>找不到商品数量</td>
    </tr>
</table>

### 4、删除商品

#### 	4.1 描述

​		满足用户将买不起的商品从购物车移除的需求

#### 	4.2 URL

​		<u>http://127.0.0.1:8000/cart/delete/[cart_id]</u>

#### 	4.3 请求方式

​		DELETE

#### 	4.4 请求格式

​		请求实例: <u>http://127.0.0.1:8000/cart/delete/123132</u>

#### 	4.5 响应格式

​		{'code': 200}

#### 	4.6 异常状态码

<table>
    <tr>
    	<th>状态码</th>
        <th>含义</th>
    </tr>
    <tr>
    	<td>30104</td>
        <td>找不到data</td>
    </tr>
        <tr>
    	<td>30105</td>
        <td>找不到商品名字</td>
    </tr>
</table>






#结算暂无





### 5、结算

#### 	5.1 描述

​		计算选定商品总价格生成订单并清空选定的商品			

#### 	5.2 URL

​		<u>http://127.0.0.1:8000/cart/order</u>

#### 	5.3 请求方式

​		POST

#### 	5.4 请求格式

<table>
    <tr>
    	<th>字段</th>
        <th>类型</th>
        <th>含义</th>
        <th>备注</th>
    </tr>
    <tr>
    	<td>username</td>
        <td>char</td>
        <td>用户名</td>
        <td>提供用户名用户绑定购物车</td>
    </tr>
    <tr>
    	<td>total_price</td>
        <td>decimal(6,2)</td>
        <td>总价格</td>
        <td></td>
    </tr>
    <tr>
    	<td>id</td>
        <td>int</td>
        <td>购物车对应商品id</td>
        <td></td>
    </tr>
</table>

#### 	5.5 响应格式

​		{'code': 200}

​		**跳转到订单模块**

#### 	5.6 异常状态码

<table>
    <tr>
    	<th>状态码</th>
        <th>含义</th>
    </tr>
    <tr>
    	<td>30501</td>
        <td>重新再来吧</td>
    </tr>
</table>