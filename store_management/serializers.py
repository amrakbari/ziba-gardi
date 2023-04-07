from rest_framework import serializers

from store_management.models import UserProfile


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
