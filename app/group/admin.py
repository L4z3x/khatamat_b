from django.contrib import admin
from .models import  *

admin.site.register(group)
admin.site.register(groupMembership)
admin.site.register(message)
admin.site.register(groupSettings)
admin.site.register(media)
admin.site.register(groupCode)  