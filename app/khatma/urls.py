from django.urls import path
from khatma.views import * 

urlpatterns = [
    path("khatma/<int:id>/",khatma_details.as_view(),name="retreive or update khatma"),
    path("create-khatma/", create_khatma.as_view(),name="create khatma"),
    path("khatma-membership/<int:id>/", khatma_membership.as_view(),name="update khatma membership"),
    path("list-khatma-membership/", khatma_membership.as_view(),name="list all members of khatma"),
    path("list-khatma/<int:group_id>/", list_khatmas_of_group,name="list khatmas of a group"),
]
