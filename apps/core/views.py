from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CoreView(GenericViewSet):
    def list(self, request):
        return Response({"message": "Hello, World!"})
