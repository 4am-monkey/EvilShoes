from django.conf.urls import url

from commodity import views

urlpatterns = [
    # 127.0.0.1:8000/commodity
    url(r'^$', views.all_commodity),

    # 127.0.0.1:8000/commodity/classify
    url(r'^classify$', views.classify_view),

    # 127.0.0.1:8000/commodity/<typename>
    url(r'type/(?P<typename>\w+)$', views.classify_commodity),

    # 127.0.0.1:8000/commodity/<commodityid>
    url(r'detail/(?P<commodityid>\w+)$', views.commodity_details),

    url(r'^search$', views.search),

    url(r'^buy$', views.buy_now)
]
