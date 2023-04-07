from django.urls import path
from rest_framework.routers import SimpleRouter

from store_management.views import CreateUpdateRetrieveProfile

router = SimpleRouter()
router.register('profiles', CreateUpdateRetrieveProfile, basename='profiles')

urlpatterns = [] + router.urls
