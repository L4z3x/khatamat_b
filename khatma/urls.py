from django.urls import path
from khatma import views
from django_channels_jwt.views import AsgiValidateTokenView
urlpatterns = [
    path('auth/',AsgiValidateTokenView.as_view(),name='get uuid ticket'),
    path("khatma/<int:id>/",views.khatma_details.as_view(),name="retreive or update khatma"),
    path("khatma/",views.khatma_details.as_view(),name="create khatma"),
    path("group/",views.Group.as_view(),name="create khatma group"),
    path("add-member-group/<int:id>/",views.add_user_to_group,name="add member to khatmaGroup"),
    path("khatma-membership/<int:id>/",views.khatma_membership.as_view(),name="add member to khatma"),
    path("khatma-membership/",views.khatma_membership.as_view(),name="add member to khatma"),
]