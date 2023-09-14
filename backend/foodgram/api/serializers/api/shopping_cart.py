from rest_framework.validators import UniqueTogetherValidator

from api.serializers.iternal.AbstractSerializers import AbstractSerializer
from recipes.models import ShoppingCart


class ShoppingCartSerializer(AbstractSerializer):
    """Добавление в Список покупок."""

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
