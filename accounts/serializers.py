from datetime import datetime

from django.db import transaction
from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import CustomUser, Address
from store_management.models import UserProfile


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.CharField(write_only=True)
    birth_date = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'role', 'birth_date')

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        try:
            datetime.strptime(attrs['birth_date'], "%m/%d/%Y")
        except ValueError:
            raise serializers.ValidationError("invalid date format")
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")

    def create(self, validated_data):
        with transaction.atomic():
            user = CustomUser.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
            user.set_password(validated_data['password'])
            user.save()
            birth_date = datetime.strptime(validated_data['birth_date'], "%m/%d/%Y")
            profile = UserProfile.objects.create(
                user=user,
                role=validated_data['role'],
                birth_date=birth_date,
            )
            profile.save()
        return user


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
