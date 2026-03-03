from core.views import CoreView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", CoreView, basename="core")

urlpatterns = router.urls
