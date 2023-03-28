import pytest
from rest_framework import status

from model_bakery import baker

from accounts.models import CustomUser


@pytest.mark.django_db
class TestAddAddress:
    def test_address_if_created_successfully_return_201(self, api_client):
        user = baker.make(CustomUser, password='rightPass')
        api_client.force_authenticate(user=user)

        response = api_client.post(path=r'/accounts/addresses/', data={
            'title': 'test',
            'description': 'test',
            'longitude': '51.134461088535474',
            'latitude': '9.707049018543879',
        })

        assert response.status_code == 201
