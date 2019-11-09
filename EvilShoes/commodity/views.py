import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user.views import check_login_status
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
def commodity_details(request, commodityid):
    # 获取指定id的商品详情
    if request.method == 'GET':
        commodities = CommodityInfo.objects.filter(id=commodityid)
        # data = []
        # for coms in commodities:
        #     ccc = {}
        #     ccc['id'] = coms.id
        #     ccc['name'] = coms.name
        #     ccc['description'] = coms.description
        #     ccc['shelves'] = coms.shelves
        #     ccc['price'] = str(coms.price)
        #     ccc['images'] = coms.images
        #     data.append(ccc)
        if not commodities:
            result = {'code': 20104, 'data': 'commodity not exist'}
            return JsonResponse(result)
        commodity = commodities[0]
        data = {
            'id': commodity.id,
            'name': commodity.name,
            'description': commodity.description,
            'shelves': commodity.shelves,
            'price': str(commodity.price),
            'image': str(commodity.images),
        }
        # if not data:
        #     result = {'code': 20103, 'data': 'Please give me data'}
        #     return JsonResponse(result)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)


# 搜索商品
def search(request):
    if request.method != 'POST':
        result = {'code': 20105, 'error': 'Please use post!'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code': 20106, 'error': 'Please give data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    key = json_obj.get('key')
    if not key:
        result = {'code': 20107, 'error': 'Please give me the key!'}
        return JsonResponse(result)
    goods = CommodityInfo.objects.filter(name__icontains=key)[0]
    if not goods:
        result = {'code': 20108, 'error': "Sorry,we don't have this goods!"}
        return JsonResponse(result)
    result = {'code': 200, 'data': {'id': goods.id, 'name': goods.name, 'shelves': goods.shelves,
                                    'price': str(goods.price), 'description': goods.description,
                                    'image': str(goods.images)}}
    return JsonResponse(result)


# 去结算/立即购买
@check_login_status
def buy_now(request):
    if request.method != 'GET':
        result = {'code': 40102, 'error': 'Please use get!'}
        return JsonResponse(result)
    json_str = request.body
    if not json_str:
        result = {'code': 40103, 'error': 'Please give me data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    commodities_id = json_obj['commodities_id']
    commodities_info = []
    for commodity_id in commodities_id:
        commodity_info = {}
        commodity = CommodityInfo.objects.filter(id=commodity_id)
        commodity_info['id'] = commodity.id
        commodity_info['name'] = commodity.name
        commodity_info['shelves'] = commodity.shelves
        commodity_info['price'] = str(commodity.price)
        commodity_info['description'] = commodity.description
        commodity_info['images'] = str(commodity.images)
        commodities_info.append(commodity_info)

    result = {'code': 200, 'commodities_info': commodities_info}
    return JsonResponse(result)
