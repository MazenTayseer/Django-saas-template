from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.base import BaseTestCase
from tests.factories import UserFactory


class LoginTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = reverse("login-list")
        self.user = UserFactory(email="login@example.com", phone_number="+442071234568")

    def test_login_with_email_success(self):
        data = {
            "identifier": self.user.email,
            "password": "Test1234!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.json())
        self.assertIn("tokens", response.json())
        self.assertEqual(response.json()["user"]["email"], self.user.email)
        self.assertIn("access", response.json()["tokens"])
        self.assertIn("refresh", response.json()["tokens"])

    def test_login_with_phone_success(self):
        data = {
            "identifier": str(self.user.phone_number),
            "password": "Test1234!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["user"]["phone_number"], "+442071234568")

    def test_login_invalid_credentials_fails(self):
        data = {
            "identifier": self.user.email,
            "password": "WrongPassword123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
