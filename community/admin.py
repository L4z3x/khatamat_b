from django.contrib import admin
from .models import *

admin.site.register(community)
admin.site.register(communityMembership)
admin.site.register(post)
admin.site.register(comment)