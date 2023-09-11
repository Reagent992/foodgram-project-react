from api.serializers.nested.recipe import HalfFieldsRecipeSerializer
from rest_framework import serializers


class AbstracsSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для Покупок и избранного."""

    class Meta:
        abstract = True

    def to_representation(self, instance):
        serializer = HalfFieldsRecipeSerializer(instance.recipe)
        return serializer.data
