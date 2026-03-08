from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.core.models import User
from tests.base import BaseTestCase
from tests.factories import UserFactory


class SignupTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = reverse("signup-list")

    def test_signup_with_email_success(self):
        data = {
            "email": "user@example.com",
            "password": "SecurePass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.json())
        self.assertIn("tokens", response.json())
        self.assertEqual(response.json()["user"]["email"], "user@example.com")
        self.assertIn("access", response.json()["tokens"])
        self.assertIn("refresh", response.json()["tokens"])
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_signup_with_phone_success(self):
        data = {
            "phone_number": "+442071234567",
            "password": "SecurePass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.json())
        self.assertIn("tokens", response.json())
        self.assertTrue(User.objects.filter(phone_number="+442071234567").exists())

    def test_signup_with_email_and_phone_success(self):
        data = {
            "email": "full@example.com",
            "phone_number": "+442071234569",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data = response.json()["user"]
        self.assertEqual(user_data["email"], "full@example.com")
        self.assertEqual(user_data["first_name"], "John")
        self.assertEqual(user_data["last_name"], "Doe")

    def test_signup_without_email_or_phone_fails(self):
        data = {
            "password": "SecurePass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["messages"], ["At least one of email or phone number is required."])

    def test_signup_duplicate_email_fails(self):
        UserFactory(email="existing@example.com")
        data = {
            "email": "existing@example.com",
            "password": "AnotherPass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["messages"], ["A user with this email already exists."])
