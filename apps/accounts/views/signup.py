from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.accounts.serializers import SignupSerializer, UserSerializer


class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
