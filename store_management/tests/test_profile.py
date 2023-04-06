import pytest
from rest_framework import status

from model_bakery import baker

from accounts.models import CustomUser
from store_management.models import UserProfile


@pytest.mark.django_db
class TestCreateProfile:
    def test_if_successful_return_201(self, api_client):
        user = baker.make(CustomUser)

        response = api_client.post(path=fr'/store/stylist-profiles/', data={
            'user': user.id,
            'role': 'US',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_profile_for_that_user_already_exists_return_400(self, api_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)

        response = api_client.post(path=fr'/store/stylist-profiles/', data={
            'user': user.id,
            'role': 'US',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_role_is_not_acceptable_return_400(self, api_client):
        user = baker.make(CustomUser)

        response = api_client.post(path=fr'/store/stylist-profiles/', data={
            'user': user.id,
            'role': 'NA',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateProfile:
    def test_if_successful_return_200_and_response_matches_put(self, authenticated_client):
        user = baker.make(CustomUser)
        api_client = authenticated_client(user)

        response = api_client.put(path=fr'/store/stylist-profiles/', data={
            'role': 'US',
            'birth_date': '2020-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('birth_date') == '2020-11-01T00:00:00'

    def test_if_successful_return_200_and_response_matches_patch(self, authenticated_client):
        user = baker.make(CustomUser)
        api_client = authenticated_client(user)

        response = api_client.patch(path=fr'/store/stylist-profiles/', data={
            'birth_date': '2020-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('birth_date') == '2020-11-01T00:00:00'

    def test_if_not_authenticated_return_401(self, authenticated_client):
        user = baker.make(CustomUser)
        api_client = authenticated_client(user)

        response = api_client.patch(path=fr'/store/stylist-profiles/', data={
            'birth_date': '2020-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


