import jwt
import pytest
from rest_framework.test import APIClient
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken
from ziba_gardi import settings


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(jwt_token):
    def do_authenticate(user: CustomUser):
        api_client = APIClient()
        token = AccessToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        return api_client

    return do_authenticate


@pytest.fixture
def jwt_token():
    def do_create(user: CustomUser):
        payload = {
            'user_id': user.id,
            'email': user.email,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return do_create
