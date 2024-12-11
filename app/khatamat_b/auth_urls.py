from django.urls import path, include
from utils import GoogleLogin
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path("", include("dj_rest_auth.urls")), # dj_rest_auth urls
    path("registration/", include("dj_rest_auth.registration.urls")), # dj_rest_auth registration urls
    path("password/reset/confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(),name="password_reset_confirm"), # dj_rest_auth password reset urls
    # path("social/", include("allauth.socialaccount.urls")), # allauth socialaccount urls   
    path("google/", GoogleLogin.as_view() ), # google social login urls
]