from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from . import views
import api.urls 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import rest_framework.urls


urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('api-auth/',include('rest_framework.urls')),
    path('api/',include(api.urls)),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html'))

]
