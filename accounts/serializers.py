from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'role_id')
