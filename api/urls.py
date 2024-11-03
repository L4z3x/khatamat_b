from api import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('refreshtoken/',TokenRefreshView.as_view(),name="refresh_token"),
    path('login/',TokenObtainPairView.as_view(),name="get_token"),
    path('signup/',views.CreateUserapi.as_view(), name='user-list'),
    path("delete/<int:id>/", views.DeleteUserapi.as_view(), name="delete-user"),
    path("retreive/<int:id>/", views.ListUserapi.as_view(), name="retreive-user"),
    path("retreive-all/", views.ListUserapi.as_view(), name="retreive-all-users"), # to be removed in production
    path("update/", views.updateUser , name="update-user"),
    path("list-brother/<int:id>/",views.brother.as_view(),name="get user's brothers"),
    path("delete-brother/<int:id>/",views.deleteBrother ,name="delete brother from brother List"),
    path("mutual-brother/<int:id>/",views.mutualBrother ,name="ger mutuals brothers"),
]
