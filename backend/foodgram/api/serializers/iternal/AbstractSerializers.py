from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer


class AbstractSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для Покупок и избранного."""

    class Meta:
        abstract = True

    def to_representation(self, instance):
        """Вывод данных другим сериализатором."""
        return HalfFieldsRecipeSerializer(instance.recipe).data

    def validate(self, data):
        """Валидация на повторное добавление."""
        user = data.get('user')
        recipe = data.get('recipe')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError(
                {'error': 'Вы уже добавили этот рецепт.'}
            )
        return data
