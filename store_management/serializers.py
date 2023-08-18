from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser
from store_management.models import UserProfile, Store, Appointment, Service


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'role',
            'birth_date',
            'created_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
        }


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'id',
            'stylist',
            'title',
            'address',
            'created_at',
            'deleted_at',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'deleted_at': {'read_only': True},
            'stylist': {'read_only': True}
        }

    def validate(self, attrs):
        request = self.context.get('request')
        current_user = CustomUser.objects.get(pk=request.user.id)
        if not current_user.address_set.filter(pk=attrs['address'].id):
            raise ValidationError("address must be for the current user")
        return attrs


class AppointmentSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    end_datetime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Appointment
        fields = (
            'id',
            'store',
            'user',
            'service',
            'start_datetime',
            'end_datetime',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class GetAppointmentForUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Appointment
        fields = (
            'id',
            'user',
            'service',
            'store',
            'start_datetime',
            'end_datetime',
        )
        extra_kwargs = {
            'store': {'read_only': True},
            'user': {'read_only': True},
            'start_datetime': {'read_only': True},
            'end_datetime': {'read_only': True},
        }

    def save(self, **kwargs):
        request = self.context.get('request')
        appointment_id = self.validated_data['id']
        service = self.validated_data['service']
        user_id = request.user.id

        user = UserProfile.objects.get(user_id=user_id)

        appointment = Appointment.objects.filter(id=appointment_id).update(
            user=user,
            service=service
        )
        return appointment


class ListAppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Appointment
        fields = (
            'id',
            'store',
            'service',
            'start_datetime',
            'end_datetime',
            'date',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'date': {'write_only': True},
        }


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id',
            'title',
            'description',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class AddServiceToStoreSerializer(serializers.Serializer):
    store = serializers.IntegerField()
    service = serializers.IntegerField()

    def save(self, **kwargs):
        store = self.validated_data['store']
        service = self.validated_data['service']
        service = Service.objects.get(id=service)
        Store.objects.get(id=store).services.add(service)


class ProfileUserSerializer(serializers.ModelSerializer):
    profile = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'profile',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }