from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import CustomUser, Address


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'title',
            'description',
            'longitude',
            'latitude',
        )
        extra_kwargs = {'id': {'read_only': True}, 'user': {'read_only': True}}
