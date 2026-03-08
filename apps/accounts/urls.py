from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import LoginView, SignupView
from apps.accounts.views.google_oauth import GoogleOAuthView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("google/oauth/", GoogleOAuthView.as_view(), name="google-oauth"),
]
