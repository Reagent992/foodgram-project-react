from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from recipes.models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Добавление и удаление из Списка покупок."""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавили этот рецепт в список покупок.'
            )
        ]

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = HalfFieldsRecipeSerializer(
                instance.recipe, context=self.context)
            return serializer.data
        return super().to_representation(instance)
