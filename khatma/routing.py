from django_channels_jwt.urls import AsgiValidateTokenView
from django.urls import path
from .consumers import *
urlpatterns = [
    path('chat/group/<int:group_id>/',groupConsumer.as_asgi(),name='messaging the group'),
    # re_path(r'/chat/broter',), for brothers only
    
] 