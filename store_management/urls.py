from django.urls import path, register_converter, re_path
from rest_framework.routers import SimpleRouter

from store_management.converters import DateConverter
from store_management.views import CreateUpdateRetrieveProfile, CreateRetrieveListUpdateDestroyStore, \
    CreateRetrieveListDestroyUpdateAppointment, CreateRetrieveListService, CurrentUserStoresList, AddServiceToStore, \
    GetAppointmentsOfStore, SetAppointmentForUser, GetServicesOfStore, GetUserFromProfile, GetNearbyStores, \
    GetStoresByService

register_converter(DateConverter, 'date')

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')
router.register('stores', CreateRetrieveListUpdateDestroyStore, basename='stores')
router.register('appointments', CreateRetrieveListDestroyUpdateAppointment, basename='Appointments')
router.register('services', CreateRetrieveListService, basename='Services')

urlpatterns = [
    path('stores/current-user-stores/', CurrentUserStoresList.as_view(),  name='current-user-stores'),
    path('stores/add-service-to-store/', AddServiceToStore.as_view(),  name='add-service-to-store'),
    path('stores/set-appointment-for-user/', SetAppointmentForUser.as_view(),  name='set-appointment-for-user'),
    path('stores/<int:store_pk>/appointments/', GetAppointmentsOfStore.as_view(),  name='appointments-of-store'),
    path('stores/<int:store_pk>/services/', GetServicesOfStore.as_view(),  name='services-of-store'),
    path('stores/profiles/<int:profile_pk>/', GetUserFromProfile.as_view(),  name='user-of-profile'),
    path('stores/get-nearby-stores/<int:address_pk>/', GetNearbyStores.as_view(),  name='get-nearby-stores'),
    path('stores/get-stores-by-service/<int:service_pk>/', GetStoresByService.as_view(),  name='get-stores-by-service'),
] + router.urls
