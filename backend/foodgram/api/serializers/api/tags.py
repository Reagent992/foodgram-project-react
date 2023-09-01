from colorfield.serializers import ColorField
from rest_framework import serializers

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    color = ColorField()

    class Meta:
        model = Tag
        fields = '__all__'
