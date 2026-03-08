from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.google_oauth import GoogleOAuthInputSerializer
from apps.accounts.serializers.user import UserSerializer
from apps.accounts.services.google_oauth import GoogleOAuthService
from apps.accounts.utils.tokens import get_tokens_for_user


class GoogleOAuthView(APIView):
    def post(self, request):
        serializer = GoogleOAuthInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get("credential")
        service = GoogleOAuthService()
        user = service.authenticate(token)

        return Response(
            {
                "user": UserSerializer(user).data,
                "tokens": get_tokens_for_user(user),
            },
            status=status.HTTP_200_OK,
        )
