from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from store_management.models import UserProfile
from store_management.serializers import UserProfileSerializer


class CreateUpdateRetrieveProfile(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_current_user_profile(self, request):
        instance = get_object_or_404(self.get_queryset())
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        methods=['PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def update_current_user_profile(self, request):
        profile = get_object_or_404(self.get_queryset())
        serializer = self.get_serializer(data=request.data, instance=profile, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
