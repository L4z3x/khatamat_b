from .views import * 
from django.urls import path
urlpatterns = [
    # path("send-join-req/<int:community_id>/",create_JoinRequest.as_view(),name='send community joinrequest(if authentication is not none)'),
    # path("accept-join-req/<int:sender_id>/",accept_joinReq,name="accept join request to community"),
    path("send-br-req/<str:username>/",send_brothershipReq,name='send brothership request'),
    path("list-br-req/",list_brothershipReq,name='list brothership request'),
    path("accept-br-req/<int:user_id>/",accept_brothershipReq,name='accept brothership request'),
    path("deny-br-req/<int:brothershipReq_id>/",deny_brothershipReq,name='accept brothership request'),
]