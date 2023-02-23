from django.urls import path

from accounts.views import ActivateUser

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view(), name='activate-user'),
]
