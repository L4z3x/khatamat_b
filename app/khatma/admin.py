from django.contrib import admin
from khatma.models import *
# Register your models here.

admin.site.register(Khatma)
admin.site.register(khatmaMembership)
admin.site.register(group)
admin.site.register(groupMembership)
admin.site.register(message)
admin.site.register(groupSettings)
admin.site.register(media)