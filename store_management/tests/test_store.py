import pytest
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateStore:
    def test_if_created_successfully_return_201(self, authenticated_client): ...

    def test_if_not_authenticated_return_401(self, api_client): ...

    def test_address_does_not_exist_return_404(self, authenticated_client): ...



@pytest.mark.django_db
class TestListStore:
    def test_if_successful_return_200_and_stores_are_for_current_user(self, authenticated_client): ...

    def test_if_not_authenticated_return_401(self, api_client): ...

    def test_if_current_user_has_no_store_return_200_and_empty_list(self, authenticated_client): ...


@pytest.mark.djamgo_db
class TestRetrieveStore:
    def test_if_successful_return_200_and_response_matches(self, authenticated_client): ...

    def test_if_not_authenticated_return_401(self, api_client): ...

    def test_if_store_id_is_not_for_the_current_user_return_404(self, authenticated_client): ...

