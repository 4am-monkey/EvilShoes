import datetime
import hashlib
import json
import re
from django.http import JsonResponse
import jwt
from user.models import UserInfo, ReceiverInfo


# 注册
def register_view(request):
    if request.method != 'POST':
        result = {'code': 10100, 'error': 'Please use post'}
        return JsonResponse(result)

    json_str = request.body
    if not json_str:
        result = {'code': 10101, 'error': 'Please give data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str.decode())
    username = json_obj.get('username')
    password_1 = json_obj.get('password_1')
    password_2 = json_obj.get('password_2')
    telephone = json_obj.get('telephone')
    email = json_obj.get('email')

    if not username:
        result = {'code': 10102, 'error': 'Please enter username!'}
        return JsonResponse(result)
    if len(username) > 32:
        result = {'code': 10103, 'error': 'Length of username can not exceed 32 bit!'}
        return JsonResponse(result)
    if not password_1 or not password_2:
        result = {'code': 10104, 'error': 'Please enter password!'}
        return JsonResponse(result)
    if len(password_1) > 32 or len(password_2) > 32:
        result = {'code': 10105, 'error': 'Length of password can not exceed 32 bit!'}
        return JsonResponse(result)
    if not telephone:
        result = {'code': 10106, 'error': 'Please enter telephone!'}
        return JsonResponse(result)
    if len(telephone) != 11:
        result = {'code': 10107, 'error': 'length of telephone must be 11!'}
        return JsonResponse(result)
    if not email:
        result = {'code': 10108, 'error': 'Please enter your email!'}
        return JsonResponse(result)
    # 判断邮箱格式
    p = re.compile('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
    res = p.match(email)
    if not res:
        result = {'code': 10109, 'error': 'The format of the mailbox is incorrect!'}
        return JsonResponse(result)
    if res.group() != email:
        result = {'code': 10110, 'error': 'The format of the mailbox is incorrect!'}
        return JsonResponse(result)
    if password_1 != password_2:
        result = {'code': 10111, 'error': 'Password_1 is not match Password_2!'}
        return JsonResponse(result)

    try:
        user = UserInfo.objects.get(username=username)
        # 有数据即用户名已存在
        result = {'code': 10112, 'error': 'Username is already exists!'}
        return JsonResponse(result)
    except Exception as e:
        # 没有数据即用户名可用
        print(e)
        # 对密码进行加密
        h_pwd = hashlib.md5()
        h_pwd.update(password_1.encode())
        password = h_pwd.hexdigest()
        # 创建用户
        now = datetime.datetime.now()
        try:
            UserInfo.objects.create(username=username, password=password, email=email, is_login=1)
        except Exception as e:
            print(e)
            result = {'code': 10113, 'error': 'Username is already exists'}
            return JsonResponse(result)
        # 创建用户成功,生成token
        token = make_token(username, now)
        result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
        return JsonResponse(result)


# 登录
def login_view(request):
    if request.method != 'POST':
        result = {'code': 10200, 'error': 'Please use post!'}
        return JsonResponse(result)

    # 获取body中的数据
    json_str = request.body
    if not json_str:
        result = {'code': 10201, 'error': 'Please give me data!'}
        return JsonResponse(result)
    json_obj = json.loads(json_str)

    username = json_obj.get('username')
    password = json_obj.get('password')
    if not username:
        result = {'code': 10202, 'error': 'Please enter username!'}
        return JsonResponse(result)
    if not password:
        result = {'code': 10203, 'error': 'Please enter password!'}
        return JsonResponse(result)

    # 对比密码
    p_m = hashlib.md5()
    p_m.update(password.encode())
    user = UserInfo.objects.filter(username=username, password=p_m.hexdigest())
    if not user:
        result = {'code': 10204, 'error': 'Wrong username or wrong password!'}
        return JsonResponse(result)
    # 添加 登录时间
    now = datetime.datetime.now()
    user.login_time = now
    user.save()

    # 生成token
    token = make_token(username, now)
    result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return JsonResponse(result)


# 用户中心
@login_status_check
def userInfo_view(request):
    # 显示用户信心
    if request.method == 'GET':
        user = request.user
        user = UserInfo.objects.filter(username=user.username)[0]
        data = {}
        data['username'] = user.username
        data['nickname'] = user.nickname
        data['email'] = user.email
        data['telephone'] = user.telephone
        result = {'code': 200, 'data': data}
        return JsonResponse(result)
    # 修改用户信息
    elif request.method == 'PUT':
        # 拿数据
        json_str = request.body
        if not json_str:
            result = {'code': 10300, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        nickname = json_obj.get('nickname')
        email = json_obj.get('email')
        telephone = json_obj.get('telephone')
        username = json_obj.get('username')
        # 判断数据
        if not username:
            result = {'code': 10301, 'error': 'Please give username!'}
            return JsonResponse(result)
        if not nickname:
            result = {'code': 10302, 'error': 'Please enter nickname!'}
            return JsonResponse(result)
        if len(nickname) > 32:
            result = {'code': 10303, 'error': 'Length of nickname can not longer than 32bit!'}
            return JsonResponse(result)
        if not telephone:
            result = {'code': 10304, 'error': 'Please enter telephone!'}
            return JsonResponse(result)
        if len(telephone) != 11:
            result = {'code': 10305, 'error': 'length of telephone must be 11!'}
            return JsonResponse(result)
        if not email:
            result = {'code': 10306, 'error': 'Please enter email!'}
            return JsonResponse(result)
        # 判断邮箱格式
        p = re.compile('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        res = p.match(email)
        if not res:
            result = {'code': 10307, 'error': 'The format of the mailbox is incorrect!'}
            return JsonResponse(result)
        if res.group() != email:
            result = {'code': 10308, 'error': 'The format of the mailbox is incorrect!'}
            return JsonResponse(result)
        # 修改数据库
        try:
            user = UserInfo.objects.filter(username=username)[0]
            user.nickname = nickname
            user.telephone = telephone
            user.email = email
            user.save()
        except Exception as e:
            print('update error!')
            print(e)
            result = {'code': 10309, 'error': 'update error!'}
            return JsonResponse(result)


# 收货地址
@login_status_check
def receiver_view(request):
    # 地址列表
    if request.method == 'GET':
        user = request.user
        all_address_info = ReceiverInfo.objects.filter(username=user.username)
        data = []
        for address_info in all_address_info:
            addr = {}
            addr['id'] = address_info.id
            addr['receiver'] = address_info.receiver
            addr['address'] = address_info.address
            addr['receiver_phone'] = address_info.receiver_phone
            addr['is_default'] = address_info.is_default
            data.append(addr)
        result = {'code': 200, 'data': data}
        return JsonResponse(result)
    # 添加地址
    elif request.method == 'POST':
        # 拿数据
        json_str = request.body
        if not json_str:
            result = {'code': 10400, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        receiver = json_obj['receiver']
        address = json_obj['address']
        receiver_phone = json_obj['receiver_phone']
        is_default = json_obj['is_default']
        # 判断数据
        if not receiver:
            result = {'code': 10401, 'error': 'Please enter receiver!'}
            return JsonResponse(result)
        if len(receiver) > 32:
            result = {'code': 10402, 'error': 'Length of receiver can not more than 32bit!'}
            return JsonResponse(result)
        if not address:
            result = {'code': 10403, 'error': 'Please enter address!'}
            return JsonResponse(result)
        if len(address) > 128:
            result = {'code': 10404, 'error': 'Length of address can not more than 128bit!'}
            return JsonResponse(result)
        if not receiver_phone:
            result = {'code': 10405, 'error': 'Please enter receiver_phone!'}
            return JsonResponse(result)
        if len(receiver_phone) != 11:
            result = {'code': 10406, 'error': 'Length of receiver_phone must be 11bit!'}
            return JsonResponse(result)
        # 创建数据
        user = request.user
        try:
            ReceiverInfo.objects.create(receiver=receiver, address=address, receiver_phone=receiver_phone,
                                        is_default=is_default, user=user.username)
        except Exception as e:
            print('create error!')
            print(e)

        result = {'code': 200, 'data': 'append successfully!'}
        return JsonResponse(result)
    # 修改默认地址
    elif request.method == 'PUT':
        json_str = request.body
        if not json_str:
            result = {'code': 10406, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        user = request.user
        addr_id = json_obj['addr_id']
        if not addr_id:
            result = {'code': 10407, 'error': 'Please give me addr_id!'}
            return JsonResponse(result)
        try:
            ReceiverInfo.objects.filter(user=user.username).update(is_default=False)
            address = ReceiverInfo.objects.get(user=user.username, id=addr_id)
            address.update(is_default=True)
            result = {'code': 200, 'data': 'Modify successfully!'}
            return JsonResponse(result)
        except Exception as e:
            print('get error!')
            print(e)
            result = {'code': 10408, 'error': 'address does not exists!'}
            return JsonResponse(result)
    # 删除地址
    elif request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {'code': 10409, 'error': 'Please give me data!'}
            return JsonResponse(result)
        json_obj = json.loads(json_str.decode())
        user = request.user
        addr_id = json_obj['addr_id']
        if not addr_id:
            result = {'code': 10410, 'error': 'Please give me addr_id!'}
            return JsonResponse(result)
        try:
            address = ReceiverInfo.objects.get(user=user.username, id=addr_id)
            address.delete()
            result = {'code': 200, 'data': 'Delete successfully!'}
            return JsonResponse(result)
        except Exception as e:
            print('get error!')
            print(e)
            result = {'code': 10411, 'error': 'address does not exists!'}
            return JsonResponse(result)


def make_token(username, create_datetime, expire=3600 * 24):
    # 生成token
    key = '123456'
    now_t = int(create_datetime.timestamp())
    payload = {'username': username, 'exp': now_t + expire, 'login_time': now_t}
    return jwt.encode(payload, key, algorithm='HS256')


def login_status_check(func):
    def wrapper(request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        if not token:
            result = {'code': 10000, 'error': 'Please login!'}
            return JsonResponse(result)
        try:
            res = jwt.decode(token, 123456)
        except Exception as e:
            print(e)
            result = {'code': 10001, 'error': 'Please login!!'}
            return JsonResponse(result)

        username = res['username']
        try:
            user = UserInfo.objects.get(username=username)
        except Exception as e:
            print(e)
            result = {'code': 10002, 'error': 'Please login!!!'}
            return JsonResponse(result)
        # 判断token创建时间【登录时间】
        token_time = res['login_time']
        user_login_time = int(user.login_time.timestamp())
        if token_time != user_login_time:
            # 已有其他客户端登录此账户
            result = {'code': 10003, 'error': 'Other user is acitved, please login!!!!'}
            return JsonResponse(result)
        func(request, *args, **kwargs)
        # return func(request, *args, **kwargs)

    return wrapper
