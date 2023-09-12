from rest_framework import serializers

from recipes.models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredients
        fields = '__all__'
