from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',)


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, target_user):
        """
        Проверка подписан ли делающий запрос user на просматриваемого user.
        """
        requesting_user = self.context.get('request').user
        if not requesting_user.is_anonymous:
            subscriptions = self.context.get('subscriptions')
            if subscriptions:
                return any(
                    sub.target_user == target_user for sub in subscriptions)
            else:
                return requesting_user.subscriptions.filter(
                    target_user=target_user.id).exists()
        return False

    def to_representation(self, instance):
        """Эндпоинт /api/users/me/ - пустой для анонимного пользователя."""
        path = self.context.get('request').path
        user = self.context.get('request').user
        if path == '/api/users/me/' and user.is_anonymous:
            return {}
        return super().to_representation(instance)
