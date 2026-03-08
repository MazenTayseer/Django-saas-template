from rest_framework.routers import DefaultRouter

from apps.core.views.hello_world import HelloWorldView

router = DefaultRouter()
router.register(r"", HelloWorldView, basename="hello-world")

urlpatterns = router.urls
