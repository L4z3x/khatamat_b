from . import views
from django.urls import path
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),
    path('login/token/',TokenObtainPairView.as_view(),name="get_token"),
    path('user/signup/',views.CreateUserapi.as_view(), name='user-list'),
    path("user/update/", views.UpdateUserapi.as_view(), name="update-user"),
    path("user/delete/", views.DeleteUserapi.as_view(), name="delete-user"),
    path("user/retreive/<int:id>/", views.ListUserapi.as_view(), name="retreive-user"),
    path("user/retreive-all/", views.ListUserapi.as_view(), name="retreive-all-users"),
]
