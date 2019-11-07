import json
from django.http import JsonResponse
from django.shortcuts import render

from user.views import check_login_status
from .models import *


# Create your views here.

@check_login_status
def cart_view(request):
    user = request.user
    # 1.显示购物车信息
    if request.method == 'GET':
        all_cart_info = CartInfo.objects.filter(user=user.username)
        # data = [{'id': 1, 'name': 'xxx', 'count': 1},{}]
        data = []
        for cart_info in all_cart_info:
            c = {}
            c['id'] = cart_info.id
            c['name'] = cart_info.name
            c['unit_price'] = cart_info.unit_price
            c['count'] = cart_info.count
            c['total_price'] = cart_info.unit_price * cart_info.count
            data.append(c)

        result = {'code': 200, 'data': data}
        return JsonResponse(result)

    # 2.修改购物车信息-->数量变化
    elif request.method == 'PUT':
        json_str = request.body
        if not json_str:
            result = {'code': 30100, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        count = json_obj['count']
        name = json_obj['name']
        if not count:
            result = {'code': 30102, 'error': 'Please give me count!'}
            return JsonResponse(result)
        if not name:
            result = {'code': 30103, 'error': 'Please give me name of goods!'}
            return JsonResponse(result)

        cart_info = CartInfo.objects.filter(user=user.username, name=name)[0]
        cart_info.count = count
        cart_info.save()

    # 3.删除购物车信息
    elif request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {'code': 30104, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        name = json_obj.get('name')
        if not name:
            result = {'code': 30105, 'error': 'Please give name of goods!'}
            return JsonResponse(result)
        cart_info = CartInfo.objects.filter(user=user.username, name=name)[0]
        cart_info.delete()

    # 4.加入购物车
    elif request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 30106, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        name = json_obj['name']
        price = json_obj['price']
        count = json_obj['count']
        if not name:
            result = {'code': 30107, 'error': 'Please give me name of goods!'}
            return JsonResponse(result)
        if not price:
            result = {'code': 30108, 'error': 'Please give me price!'}
            return JsonResponse(result)
        if not count:
            result = {'code': 30109, 'error': 'Please give me count!'}
            return JsonResponse(result)
        try:
            # 购物车中已经有这件商品则数量增加
            cart_info = CartInfo.objects.get(user=user.username, name=name)
            cart_info.count += count
            cart_info.save()
        except Exception as e:
            print(e)
            # 购物车中没有这件商品则增加商品
            CartInfo.objects.create(user=user.username, name=name, unit_price=price, count=count)

        result = {'code': 200}
        return JsonResponse(result)
