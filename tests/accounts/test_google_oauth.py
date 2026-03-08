from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from tests.base import BaseTestCase


class GoogleOAuthApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("google-oauth")

    @patch("apps.accounts.services.google_oauth.id_token.verify_oauth2_token")
    def test_google_login_creates_user(self, mock_verify):
        mock_verify.return_value = {
            "iss": "accounts.google.com",
            "sub": "google-uid-123",
            "email": "jane@example.com",
            "given_name": "Jane",
            "family_name": "Doe",
            "email_verified": True,
        }

        response = self.client.post(self.url, {"credential": "fake-token"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["user"]["email"], "jane@example.com")
        self.assertIn("access", data["tokens"])
        self.assertIn("refresh", data["tokens"])

    def test_google_login_missing_credential(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
