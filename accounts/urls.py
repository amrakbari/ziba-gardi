from django.urls import path
from rest_framework.routers import SimpleRouter

from accounts.views import ActivateUser, CreateRetrieveListDeleteUpdateAddressViewSet

router = SimpleRouter()
router.register('addresses', CreateRetrieveListDeleteUpdateAddressViewSet)

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view(), name='activate-user'),
] + router.urls
