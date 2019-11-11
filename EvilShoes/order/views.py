import json
import redis
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from commodity.models import CommodityInfo
from order.models import OrderInfo, OrderGoods
from user.models import ReceiverInfo
from user.views import check_login_status

from django.core import serializers


# @transaction
@check_login_status
def order_view(request):
    user = request.user
    # conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # cart_key = 'cart_%s' % user.username
    # 生成订单
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 40100, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        addr_id = json_obj['addr_id']
        commodities = json_obj['commodities']
        total_price = json_obj['total_money']
        total_count = json_obj['total_amount']
        try:
            order = OrderInfo.objects.create(user=user, addr_id=addr_id, total_count=total_count,
                                             total_price=total_price)
        except Exception as e:
            print(e)
            print('create error!')
            result = {'code': 40101, 'error': 'filed to create order!'}
            return JsonResponse(result)

        for commodity in commodities:
            id = commodity['id']
            count = commodity['count']
            price = commodity['price']
            try:
                com = CommodityInfo.objects.select_for_update.get(id=id)
            except CommodityInfo.DoesNotExist:
                result = {'code': 40102, 'error': '商品不存在!'}
                return JsonResponse(result)
            commodity_name = com.name
            OrderGoods.objects.create(order=order, name=commodity_name, count=count, price=price)
            # 更新库存
            com.storage -= int(count)
            com.save()
            # # 清除用户购物车中对应的记录
            # conn.hdel(cart_key, id)
        result = {'code': 200, 'data': 'Create successfully!'}
        return JsonResponse(result)

    # 查看订单
    elif request.method == 'GET':
        # result = {'code': 200, 'all_order': [
        #     {'id': 1, 'addr_id': 1, 'total_amount': 1, 'total_money': 1, 'create_time': 111, 'status': 0,
        #      'commodities': [{'name': 'xxx', 'price': 1, 'count': 1}, {}, {}]}, {}, {}]
        #           }
        orders = OrderInfo.objects.filter(user=user)
        all_order = []
        for order in orders:
            o = {}
            o['id'] = order.id
            # o['addr_id'] = order.addr_id
            o['total_amount'] = order.total_count
            o['total_money'] = order.total_price
            o['create_time'] = order.create_time
            o['status'] = order.status
            address = ReceiverInfo.objects.filter(id=order.addr_id)
            o['addr_info'] = serializers.serialize('json', address)
            all_goods = OrderGoods.objects.filter(order=order)
            o['commodities'] = []
            for goods in all_goods:
                g = {}
                g['name'] = goods.name
                g['price'] = goods.price
                g['count'] = goods.count
                o['commodities'].append(g)
            all_order.append(o)
            # order_commodities = OrderGoods.objects.filter(order=order)
            # order.order_commodities = order_commodities
        result = {'code': 200, 'all_order': all_order}
        return JsonResponse(result)

    # 删除订单
    elif request.method == 'DELETE':
        # 拿orderID
        pass
