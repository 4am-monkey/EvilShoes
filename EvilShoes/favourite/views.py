from django.shortcuts import render
import json
from django.http import JsonResponse

from commodity.models import CommodityInfo
from .models import *
from user.views import check_login_status


# Create your views here.


# 显示收藏夹所有商品
@check_login_status
def favourite_view(request):
    user = request.user
    if request.method == 'GET':
        all_favourite = Favourite.objects.filter(user=user.username)
        data = []
        for fav in all_favourite:
            f = {}
            f['id'] = fav.id
            f['name'] = fav.name
            f['description'] = fav.description
            f['images'] = str(fav.images)
            data.append(f)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)

    # 增加收藏商品
    elif request.method == 'POST':
        # 拿数据
        json_str = request.body
        if not json_str:
            result = {'code': 50201, 'data': 'Please give me data'}
            return JsonResponse(result)
        # 转python
        json_obj = json.loads(json_str.decode())
        id = json_obj['id']
        if not id:
            result = {'code': 50202, 'data': 'Please give me id'}
            return JsonResponse(result)
        try:
            good = CommodityInfo.objects.get(id=id)
        except Exception as e:
            result = {'code': 50203, 'data': 'commodity not found'}
            return JsonResponse(result)
        # 判断
        try:
            Favourite.objects.create(id=id, name=good.name, description=good.description,
                                     images=good.images, user=user)
        except Exception as e:
            print('create error!')
            print(e)
            result = {'code': 50206, 'data': 'Some way error!'}
            return JsonResponse(result)
        result = {'code': 200}
        return JsonResponse(result)

    # 删除收藏商品
    elif request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {'code': 50301, 'data': 'Please give me data'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        id = json_obj.get('id')
        if not id:
            result = {'code': 50302, 'data': 'Please give me id of goods'}
            return JsonResponse(result)
        try:
            fav_info = Favourite.objects.filter(user=user.username, id=id)[0]
            fav_info.delete()
        except Exception as e:
            print('delete error')
            print(e)
            result = {'code': 50303, 'data': 'Some way error!'}
            return JsonResponse(result)
        result = {'code': 200}
        return JsonResponse(result)
