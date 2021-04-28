from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

USERNAME = 'Tester'
PASSWORD = 'Secretword'


class ApiURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME,
                                            password=PASSWORD,
                                            role='admin')
        cls.token = RefreshToken.for_user(cls.user).access_token
        cls.user_auth = 'Authorization: Bearer ' + str(cls.token)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=self.user_auth)

    def test_auth_url(self):
        self.client.credentials()
        data = {"username": USERNAME, "password": PASSWORD}
        response = self.client.post(reverse('token_obtain_pair'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_url(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
