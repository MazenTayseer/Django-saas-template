from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class HelloWorldView(GenericViewSet):
    def list(self, request):
        return Response({"message": "Hello, World!"})
