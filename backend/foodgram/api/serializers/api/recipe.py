from django.conf import settings
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.serializers.api.tags import TagSerializer
from api.serializers.api.users import CustomUserSerializer
from api.serializers.nested.recipe import (RecipeIngredientsSerializer,
                                           WriteRecipeIngredientsSerializer)
from recipes.models import Recipe, RecipeIngredients, Tag


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    author = CustomUserSerializer()
    is_in_shopping_cart = serializers.BooleanField(default=0)
    is_favorited = serializers.BooleanField(default=0)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'author', 'image',
                  'is_favorited', 'is_in_shopping_cart')


class RecipeCreateEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования и создания рецептов."""

    image = Base64ImageField(required=True)
    ingredients = WriteRecipeIngredientsSerializer(many=True)
    cooking_time = serializers.IntegerField(
        min_value=settings.MIN_VALUE,
        max_value=settings.MAX_COOKING_TIME
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text',
                  'ingredients', 'image',
                  'tags', 'author')
        read_only_fields = ('author',)

    def validate_tags(self, tags):
        """Провера тегов на наличие и уникальность."""
        if not tags:
            raise serializers.ValidationError(
                {'error': 'Список тегов не может быть пустым.'})
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                {'error': 'Теги должны быть уникальными.'})
        return tags

    def validate(self, attrs):
        """Проверка ингредиентов на наличие и уникальность."""
        ingredients = attrs.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'error': 'Список ингредиентов не может быть пустым.'})

        ingredients_length = [
            ingredient.get('id') for ingredient in ingredients
        ]
        if len(ingredients_length) != len(set(ingredients_length)):
            raise serializers.ValidationError(
                {'error': 'Список ингредиентов не может содержать дубликаты.'})

        return attrs

    def validate_image(self, image):
        """Проверка на наличие картинки."""
        if not image:
            raise serializers.ValidationError(
                {'error': 'Нельзя отправить рецепт без картинки.'})
        return image

    @staticmethod
    def create_ingredients(ingredients, recipe):
        """Добавление ингредиентов рецепта в промежуточную модель."""
        recipe_ingredients_to_create = [
            RecipeIngredients(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]

        return RecipeIngredients.objects.bulk_create(
            recipe_ingredients_to_create)

    @atomic
    def create(self, validated_data):
        """Запись ингредиентов и тегов в рецепт."""
        ingredients = validated_data.pop('ingredients', False)
        tags = validated_data.pop('tags', False)
        validated_data['author'] = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients=ingredients, recipe=recipe)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Изменение рецепта."""
        new_ingredients = validated_data.pop('ingredients', False)
        new_tags = validated_data.pop('tags', False)
        instance.ingredients.clear()
        instance.tags.clear()
        self.create_ingredients(recipe=instance, ingredients=new_ingredients)
        instance.tags.set(new_tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Отвечает сериализатор для чтения."""
        return RecipeListRetriveSerializer(instance=instance,
                                           context=self.context).data
