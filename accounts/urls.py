from django.urls import path
from rest_framework.routers import SimpleRouter

from accounts.views import ActivateUser, CreateRetrieveListDeleteUpdateAddressViewSet, ListNeighbourhoodViewSet

router = SimpleRouter()
router.register('addresses', CreateRetrieveListDeleteUpdateAddressViewSet, basename='addresses')
router.register('neighbourhoods', ListNeighbourhoodViewSet, basename='neighbourhoods')

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view(), name='activate-user'),
] + router.urls
