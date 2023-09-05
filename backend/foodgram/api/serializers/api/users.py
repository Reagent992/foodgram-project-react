from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)
        # TODO: Проверить, это наверно уже не нужно.
        # extra_kwargs = {'email': {'required': True, 'allow_blank': False},
        #                 'username': {'required': True, 'allow_blank': False},
        #                 'first_name': {'required': True, 'allow_blank': False},
        #                 'last_name': {'required': True, 'allow_blank': False},
        #                 'password': {'required': True, 'allow_blank': False},
        #                 }


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        """
        Проверка подписан ли делающий запрос user на просматриваемого user.
        # FIXME: Количество запросов в БД равно количеству пользователей.
        """
        # -------------------------Просмотр запросов в БД----------------------
        # TODO: Удалить.
        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        print('--------------------------------------------------------------')
        # ---------------------------------------------------------------------
        requesting_user = self.context.get('request').user
        if not requesting_user.is_anonymous:
            return requesting_user.subscriptions.filter(
                target_user=obj.id).exists()
        return False
