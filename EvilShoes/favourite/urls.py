from django.conf.urls import url

from favourite import views

urlpatterns = [
    url(r'^$', views.favourite_view)
]
