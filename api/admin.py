from django.contrib import admin
from .models import MyUser,Notification,joinRequest
# Register your models here.


admin.site.register(MyUser)
admin.site.register(Notification)
admin.site.register(joinRequest)