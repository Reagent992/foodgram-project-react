from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from api.serializers.api.tags import TagSerializer
from api.serializers.api.users import CustomUserSerializer
from api.serializers.nested.base64 import Base64ImageFieldSerializer
from api.serializers.nested.recipe import (RecipeIngredientsSerializer,
                                           )
from recipes.models import Recipe, RecipeIngredients

User = get_user_model()


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'author', 'image',
                  "is_favorited", "is_in_shopping_cart",)

    def get_is_favorited(self, obj):
        """Проверка добавил ли автор этот рецепт в избранное."""
        requesting_user = self.context.get('request').user
        return requesting_user.favorite_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка добавлен ли рецепт в корзину."""
        requesting_user = self.context.get('request').user
        return requesting_user.shopping_cart.filter(recipe=obj).exists()


class RecipeCreateEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования и создания рецептов."""
    image = Base64ImageFieldSerializer(required=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text',
                  'ingredients', 'image',
                  'tags',)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient.pop('amount', False)
            new_ingredient = ingredient.pop('id', False)
            if amount and new_ingredient:
                RecipeIngredients.objects.create(
                    recipe=recipe,
                    ingredient=new_ingredient,
                    amount=amount
                )

    @atomic
    def create(self, validated_data):
        """Запись ингредиентов и тегов в рецепт."""
        ingredients = validated_data.pop('recipeingredients', False)
        tags = validated_data.pop('tags', False)
        recipe = Recipe.objects.create(**validated_data)
        if ingredients:
            self.create_ingredients(ingredients=ingredients,
                                    recipe=recipe)

        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance: Recipe, validated_data):
        """Изменение рецепта."""
        instance.name = validated_data.pop('name', instance.name)
        instance.image = validated_data.pop('image', instance.image)
        instance.cooking_time = validated_data.pop(
            'cooking_time', instance.cooking_time)
        instance.text = validated_data.pop('text', instance.text)

        new_ingredients = validated_data.pop(
            'recipeingredients', False)
        new_tags = validated_data.pop('tags', False)
        instance.ingredients.clear()
        instance.tags.clear()
        if new_ingredients:
            self.create_ingredients(
                recipe=instance,
                ingredients=new_ingredients)
        if new_tags:
            instance.tags.set(new_tags)
        instance.save()

        return instance
