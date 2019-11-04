from django.contrib import admin

# Register your models here.
from user.models import *

admin.site.register(UserInfo)
admin.site.register(ReceiverInfo)
