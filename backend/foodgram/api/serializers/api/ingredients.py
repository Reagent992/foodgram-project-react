from recipes.models import Ingredients
from rest_framework import serializers


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit.name')

    class Meta:
        model = Ingredients
        fields = '__all__'
