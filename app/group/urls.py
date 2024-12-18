from django.urls import path
from .views import *
from .views_message import *
from django_channels_jwt.views import AsgiValidateTokenView


urlpatterns = [ 
    # consumer auth url 
    path('auth/',AsgiValidateTokenView.as_view(),name='get uuid ticket'),
    
    # group urls
    path("group/", Group.as_view(),name="create delete group"),
    path("group-settings/<int:id>/",group_settings.as_view(),name="get update group settings"),
    path("add-member-group/<int:group_id>/", add_user_to_group,name="add member to group"),
    path("remove-member-group/<int:group_id>/<int:user_id>/", kick_user,name="remove member from group"),
    path("change-member-role/<int:group_id>/<int:user_id>/", change_user_role, name="change member role in group"),
    path("generate-group-code/<int:group_id>/", generate_group_code,name="generate group code"),
    path("join-group-by-code/", join_group_by_code,name="join group"),
    path("deactivate-group-code/", deactivate_group_code,name="deactivate group code"),
    
   # message urls
    path("messages/<int:group_id>/", list_messages.as_view(),name="list messages of a khatma"),
    path("media/<int:group_id>/", FileUploadMessage.as_view(),name="upload a file and send in a message"),
]