import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import CartInfo
from commodity.models import *

# 商品信息
from user.views import check_login_status


def GoodsInfo(request):
    if request.method == 'GET':
        try:
            goods = CommodityInfo.objects.all()
            a = []
            for good in goods:
                b = {}
                b['id'] = good.id
                b['name'] = good.name
                b['shelves'] = good.shelves
                b['price'] = str(good.price)
                b['description'] = good.description
                b['images'] = good.images
                a.append(b)
            return JsonResponse({'code': 200, 'data': a})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 20100, 'error': 'The force majeure cause error'})


# 商品类别
def GoodsType(request):
    if request.method == 'GET':
        try:
            gts = CommodityClassify.objects.all()
            c = []
            for gt in gts:
                d = {}
                d['name'] = gt.name
                d['description'] = gt.description
                c.append(d)
            return JsonResponse({'code': 200, 'data': c})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 20102, 'error': 'The force majeure cause error'})
