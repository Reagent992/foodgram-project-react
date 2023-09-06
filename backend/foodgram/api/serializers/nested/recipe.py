from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredients, Ingredients


class HalfFieldsRecipeSerializer(serializers.ModelSerializer):
    """Вывод нескольких полей рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов с дополнительными полями."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class HalfIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для записи рецепта."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')
