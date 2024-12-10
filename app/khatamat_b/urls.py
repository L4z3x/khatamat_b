from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView
from khatamat_b import auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/',SpectacularAPIView.as_view(),name="schema"),
    path('schema/docs/',SpectacularSwaggerView.as_view(url_name="schema"),name="api docs"),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/',include("api.urls")),
    path('khatma/',include("khatma.urls")),
    path('notification/',include("notification.urls")),
    path("auth/", include(auth_urls)), # dj_rest_auth urls
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
