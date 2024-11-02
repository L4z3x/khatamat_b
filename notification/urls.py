from .views import * 
from django.urls import path
urlpatterns = [
    path("join-request/", create_JoinRequest.as_view(), name="send join request"),
    path("send-br-req/",send_brothershipReq,name='send brothership request'),
    path("list-br-req/",list_brothershipReq,name='list brothership request'),
    path("accept-br-req/",accept_brothershipReq,name='accept brothership request'),
]