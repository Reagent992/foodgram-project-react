from api.serializers.iternal.AbstractSerializers import AbstractSerializer
from recipes.models import FavoriteRecipe


class FavoriteRecipeSerializer(AbstractSerializer):
    """Добавление в избранное."""

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
