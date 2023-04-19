from django.urls import path
from rest_framework.routers import SimpleRouter

from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyProfile

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyProfile, basename='stores')

urlpatterns = [] + router.urls
