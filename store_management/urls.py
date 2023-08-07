from django.urls import path
from rest_framework.routers import SimpleRouter

from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyStore, CreateRetrieveListDestroyUpdateAppointment, CreateRetrieveListService

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyStore, basename='stores')
router.register('appointments', CreateRetrieveListDestroyUpdateAppointment, basename='Appointments')
router.register('services', CreateRetrieveListService, basename='Services')

urlpatterns = [] + router.urls
