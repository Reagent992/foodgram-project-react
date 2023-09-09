from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from users.models import Subscription


class SubscriptionResponseSerializer(serializers.Serializer):
    """Вывод списка подписок."""

    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.BooleanField(source='author')
    recipes = HalfFieldsRecipeSerializer(source='author.recipe.all',
                                         many=True)
    recipes_count = serializers.IntegerField(source='author.recipe.count')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Создание и удаление подписок."""

    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

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
        if self.context['request'].method == 'POST':
            serializer = SubscriptionResponseSerializer(
                instance, context=self.context)
            return serializer.data
        return super().to_representation(instance)
