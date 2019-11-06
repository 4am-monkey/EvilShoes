import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import CommodityInfo
from .models import CommodityClassify


# 分类接口
def classify_view(request):
    # 获取所有分类
    if request.method == 'GET':
        all_classify_info = CommodityClassify.objects.all()
        data = []
        for classify_info in all_classify_info:
            type = {}
            type['name'] = classify_info.name
            type['description'] = classify_info.description
            data.append(type)
        # if not data:
        #     result = {'code': 20100, 'data': 'table classify is empty'}
        #     return JsonResponse(result)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)


# 所有商品接口
def all_commodity(request):
    # 获取所有的商品
    if request.method == 'GET':
        commodities = CommodityInfo.objects.all()
        data = []
        for com in commodities:
            c = {}
            c['id'] = com.id
            c['name'] = com.name
            c['price'] = str(com.price)
            c['images'] = str(com.images)
            data.append(c)
        # if not data:
        #     result = {'code': 20101, 'data': 'Please give me data'}
        #     return JsonResponse(result)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)


# 分类下的商品接口
def classify_commodity(request, typename):
    # 获取分类下的所有商品
    if request.method == 'GET':
        commodities = CommodityInfo.objects.filter(classify=typename)
        data = []
        for tycom in commodities:
            cc = {}
            cc['id'] = tycom.id
            cc['name'] = tycom.name
            cc['price'] = str(tycom.price)
            cc['images'] = tycom.images
            data.append(cc)
        if not data:
            result = {'code': 20102, 'data': 'Please give me data'}
            return JsonResponse(result)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)


# 商品详情接口
def commodity_details(request):
    # 获取指定id的商品详情
    if request.method == 'GET':
        commodities = CommodityInfo.objects.filter(id=id)
        data = []
        for coms in commodities:
            ccc = {}
            ccc['id'] = coms.id
            ccc['name'] = coms.name
            ccc['description'] = coms.description
            ccc['shelves'] = coms.shelves
            ccc['price'] = str(coms.price)
            ccc['images'] = coms.images
            data.append(ccc)
        if not data:
            result = {'code': 20103, 'data': 'Please give me data'}
            return JsonResponse(result)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)
