from . import views
from django.urls import path
from .serializers import UserSerializer

urlpatterns = [
    path('',views.Userapi.as_view(), name='user-list'),
    path('<int:id>/',views.Userapi.as_view(), name='user-list')
]
