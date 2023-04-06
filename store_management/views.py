from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from store_management.models import UserProfile
from store_management.serializers import UserProfileSerializer


class CreateUpdateRetrieveProfile(mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(UserProfile)
