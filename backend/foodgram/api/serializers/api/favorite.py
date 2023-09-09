from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from recipes.models import FavoriteRecipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления в избранное."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = HalfFieldsRecipeSerializer(instance.recipe)
            return serializer.data
        return super().to_representation(instance)
