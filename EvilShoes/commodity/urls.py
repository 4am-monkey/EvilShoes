from django.conf.urls import url

from commodity import views

urlpatterns = [
    url(r'^$', views.GoodsInfo),
    url(r'^/(?P<classifyid>\w+)$', views.GoodsType),
]
