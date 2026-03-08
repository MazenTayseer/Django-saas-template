from django.urls import path

from apps.core.views.hello_world import HelloWorldView

urlpatterns = [
    path("", HelloWorldView.as_view(), name="hello-world"),
]
