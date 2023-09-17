from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.nested.recipe import HalfFieldsRecipeSerializer


class AbstractSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для Покупок и избранного."""

    class Meta:
        abstract = True

    def to_representation(self, instance):
        return HalfFieldsRecipeSerializer(instance.recipe).data

    def validate(self, data):
        """Валидация на повторное добавление."""

        validator = UniqueTogetherValidator(
            queryset=self.Meta.model.objects.all(),
            fields=('user', 'recipe'),
            message='Вы уже добавили этот рецепт.'
        )
        serializer_instance = self.__class__(data=data)
        self.validators = validator(attrs=data, serializer=serializer_instance)

        return data
