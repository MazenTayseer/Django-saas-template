from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import LoginView, SignupView

router = DefaultRouter()
router.register(r"signup", SignupView, basename="signup")
router.register(r"login", LoginView, basename="login")

urlpatterns = [
    *router.urls,
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
