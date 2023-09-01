from rest_framework import serializers

from recipes.models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit.name')

    class Meta:
        model = Ingredients
        fields = '__all__'
