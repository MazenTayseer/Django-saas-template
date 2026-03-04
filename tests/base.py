from django.test import Client, TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
