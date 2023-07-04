from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser
from store_management.models import UserProfile, Store, Appointment


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'role',
            'birth_date',
            'created_at',
        )
        extra_kwargs = {'created_at': {'read_only': True}}


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
    class Meta:
        model = Appointment
        fields = (
            'id',
            'store',
            'service',
            'start_datetime',
            'end_datetime',
        )
