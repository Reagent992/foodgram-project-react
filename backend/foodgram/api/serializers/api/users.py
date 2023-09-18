from rest_framework import serializers

from users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, author):
        """
        Проверка подписан ли делающий запрос пользователь
        на просматриваемого пользователя.
        """
        requesting_user = self.context.get('request').user
        return (requesting_user.is_authenticated
                and requesting_user.subscriptions.filter(
                    author=author).exists())
