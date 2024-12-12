from django.urls import path
from khatma.views import * 
from django_channels_jwt.views import AsgiValidateTokenView
urlpatterns = [
    path('auth/',AsgiValidateTokenView.as_view(),name='get uuid ticket'),
    path("khatma/<int:id>/",khatma_details.as_view(),name="retreive or update khatma"),
    path("create-khatma/", create_khatma.as_view(),name="create khatma"),
    path("group/", Group.as_view(),name="create delete group"),
    path("group-settings/<int:id>/",group_settings.as_view(),name="get update group settings"),
    path("add-member-group/<int:group_id>/", add_user_to_group,name="add member to group"),
    path("khatma-membership/<int:id>/", khatma_membership.as_view(),name="add member to khatma"),
    path("list-khatma-membership/", khatma_membership.as_view(),name="list all members of khatma"),
    path("list-khatma/<int:group_id>/", list_khatmas_of_group,name="list khatmas of a group"),
    path("messages/<int:group_id>/", list_messages.as_view(),name="list messages of a khatma"),
    path("media/<int:group_id>/", FileUploadMessage.as_view(),name="upload a file and send in a message"),
]
