from django.urls import path
from .consumers import *
urlpatterns = [
    path('chat/group/<int:group_id>/',groupConsumer.as_asgi(),name='group chat'),
    
] 