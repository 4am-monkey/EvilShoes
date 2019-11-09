import json
from django.http import JsonResponse
from django.shortcuts import render
import redis
from commodity.models import CommodityInfo
from user.views import check_login_status
from .models import *


# Create your views here.

@check_login_status
def cart_view(request):
    user = request.user
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    cart_key = 'cart_%s' % user.username
    # 1.显示购物车信息--sql版本
    # if request.method == 'GET':
    #     all_cart_info = CartInfo.objects.filter(user=user.username)
    #     # data = [{'id': 1, 'name': 'xxx', 'count': 1},{}]
    #     data = []
    #     for cart_info in all_cart_info:
    #         c = {}
    #         c['id'] = cart_info.id
    #         c['name'] = cart_info.name
    #         c['unit_price'] = cart_info.unit_price
    #         c['count'] = cart_info.count
    #         c['total_price'] = cart_info.unit_price * cart_info.count
    #         data.append(c)
    #
    #     result = {'code': 200, 'data': data}
    #     return JsonResponse(result)

    # 1.显示购物车信息--redis版本
    if request.method == 'GET':
        # 获取用户购物车信息
        # {'商品ID':商品数量}
        cart_dict = conn.hgetall(cart_key)
        commodities = []
        # 遍历字典获取商品信息
        for commodity_id, count in cart_dict.items():
            # 根据商品ID获取商品信息
            commodity = CommodityInfo.objects.filter(id=commodity_id)[0]
            # 商品小计
            amount = commodity.price * int(count)
            # 给commodity动态增加属性
            commodity.amount = amount
            commodity.count = count
            commodities.append(commodity)
        result = {'code': 200, 'commodities': commodities}
        return JsonResponse(result)


    # 2.修改购物车信息-->数量变化--sql版本
    # elif request.method == 'PUT':
    #     json_str = request.body
    #     if not json_str:
    #         result = {'code': 30100, 'error': 'Please give me data!'}
    #         return JsonResponse(result)
    #     json_obj = json.loads(json_str.decode())
    #     count = json_obj['count']
    #     name = json_obj['name']
    #     if not count:
    #         result = {'code': 30102, 'error': 'Please give me count!'}
    #         return JsonResponse(result)
    #     if not name:
    #         result = {'code': 30103, 'error': 'Please give me name of goods!'}
    #         return JsonResponse(result)
    #
    #     cart_info = CartInfo.objects.filter(user=user.username, name=name)[0]
    #     cart_info.count = count
    #     cart_info.save()

    # 2.修改购物车信息-->数量变化--redis版本
    elif request.method == 'PUT':
        # 拿数据
        json_str = request.body
        if not json_str:
            result = {'code': 30100, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        commodity_id = json_obj['commodity_id']
        count = json_obj['count']
        # 校验数据
        if not commodity_id:
            result = {'code': 30101, 'error': 'Please give me commodity_id!'}
            return JsonResponse(result)
        if not count:
            result = {'code': 30102, 'error': 'Please give me count!'}
            return JsonResponse(result)
        try:
            count = int(count)
        except Exception as e:
            print(e)
            result = {'code': 30103, 'error': '数据出错!'}
            return JsonResponse(result)
        try:
            commodity = CommodityInfo.objects.get(id=commodity_id)
        except CommodityInfo.DoesNotExist:
            result = {'code': 30104, 'error': '商品不存在!'}
            return JsonResponse(result)
        # 更新购物车记录
        conn.hset(cart_key, commodity_id, count)
        result = {'code': 200, 'message': '更新成功！'}
        return JsonResponse(result)

    # 3.删除购物车信息--sql版本
    # elif request.method == 'DELETE':
    #     json_str = request.body
    #     if not json_str:
    #         result = {'code': 30104, 'error': 'Please give me data!'}
    #         return JsonResponse(result)
    #     json_obj = json.loads(json_str.decode())
    #     name = json_obj.get('name')
    #     if not name:
    #         result = {'code': 30105, 'error': 'Please give name of goods!'}
    #         return JsonResponse(result)
    #     cart_info = CartInfo.objects.filter(user=user.username, name=name)[0]
    #     cart_info.delete()

    # 3.删除购物车信息--redis版本
    elif request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {'code': 30105, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        commodity_id = json_obj['commodity_id']
        if not commodity_id:
            result = {'code': 30106, 'error': 'Please give me commodity_id!'}
            return JsonResponse(result)
        try:
            commodity = CommodityInfo.objects.get(id=commodity_id)
        except CommodityInfo.DoesNotExist:
            result = {'code': 30107, 'error': '商品不存在！'}
            return JsonResponse(result)
        # 删除
        conn.hdel(cart_key, commodity_id)

        result = {'code': 200, 'message': '删除成功！'}
        return JsonResponse(result)
    # 4.加入购物车--sql版本
    # elif request.method == 'POST':
    #     json_str = request.body
    #     if not json_str:
    #         result = {'code': 30106, 'error': 'Please give me data!'}
    #         return JsonResponse(result)
    #     json_obj = json.loads(json_str.decode())
    #     name = json_obj['name']
    #     price = json_obj['price']
    #     count = json_obj['count']
    #     if not name:
    #         result = {'code': 30107, 'error': 'Please give me name of goods!'}
    #         return JsonResponse(result)
    #     if not price:
    #         result = {'code': 30108, 'error': 'Please give me price!'}
    #         return JsonResponse(result)
    #     if not count:
    #         result = {'code': 30109, 'error': 'Please give me count!'}
    #         return JsonResponse(result)
    #     try:
    #         # 购物车中已经有这件商品则数量增加
    #         cart_info = CartInfo.objects.get(user=user.username, name=name)
    #         cart_info.count += count
    #         cart_info.save()
    #     except Exception as e:
    #         print(e)
    #         # 购物车中没有这件商品则增加商品
    #         CartInfo.objects.create(user=user.username, name=name, unit_price=price, count=count)
    #
    #     result = {'code': 200}
    #     return JsonResponse(result)

    # 4.加入购物车--redis版本
    elif request.method == 'POST':
        # 拿数据
        json_str = request.body
        if not json_str:
            result = {'code': 30106, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        commodity_id = json_obj['commodity_id']
        count = json_obj['count']
        # 校验数据
        if not commodity_id:
            result = {'code': 30107, 'error': 'Please give me commodity_id!'}
            return JsonResponse(result)
        if not count:
            result = {'code': 30108, 'error': 'Please give me count!'}
            return JsonResponse(result)
        try:
            count = int(count)
        except Exception as e:
            print(e)
            result = {'code': 30109, 'error': '数据出错!'}
            return JsonResponse(result)
        try:
            commodity = CommodityInfo.objects.get(id=commodity_id)
        except CommodityInfo.DoesNotExist:
            result = {'code': 30110, 'error': '商品不存在!'}
            return JsonResponse(result)
        # 添加购物车记录
        # 先尝试从redis中
        cart_count = conn.hget(cart_key, commodity_id)
        if cart_count:
            # 累加购物车中商品的数目
            count += int(cart_count)
        # 设置hash中commodity_id的值
        conn.hset(cart_key, commodity_id, count)
        result = {'code': 200, 'message': '添加成功！'}
        return JsonResponse(result)
