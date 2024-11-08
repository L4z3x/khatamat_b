from django.contrib import admin
from khatma.models import *
# Register your models here.

admin.site.register(Khatma)
admin.site.register(khatmaMembership)
admin.site.register(khatmaGroup)
admin.site.register(khatmaGroupMembership)
admin.site.register(message)