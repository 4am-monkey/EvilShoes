from django.conf.urls import url

from commodity import views

urlpatterns = [
    # 127.0.0.1:8000/commodity
    url(r'^$', views.GoodsInfo),
    # 127.0.0.1:8000/commodity/classify
    url(r'^classify$', views.GoodsType),
]
