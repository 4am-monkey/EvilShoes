import json
from django.http import JsonResponse
from django.shortcuts import render

from user.views import check_login_status
from .models import *


# Create your views here.

@check_login_status
def show_cart(request):
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
