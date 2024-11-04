from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
import api.urls,khatma.urls,notification.urls 
import rest_framework.urls
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('api-auth/',include(rest_framework.urls)),
    path('schema/',SpectacularAPIView.as_view(),name="schema"),
    path('schema/docs/',SpectacularSwaggerView.as_view(url_name="schema"),name="api docs"),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/',include(api.urls)),
    path('khatma/',include(khatma.urls)),
    path('notification/',include(notification.urls)),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html')),
] 
