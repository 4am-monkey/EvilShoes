from django.db import models


# Create your models here.
# 用户信息表
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, primary_key=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=255, default='')
    telephone = models.CharField(verbose_name='手机号码', max_length=11)
    # gender = models.BooleanField(verbose_name='性别', max_length=1, choices=((0, '男'), (1, '女')))
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    login_time = models.DateTimeField(verbose_name='登录时间')

    # is_login = models.SmallIntegerField(verbose_name='登录状态', default=0)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        return self.username


# 收货人信息表
class ReceiverInfo(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='所属用户')
    receiver = models.CharField(max_length=32, verbose_name='收货人')
    address = models.CharField(max_length=648, verbose_name='收货地址')
    receiver_phone = models.CharField(max_length=11, verbose_name='收货人电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'receiver_info'
        verbose_name = '收件人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        """
            定义每个数据对象的显示信息
        """
        return self.receiver
