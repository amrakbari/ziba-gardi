import pytest
from rest_framework import status

from model_bakery import baker

from accounts.models import CustomUser
from store_management.models import UserProfile


@pytest.mark.django_db
class TestCreateProfile:
    def test_if_successful_return_201(self, api_client):
        user = baker.make(CustomUser)

        response = api_client.post(path=fr'/store/profiles/', data={
            'user': user.id,
            'role': 'US',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_profile_for_that_user_already_exists_return_400(self, api_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)

        response = api_client.post(path=fr'/store/profiles/', data={
            'user': user.id,
            'role': 'US',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_role_is_not_acceptable_return_400(self, api_client):
        user = baker.make(CustomUser)

        response = api_client.post(path=fr'/store/profiles/', data={
            'user': user.id,
            'role': 'NA',
            'birth_date': '2017-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetProfile:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_profile = baker.make(UserProfile, user=user1)
        user2_profile = baker.make(UserProfile, user=user2)
        api_client = authenticated_client(user2)

        response = api_client.get(path=r'/store/profiles/get_current_user_profile/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('user') == user2.id

    def test_if_not_authenticated_return_401(self, api_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)

        response = api_client.get(path=r'/store/profiles/get_current_user_profile/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestUpdateProfile:
    def test_if_successful_return_200_and_response_matches_patch(self, authenticated_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)
        api_client = authenticated_client(user)

        response = api_client.patch(path=fr'/store/profiles/update_current_user_profile/', data={
            'birth_date': '2020-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('birth_date') == '2020-11-01T00:00:00Z'

    def test_if_not_authenticated_return_401(self, authenticated_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)
        api_client = authenticated_client(user)

        response = api_client.patch(path=fr'/store/profiles/update_current_user_profile/', data={
            'birth_date': '2020-11-01T00:00:00',
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


