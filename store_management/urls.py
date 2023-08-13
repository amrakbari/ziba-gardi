from django.urls import path, register_converter, re_path
from rest_framework.routers import SimpleRouter

from store_management.converters import DateConverter
from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyStore, \
    CreateRetrieveListDestroyUpdateAppointment, CreateRetrieveListService, CurrentUserStoresList, AddServiceToStore, \
    GetAppointmentsOfStore

register_converter(DateConverter, 'date')

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyStore, basename='stores')
router.register('appointments', CreateRetrieveListDestroyUpdateAppointment, basename='Appointments')
router.register('services', CreateRetrieveListService, basename='Services')

urlpatterns = [
    path('stores/current-user-stores/', CurrentUserStoresList.as_view(),  name='current-user-stores'),
    path('stores/add-service-to-store/', AddServiceToStore.as_view(),  name='add-service-to-store'),
    path('stores/<int:store_pk>/appointments/', GetAppointmentsOfStore.as_view(),  name='appointments-of-store'),
] + router.urls
