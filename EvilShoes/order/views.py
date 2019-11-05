import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


from order.models import OrderInfo


# 生成订单
def create_order(request):
    if request.method != 'POST':
        result = {'code': 40100, 'error': 'Please use post!'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code': 40101, 'error': 'Please give me data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    name = json_obj['name']
    count = json_obj['count']
    price = json_obj['price']
    if not name:
        result = {'code': 40102, 'error': 'Please give me name!'}
        return JsonResponse(result)
    if not count:
        result = {'code': 40103, 'error': 'Please give me count!'}
        return JsonResponse(result)
    if not price:
        result = {'code': 40104, 'error': 'Please give me price!'}
        return JsonResponse(result)

    user = request.user
    try:
        OrderInfo.objects.create(user=user.username, name=name, count=count, unit_price=price)
    except Exception as e:
        price(e)
