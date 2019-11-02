from django.contrib import admin

# Register your models here.
from commodity.models import *

admin.site.register(CommodityInfo)
admin.site.register(CommodityClassify)
