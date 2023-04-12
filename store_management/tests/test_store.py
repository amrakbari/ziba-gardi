import pytest
from rest_framework import status

from model_bakery import baker

from accounts.models import Address, CustomUser
from store_management.models import Store, UserProfile


@pytest.mark.django_db
class TestCreateStore:
    def test_if_created_successfully_return_201(self, authenticated_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)
        address = baker.make(Address, user=user)
        api_client = authenticated_client(user)

        response = api_client.post(path=r'/accounts/stores/', data={
            'title': 'sample store',
            'address': address.id,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('stylist') == profile

    def test_if_not_authenticated_return_401(self, api_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)
        address = baker.make(Address, user=user)

        response = api_client.post(path=r'/accounts/stores/', data={
            'title': 'sample store',
            'address': address.id,
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_address_does_not_exist_return_404_or_not_for_current_user(self, authenticated_client):
        user = baker.make(CustomUser)
        profile = baker.make(UserProfile, user=user)
        address = baker.make(Address, user=user)
        api_client = authenticated_client(user)

        response = api_client.post(path=r'/accounts/stores/', data={
            'title': 'sample store',
            'address': address.id + 1,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('stylist') == profile


@pytest.mark.django_db
class TestListStore:
    def test_if_successful_return_200_and_stores_are_for_current_user(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_addr = baker.make(Address, user=user1)
        user2_addr = baker.make(Address, user=user2)
        user1_stores = baker.make(Store, 4, user=user1, address=user1_addr)
        user2_stores = baker.make(Store, 5, user=user2, address=user2_addr)
        api_client = authenticated_client(user1)

        response = api_client.get(path=r'/accounts/stores/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(user1_stores)

    def test_if_not_authenticated_return_401(self, api_client):
        user1 = baker.make(CustomUser)
        address = baker.make(Address, user=user1)
        stores = baker.make(Store, 4, user=user1, address=address)

        response = api_client.get(path=r'/accounts/stores/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_current_user_has_no_store_return_200_and_empty_list(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_addr = baker.make(Address, user=user1)
        user2_addr = baker.make(Address, user=user2)
        user2_stores = baker.make(Store, 5, user=user2, address=user2_addr)
        api_client = authenticated_client(user1)

        response = api_client.get(path=r'/accounts/stores/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0


@pytest.mark.djamgo_db
class TestRetrieveStore:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_addr = baker.make(Address, user=user1)
        user2_addr = baker.make(Address, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_addr)
        user2_stores = baker.make(Store, 5, user=user2, address=user2_addr)
        api_client = authenticated_client(user1)

        response = api_client.get(path=fr'/accounts/stores/{user1_store.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('id') == user1_store.id

    def test_if_not_authenticated_return_401(self, api_client):
        user = baker.make(CustomUser)
        address = baker.make(Address, user=user)
        store = baker.make(Store, user=user, address=address)

        response = api_client.get(path=fr'/accounts/stores/{store.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_store_id_is_not_for_the_current_user_return_404(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_addr = baker.make(Address, user=user1)
        user2_addr = baker.make(Address, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_addr)
        user2_store = baker.make(Store, user=user2, address=user2_addr)
        api_client = authenticated_client(user1)

        response = api_client.get(path=fr'/accounts/stores/{user2_store.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateStorePut:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client):
        user = baker.make(CustomUser)
        address1 = baker.make(Address, user=user)
        address2 = baker.make(Address, user=user)
        store = baker.make(Store, user=user, address=address1)
        sample_data = {
            'title': 'test update',
            'address': address2.id
        }
        api_client = authenticated_client(user)

        response = api_client.put(path=fr'/accounts/stores/{store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('title') == sample_data.get('title')
        assert response.json().get('address') == sample_data.get('address')

    def test_if_not_authenticated_return_401(self, api_client):
        user = baker.make(CustomUser)
        address1 = baker.make(Address, user=user)
        address2 = baker.make(Address, user=user)
        store = baker.make(Store, user=user, address=address1)
        sample_data = {
            'title': 'test update',
            'address': address2.id
        }

        response = api_client.put(path=fr'/accounts/stores/{store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_store_id_is_not_for_the_current_user_return_404(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_address1 = baker.make(Address, user=user1)
        user1_address2 = baker.make(Address, user=user1)
        user2_address = baker.make(Address, user=user2)
        user1_profile = baker.make(UserProfile, user=user1)
        user2_profile = baker.make(UserProfile, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_address1)
        user2_store = baker.make(Store, user=user2, address=user2_address)
        api_client = authenticated_client(user1)

        sample_data = {
            'title': 'test update',
            'address': user1_address2.id
        }
        response = api_client.put(path=fr'/accounts/stores/{user2_store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_address_id_is_not_for_the_current_user_return_404(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_address = baker.make(Address, user=user1)
        user2_address = baker.make(Address, user=user2)
        user1_profile = baker.make(UserProfile, user=user1)
        user2_profile = baker.make(UserProfile, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_address)
        user2_store = baker.make(Store, user=user2, address=user2_address)
        api_client = authenticated_client(user1)

        sample_data = {
            'title': 'test update',
            'address': user2_address.id
        }
        response = api_client.put(path=fr'/accounts/stores/{user2_store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdateStorePatch:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client):
        user = baker.make(CustomUser)
        address1 = baker.make(Address, user=user)
        address2 = baker.make(Address, user=user)
        store = baker.make(Store, user=user, address=address1)

        sample_data = {
            'address': address2.id
        }
        api_client = authenticated_client(user)
        response = api_client.patch(path=fr'/accounts/stores/{store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('address') == sample_data.get('address')

    def test_if_not_authenticated_return_401(self, api_client):
        user = baker.make(CustomUser)
        address1 = baker.make(Address, user=user)
        address2 = baker.make(Address, user=user)
        store = baker.make(Store, user=user, address=address1)
        sample_data = {
            'address': address2.id
        }

        response = api_client.patch(path=fr'/accounts/stores/{store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_store_id_is_not_for_the_current_user_return_404(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_address1 = baker.make(Address, user=user1)
        user1_address2 = baker.make(Address, user=user1)
        user2_address = baker.make(Address, user=user2)
        user1_profile = baker.make(UserProfile, user=user1)
        user2_profile = baker.make(UserProfile, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_address1)
        user2_store = baker.make(Store, user=user2, address=user2_address)
        api_client = authenticated_client(user1)

        sample_data = {
            'title': 'test update',
        }
        response = api_client.patch(path=fr'/accounts/stores/{user2_store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_address_id_is_not_for_the_current_user_return_404(self, authenticated_client):
        user1 = baker.make(CustomUser)
        user2 = baker.make(CustomUser)
        user1_address = baker.make(Address, user=user1)
        user2_address = baker.make(Address, user=user2)
        user1_profile = baker.make(UserProfile, user=user1)
        user2_profile = baker.make(UserProfile, user=user2)
        user1_store = baker.make(Store, user=user1, address=user1_address)
        user2_store = baker.make(Store, user=user2, address=user2_address)
        api_client = authenticated_client(user1)

        sample_data = {
            'address': user2_address.id
        }
        response = api_client.patch(path=fr'/accounts/stores/{user1_store.id}/', data=sample_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteStore:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client): ...

    def test_if_not_authenticated_return_401(self, api_client): ...

    def test_if_store_id_is_not_for_the_current_user(self, authenticated_client): ...
