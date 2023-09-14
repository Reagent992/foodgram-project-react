from rest_framework import serializers

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer


class AbstractSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для Покупок и избранного."""

    class Meta:
        abstract = True

    def to_representation(self, instance):
        serializer = HalfFieldsRecipeSerializer(instance.recipe)
        return serializer.data
