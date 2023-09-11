from api.serializers.iternal.AbstractSerializers import AbstracsSerializer
from recipes.models import FavoriteRecipe
from rest_framework.validators import UniqueTogetherValidator


class FavoriteRecipeSerializer(AbstracsSerializer):
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
