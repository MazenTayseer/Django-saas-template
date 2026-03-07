from rest_framework.routers import DefaultRouter

from apps.core.views import CoreView

router = DefaultRouter()
router.register(r"", CoreView, basename="core")

urlpatterns = router.urls
