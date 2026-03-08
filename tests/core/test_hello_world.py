from django.urls import reverse
from rest_framework import status

from tests.base import BaseTestCase


class HelloWorldViewTestCase(BaseTestCase):
    def test_hello_world_success(self):
        url = reverse("hello-world-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Hello, World!"})
