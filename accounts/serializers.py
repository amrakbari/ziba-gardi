from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer

from accounts.models import CustomUser


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'role')

