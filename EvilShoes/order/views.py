import json
import redis
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
import os

# Create your views here.
from commodity.models import CommodityInfo
from order.models import OrderInfo, OrderGoods
from user.models import ReceiverInfo
from user.views import check_login_status
from django.core import serializers
from alipay import AliPay


# @transaction
@check_login_status
def order_view(request):
    user = request.user
    conn = redis.Redis(host='127.0.0.1', port=6379, db=0, password='123456')
    # conn = redis.Redis(host='127.0.0.1', port=6379, db=0)
    cart_key = 'cart_%s' % user.username
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
            order_id = order.id
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
                com = CommodityInfo.objects.get(id=id)
            except CommodityInfo.DoesNotExist:
                result = {'code': 40102, 'error': '商品不存在!'}
                return JsonResponse(result)
            commodity_name = com.name
            OrderGoods.objects.create(order=order, name=commodity_name, count=count, price=price)
            # 更新库存
            com.storage -= int(count)
            com.save()
            # 清除用户购物车中对应的记录
            conn.hdel(cart_key, id)
        result = {'code': 200, 'data': {'order_id': order_id}}
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


# 订单支付
@check_login_status
def order_pay_view(request):
    user = request.user
    if request.method != 'POST':
        result = {'code': 40103, 'error': 'Please use post!'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code': 40104, 'error': 'Please give me data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    order_id = json_obj.get('order_id')
    if not order_id:
        result = {'code': 40105, 'error': 'Please give me order_id!'}
        return JsonResponse(result)
    try:
        order = OrderInfo.objects.get(id=order_id, user=user, status=0)
    except OrderInfo.DoesNotExist:
        result = {'code': 40106, 'error': '订单不存在！'}
        return JsonResponse(result)
    # 初始化
    alipay = AliPay(
        appid="2016101700705616",
        app_notify_url=None,  # 默认回调url
        # app_private_key_string=os.path.join(settings.BASE_DIR, '/order/app_private_key.pem'),
        app_private_key_string=open("/home/python/zero/EvilShoes/EvilShoes/order/app_private_key.pem").read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        # alipay_public_key_string=os.path.join(settings.BASE_DIR, '/order/app_public_key.pem'),
        alipay_public_key_string=open("/home/python/zero/EvilShoes/EvilShoes/order/app_public_key.pem").read(),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    total_price = order.total_price
    # 调用支付宝接口
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(total_price),
        subject='潮鞋order_%d' % order_id,
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    pay_url = 'https://openapi.alipay.com/gateway.do?' + order_string
    result = {'code': 200, 'pay_url': pay_url}
    return JsonResponse(result)


# 查看订单支付的结果
# ajax post
# 前端传递参数：订单id(order_id)
# /order/check
@check_login_status
def check_pay_view(request):
    user = request.user
    if request.method != 'POST':
        result = {'code': 40107, 'error': 'Please use post!'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code': 40108, 'error': 'Please give me data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    # 接收参数
    order_id = json_obj.get("order_id")
    # 校验参数
    if not order_id:
        result = {'code': 40109, 'error': 'Please give me order_id!'}
        return JsonResponse(result)
    try:
        order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=0)
    except OrderInfo.DoesNotExist:
        return JsonResponse({"res": 2, "errmsg": "订单错误"})

    # 初始化
    alipay = AliPay(
        appid="2016101700705616",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=os.path.join(settings.BASE_DIR, 'order/app_private_key.pem'),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=os.path.join(settings.BASE_DIR, 'order/app_public_key.pem'),
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    while True:
        response = alipay.api_alipay_trade_query(order_id)
        code = response.get("code")
        # 如果返回码为10000和交易状态为交易支付成功
        if code == "10000" and response.get("trade_status") == "TRADE_SUCCESS":
            # 支付成功
            # 获取支付宝交易号
            trade_no = response.get("trade_no")
            # 更新订单状态
            order.trade_no = trade_no
            order.order_status = 4  # 待评价
            order.save()
            return JsonResponse({"res": 3, "message": "支付成功"})
        # 返回码为40004 或 交易状态为等待买家付款
        elif code == "40004" or (response.get("trade_status") == "WAIT_BUYER_PAY"):
            # 等待买家付款
            # 业务处理失败，可能一会就会成功
            import time
            time.sleep(5)
            continue
        else:
            # 支付出错
            return JsonResponse({"res": 4, "errmsg": "支付失败"})
