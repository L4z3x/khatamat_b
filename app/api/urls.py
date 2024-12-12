from api.views import *
from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet 

urlpatterns = [
    path("delete/<int:user_id>/", DeleteUser.as_view(), name="delete-user"),
    
    path("usersettings/<int:user_id>/", User_Setting.as_view(),name="get user settings"),
    
    path("list-friends/", brother.as_view(),name="get the user's brothers"),
    
    path("delete-brother/<int:user_id>/", deleteBrother ,name="delete brother from brother List"),
    
    path("mutual-brother/<int:user_id>/", mutualBrother ,name="ger mutuals brothers"),
    
    path("list-blocked/", list_blocked ,name="list blocked brothers"),
    
    path("block-user/<int:user_id>/", blockBrother ,name="blocke brother"),
    
    path("fcm-device/", FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name="create_fcm_device"),
]
