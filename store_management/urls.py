from django.urls import path
from rest_framework.routers import SimpleRouter

from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyStore

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyStore, basename='stores')

urlpatterns = [] + router.urls
