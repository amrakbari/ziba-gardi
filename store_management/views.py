from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from store_management.models import UserProfile, Store, Appointment
from store_management.serializers import UserProfileSerializer, StoreSerializer, AppointmentSerializer


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


class CreateRetrieveListUpdateDestroyStore(mixins.CreateModelMixin,
                                           mixins.RetrieveModelMixin,
                                           mixins.ListModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.DestroyModelMixin,
                                           viewsets.GenericViewSet):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        current_user_profile = UserProfile.objects.get(user_id=self.request.user.id)
        return Store.objects.filter(stylist=current_user_profile)

    def perform_create(self, serializer):
        current_user_profile = UserProfile.objects.get(user_id=self.request.user.id)
        serializer.validated_data['stylist'] = current_user_profile
        serializer.save()
        print('a')

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.utcnow()
        instance.save()


class CreateRetrieveListDestroyUpdateAppointment(mixins.CreateModelMixin,
                                                 mixins.RetrieveModelMixin,
                                                 mixins.ListModelMixin,
                                                 mixins.DestroyModelMixin,
                                                 mixins.UpdateModelMixin,
                                                 viewsets.GenericViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # TODO add is_stylist permission
    queryset = Appointment.objects.all()


