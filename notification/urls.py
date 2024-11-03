from .views import * 
from django.urls import path
urlpatterns = [
    path("send-join-request/<str:group_name>/", create_JoinRequest.as_view(), name="send join request"),
    path("send-br-req/<int:id>/",send_brothershipReq,name='send brothership request'),
    path("list-br-req/",list_brothershipReq,name='list brothership request'),
    path("accept-br-req/<int:id>/",accept_brothershipReq,name='accept brothership request'),
    path("deny-br-req/<int:id>/",deny_brothershipReq,name='accept brothership request'),
]