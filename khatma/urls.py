from django.urls import path
from khatma import views
from django_channels_jwt.views import AsgiValidateTokenView
urlpatterns = [
    path('auth/',AsgiValidateTokenView.as_view(),name='get uuid ticket'),
    path("create/",views.CreateKhatma.as_view(),name="create khatma"),
    path("retreive/<str:kh_name>/",views.getkhatma.as_view(),name="retreive khatma"),
    path("create-khatma-group/",views.CreateKhatmaGroup.as_view(),name="create khatma group"),
    path("add-member-kg/",views.khatma_G_memb.as_view(),name="add member to khatmaGroup"),
    path("add-member-k/",views.khatma_memb.as_view(),name="add member to khatma"),
]