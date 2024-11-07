from django_channels_jwt.urls import AsgiValidateTokenView
from django.urls import re_path
from .consumers import *
urlpatterns = [
    re_path(r'chat/group/',khatmaGroupConsumer.as_asgi(),name='messaging the group'),
    # re_path(r'/chat/brother',), for brothers only
    
] 