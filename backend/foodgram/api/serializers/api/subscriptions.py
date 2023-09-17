from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.api.users import CustomUserSerializer
from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from users.models import Subscription


class SubscriptionResponseSerializer(CustomUserSerializer):
    """Вывод списка подписок."""

    recipes_count = serializers.IntegerField(source='recipe.count')
    recipes = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes', 'recipes_count')

    def get_recipes(self, user):
        """
        Список рецептов, с заданным ограничением на количество рецептов.
        """

        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = user.recipe.all()
        if limit and limit.isdigit():
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass

        return HalfFieldsRecipeSerializer(queryset, many=True).data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Создание и удаление подписок."""

    class Meta:
        model = Subscription
        fields = ('subscriber', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('subscriber', 'author'),
                message='Вы уже подписались на этого пользователя.'
            )
        ]

    def validate(self, data):
        if data['subscriber'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя.'
            )
        return data

    def to_representation(self, instance):
        return SubscriptionResponseSerializer(
            instance.author, context=self.context).data
