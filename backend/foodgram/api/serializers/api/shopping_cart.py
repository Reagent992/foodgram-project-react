from api.serializers.iternal.AbstractSerializers import AbstractSerializer
from recipes.models import ShoppingCart


class ShoppingCartSerializer(AbstractSerializer):
    """Добавление в Список покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
