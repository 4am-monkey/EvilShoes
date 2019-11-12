from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'^$', views.order_view),
    url(r'^pay$', views.order_pay_view),
]
