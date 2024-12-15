from django.urls import path
from khatma.views import * 
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
    # khatma urls
    path("khatma/<int:id>/",khatma_details.as_view(),name="retreive or update khatma"),
    path("create-khatma/", create_khatma.as_view(),name="create khatma"),
    path("khatma-membership/<int:id>/", khatma_membership.as_view(),name="update khatma membership"),
    path("list-khatma-membership/", khatma_membership.as_view(),name="list all members of khatma"),
    path("list-khatma/<int:group_id>/", list_khatmas_of_group,name="list khatmas of a group"),
    # message urls
    path("messages/<int:group_id>/", list_messages.as_view(),name="list messages of a khatma"),
    path("media/<int:group_id>/", FileUploadMessage.as_view(),name="upload a file and send in a message"),
]
