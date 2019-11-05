from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^register$', views.register_view),
    url(r'^login$', views.login_view),
    url(r'^checklogin$', views.check_login),
    url(r'^info$', views.userInfo_view),
    url(r'^address$', views.receiver_view),
]
