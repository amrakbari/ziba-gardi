import pytest
from rest_framework import status

from model_bakery import baker

from accounts.models import CustomUser, Address


@pytest.mark.django_db
class TestAddAddress:
    def test_if_created_successfully_return_201(self, authenticated_client):
        user = baker.make(CustomUser, password='rightPass')
        api_client = authenticated_client(user)

        response = api_client.post(path=r'/accounts/addresses/', data={
            'title': 'test',
            'description': 'test',
            'longitude': '51.134461088535474',
            'latitude': '9.707049018543879',
        })

        assert response.status_code == 201

    def test_if_user_is_not_authenticated_return_401(self, api_client):
        response = api_client.post(path=r'/accounts/addresses/', data={
            'title': 'test',
            'description': 'test',
            'longitude': '51.134461088535474',
            'latitude': '9.707049018543879',
        })

        assert response.status_code == 401

    def test_if_both_long_lat_are_negative_return_201(self, authenticated_client):
        user = baker.make(CustomUser, password='rightPass')
        api_client = authenticated_client(user)
        response = api_client.post('/accounts/addresses/', data={
            'title': 'test',
            'description': 'test',
            'longitude': '-51.134461088535474',
            'latitude': '-9.707049018543879',
        })

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestGetListOfAddresses:
    def test_if_successful_address_users_match_current_user_id_and_return_200(self, authenticated_client):
        user1 = baker.make(CustomUser, password='rightPass')
        user2 = baker.make(CustomUser, password='rightPass')
        api_client = authenticated_client(user1)
        user2_address = baker.make(Address, user=user2)
        user1_addresses = baker.make(Address, 4, user=user1)
        response = api_client.get(path=r'/accounts/addresses/', headers={'Content-Type': 'application/json'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 4
        for item in response.json():
            assert item['user'] == user1.id

    def test_if_not_authenticated_return_401(self, api_client):
        user1 = baker.make(CustomUser, password='rightPass')
        user1_addresses = baker.make(Address, 4, user=user1)
        response = api_client.get(path=r'/accounts/addresses/', headers={'Content-Type': 'application/json'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


