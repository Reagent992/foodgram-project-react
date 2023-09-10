from colorfield.serializers import ColorField
from recipes.models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    color = ColorField()

    class Meta:
        model = Tag
        fields = '__all__'
