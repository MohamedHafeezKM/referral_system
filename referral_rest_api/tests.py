from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from referral_rest_api.models import UserInfo
from django.contrib.auth.models import User


class UserinfoAPITest(APITestCase):
    def test_create_object(self):
        response = self.client.post('Userinfo/api//', {'name': 'Test Object'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)