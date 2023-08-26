import base64

from colorfield.serializers import ColorField
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Recipe, Tag, RecipeIngredients, Ingredients,
                            FavoriteRecipe)

User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit.name')

    class Meta:
        model = Ingredients
        fields = '__all__'


class Base64ImageFieldSerializer(serializers.ImageField):
    """Декодирование Base64 картинки."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    color = ColorField()

    # TODO: Сделать валидацию цвета, из сериализатором из библиотеки.
    # TODO: Валидация по unique slug
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        """
        Проверка подписан ли делающий запрос user на просматриваемого user.
        """
        # FIXME: Возможно это надо делать в viewset для оптимизации запроса в БД.
        requesting_user = self.context.get('request').user
        return requesting_user.subscriptions.filter(
            target_user=obj.id).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    # TODO: Подставлять автора при создании рецепта.
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'author', 'image',
                  # TODO: "is_favorited",
                  # TODO: "is_in_shopping_cart",
                  )


class RecipeCreateEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования и создания рецептов."""
    image = Base64ImageFieldSerializer(required=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )


class HalfFieldsRecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для вывода добавленного в избранное."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления в избранное."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    response = serializers.SerializerMethodField(method_name='get_response')

    def get_response(self, obj):
        serializer = HalfFieldsRecipeSerializer(obj.recipe)
        return serializer.data

    class Meta:
        model = FavoriteRecipe
        fields = (
            'user', 'recipe', 'response'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='Уже добавлено в избранное'
            )
        ]
