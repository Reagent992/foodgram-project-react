from api.serializers.iternal.AbstractSerializers import AbstracsSerializer
from recipes.models import ShoppingCart
from rest_framework.validators import UniqueTogetherValidator


class ShoppingCartSerializer(AbstracsSerializer):
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
