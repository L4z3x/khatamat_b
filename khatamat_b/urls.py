from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
import api.urls 
import khatma.urls
import rest_framework.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include(rest_framework.urls)),
    path('api/',include(api.urls)),
    path('khatma/',include(khatma.urls)),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html'))
]
