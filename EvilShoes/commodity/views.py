from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from commodity.models import *


def GoodsInfo(request):
    if request.method == 'GET':
        try:
            goods = Commodity.objects.all()
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
            return JsonResponse({'code': 403, 'error': 'The force majeure cause error'})


def GoodsType(request):
    if request.method == 'GET':
        try:
            gts = Classify.objects.all()
            c = []
            for gt in gts:
                d = {}
                d['name'] = gt.name
                d['description'] = gt.description
                c.append(d)
            return JsonResponse({'code': 200, 'data': c})
        except Exception as e:
            return JsonResponse({'code': 403, 'error': 'The force majeure cause error'})
