from django.urls import path
from khatma import views

urlpatterns = [
    path("create/",views.CreateKhatma.as_view(),name="create khatma"),
    path("retreive/",views.getkhatma.as_view(),name="retreive khatma"),
]