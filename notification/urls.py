from .views import * 
from django.urls import path
urlpatterns = [
    path("send-join-req/<str:group_name>/", create_JoinRequest.as_view(), name="send join request"),
    path("accept-join-req/<int:id>/",accept_joinReq,name="accept join request"),
    # path("deny-join-req/<int:id>/",deny_joinReq,name="accept join request"), to be added
    # path("list-join-req/<int:id>/",list_joinReq,name="accept join request"), to be added
    path("send-br-req/<int:id>/",send_brothershipReq,name='send brothership request'),
    path("list-br-req/",list_brothershipReq,name='list brothership request'),
    path("accept-br-req/<int:id>/",accept_brothershipReq,name='accept brothership request'),
    path("deny-br-req/<int:id>/",deny_brothershipReq,name='accept brothership request'),
]