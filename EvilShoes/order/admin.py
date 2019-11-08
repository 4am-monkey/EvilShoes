from django.contrib import admin

# Register your models here.
from order.models import *

admin.site.register(OrderInfo)
admin.site.register(OrderGoods)
