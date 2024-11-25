from api import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
urlpatterns = [
    path('refreshtoken/',TokenRefreshView.as_view(),name="refresh_token"),
    path('login/',TokenObtainPairView.as_view(),name="get_token"),
    path('signup/',views.CreateUser, name='user-list'),
    path("delete/<int:user_id>/", views.DeleteUser.as_view(), name="delete-user"),
    path("retreive/<int:user_id>/", views.ListUserapi.as_view(), name="retreive-user"),
    path("retreive-all/", views.ListUserapi.as_view(), name="retreive-all-users"), # to be removed in production
    path("update/", views.updateUser , name="update-user"),
    path("list-brother/",views.brother.as_view(),name="get the user's brothers"),
    path("delete-brother/<int:user_id>/",views.deleteBrother ,name="delete brother from brother List"),
    path("mutual-brother/<int:user_id>/",views.mutualBrother ,name="ger mutuals brothers"),
    path("list-blocked/",views.list_blocked ,name="list blocked brothers"),
    path("block-brother/<int:user_id>/",views.blockBrother ,name="blocke brother"),
    
]
