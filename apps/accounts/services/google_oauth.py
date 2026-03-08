from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.accounts.exceptions import GoogleOAuthError
from apps.core.models import User


class GoogleOAuthService:
    def authenticate(self, token: str) -> User:
        payload = self._validate_token(token)
        email = payload.get("email")
        google_id = payload.get("sub")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": payload.get("given_name"),
                "last_name": payload.get("family_name"),
                "google_id": google_id,
            },
        )

        if not created and not user.google_id:
            user.google_id = google_id
            user.save(update_fields=["google_id", "updated_at"])

        return user

    def _validate_token(self, token: str) -> dict:
        try:
            payload = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except Exception:
            raise GoogleOAuthError("Invalid Google ID token.")

        if payload.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
            raise GoogleOAuthError("Invalid token issuer.")

        return payload
