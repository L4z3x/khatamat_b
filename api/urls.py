from api import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('refreshtoken/',TokenRefreshView.as_view(),name="refresh_token"),
    path('login/',TokenObtainPairView.as_view(),name="get_token"),
    path('signup/',views.CreateUserapi.as_view(), name='user-list'),
    path("update/", views.UpdateUserapi.as_view(), name="update-user"),
    path("delete/<int:id>/", views.DeleteUserapi.as_view(), name="delete-user"),
    path("retreive/<int:id>/", views.ListUserapi.as_view(), name="retreive-user"),
    path("retreive-all/", views.ListUserapi.as_view(), name="retreive-all-users"),
    path("join-request/", views.create_JoinRequest.as_view(), name="send-join-request"),
]  
