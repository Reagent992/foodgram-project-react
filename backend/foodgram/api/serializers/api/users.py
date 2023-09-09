from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, author):
        """
        Проверка подписан ли делающий запрос user на просматриваемого user.
        """

        requesting_user = self.context.get('request').user
        if not requesting_user.is_anonymous:
            subscriptions = self.context.get('subscriptions')
            if subscriptions:
                return any(
                    sub.author == author for sub in subscriptions)
            else:
                return requesting_user.author.filter(
                    author=author.id).exists()
        return False
