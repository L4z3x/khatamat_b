from django.contrib import admin
from khatma.models import Khatma,khatmaMembership,khatmaGroup,khatmaGroupMembership
# Register your models here.

admin.site.register(Khatma)
admin.site.register(khatmaMembership)
admin.site.register(khatmaGroup)
admin.site.register(khatmaGroupMembership)