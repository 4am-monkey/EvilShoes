import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


from order.models import OrderInfo, OrderGoods
from user.views import check_login_status


@check_login_status
def order_view(request):
    user = request.user
    # 生成订单(立即购买/去结算)
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 40100, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        addr_id = json_obj['addr_id']
        total_amount = json_obj['total_amount']
        total_money = json_obj['total_money']
        commodities = json_obj['commodities']
        try:
            order = OrderInfo.objects.create(user=user.username, addr_id=addr_id, total_amount=total_amount,
                                             total_money=total_money)
        except Exception as e:
            print(e)
            print('create error!')
            result = {'code': 40101, 'error': 'filed to create order!'}
            return JsonResponse(result)

        for commodity in commodities:
            name = commodity['name']
            count = commodity['count']
            price = commodity['price']
            OrderGoods.objects.create(order=order.id, name=name, count=count, price=price)

    # 查看订单
    elif request.method == 'GET':
        # result = {'code': 200, 'all_order': [
        #     {'id': 1, 'addr_id': 1, 'total_amount': 1, 'total_money': 1, 'create_time': 111, 'status': 0,
        #      'commodities': [{'name': 'xxx', 'price': 1, 'count': 1}, {}, {}]}, {}, {}]
        #           }
        orders = OrderInfo.objects.filter(user=user.username)
        all_order = []
        for order in orders:
            o = {}
            o['id'] = order.id
            o['addr_id'] = order.addr_id
            o['total_amount'] = order.total_amount
            o['total_money'] = order.total_money
            o['create_time'] = order.create_time
            o['status'] = order.status
            all_goods = OrderGoods.objects.filter(order=id)
            o['commodities'] = []
            for goods in all_goods:
                g = {}
                g['name'] = goods.name
                g['price'] = goods.price
                g['count'] = goods.count
                o['commodities'].append(g)
            all_order.append(o)

        result = {'code': 200, 'all_order': all_order}
        return JsonResponse(result)

    # 删除订单
    elif request.method == 'DELETE':
        # 拿orderID
        pass
