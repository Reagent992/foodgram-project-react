from django.conf import settings
from rest_framework import serializers

from recipes.models import Ingredients, Recipe, RecipeIngredients


class HalfFieldsRecipeSerializer(serializers.ModelSerializer):
    """Вывод нескольких полей рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов для просмотра рецептов с дополнительными полями.
    """

    id = serializers.ReadOnlyField(source='ingredient.pk')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class WriteRecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для записи ингредиентов в рецепт."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField(min_value=settings.MIN_VALUE,
                                      max_value=settings.MAX_AMOUNT)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')
