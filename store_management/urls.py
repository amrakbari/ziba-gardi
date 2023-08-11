from django.urls import path
from rest_framework.routers import SimpleRouter

from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyStore, \
    CreateRetrieveListDestroyUpdateAppointment, CreateRetrieveListService, CurrentUserStoresList

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyStore, basename='stores')
router.register('appointments', CreateRetrieveListDestroyUpdateAppointment, basename='Appointments')
router.register('services', CreateRetrieveListService, basename='Services')

urlpatterns = [
    path('stores/current-user-stores/', CurrentUserStoresList.as_view(),  name='current-user-stores'),
] + router.urls
