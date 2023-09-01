from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from api.serializers.api.users import CustomUserSerializer
from recipes.models import Subscription


class SubscriptionResponseSerializer(serializers.Serializer):
    """Вывод списка подписок."""
    email = serializers.EmailField(source='target_user.email')
    id = serializers.IntegerField(source='target_user.id')
    username = serializers.CharField(source='target_user.username')
    first_name = serializers.CharField(source='target_user.first_name')
    last_name = serializers.CharField(source='target_user.last_name')
    is_subscribed = serializers.BooleanField(source='target_user')
    recipes = HalfFieldsRecipeSerializer(source='target_user.recipe.all',
                                         many=True)
    recipes_count = serializers.IntegerField(source='target_user.recipe.count')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Создание и удалеине подписок."""
    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('subscriber', 'target_user')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('subscriber', 'target_user'),
                message='Вы уже подписались на этого пользователя.'
            )
        ]

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = CustomUserSerializer(
                instance.target_user, context=self.context)
            return serializer.data
        return super().to_representation(instance)
