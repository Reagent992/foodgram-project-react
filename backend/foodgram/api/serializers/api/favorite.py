from rest_framework.validators import UniqueTogetherValidator

from api.serializers.iternal.AbstractSerializers import AbstractSerializer
from recipes.models import FavoriteRecipe


class FavoriteRecipeSerializer(AbstractSerializer):
    """Добавление в избранное."""

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='Уже добавлено в избранное'
            )
        ]
