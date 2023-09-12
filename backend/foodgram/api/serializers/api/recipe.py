from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.serializers.api.tags import TagSerializer
from api.serializers.api.users import CustomUserSerializer
from api.serializers.nested.recipe import (HalfIngredientsSerializer,
                                           RecipeIngredientsSerializer)
from recipes.models import Recipe, RecipeIngredients, Tag


def create_ingredients(ingredients, recipe):
    recipe_ingredients_to_create = []
    for ingredient in ingredients:
        amount = ingredient.pop('amount', False)
        new_ingredient = ingredient.pop('id', False)
        if amount and new_ingredient:
            recipe_ingredients_to_create.append(
                RecipeIngredients(
                    recipe=recipe,
                    ingredient=new_ingredient,
                    amount=amount
                ))
    RecipeIngredients.objects.bulk_create(recipe_ingredients_to_create)


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'author', 'image', 'is_favorited',
                  'is_in_shopping_cart',)

    def get_is_favorited(self, recipe):
        """Проверка добавил ли автор рецепт в избранное."""

        requesting_user = self.context.get('request').user
        return requesting_user.is_authenticated and recipe.is_fav

    def get_is_in_shopping_cart(self, recipe):
        """Проверка добавлен ли рецепт в корзину."""

        requesting_user = self.context.get('request').user
        return requesting_user.is_authenticated and recipe.in_cart


class RecipeCreateEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования и создания рецептов."""

    image = Base64ImageField(required=True)
    # TODO: с id ингредиентов ошибка(
    #  добавляются правильные, а выводятся другие id,
    #  из таблицы Recipeingredients)
    ingredients = HalfIngredientsSerializer(
        source='recipeingredients', many=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text',
                  'ingredients', 'image',
                  'tags', 'author')

    def validate_tags(self, tags):
        """Провера тегов на наличие и уникальность."""

        if not tags:
            raise serializers.ValidationError(
                "Список тегов не может быть пустым.")
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError("Теги должны быть уникальными.")
        return tags

    def validate_ingredients(self, ingredients):
        """Проверка ингредиентов на наличие и уникальность."""

        if not ingredients:
            raise serializers.ValidationError(
                "Список ингредиентов не может быть пустым.")

        unique_ingredients = set()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if ingredient_id in unique_ingredients:
                raise serializers.ValidationError(
                    "Список ингредиентов не может содержать дубликаты.")
            unique_ingredients.add(ingredient_id)
        return ingredients

    def validate_image(self, image):
        """Проверка на наличие картинки."""

        if not image:
            raise serializers.ValidationError(
                "Нельзя отправиль рецепт без картинки.")
        return image

    @atomic
    def create(self, validated_data):
        """Запись ингредиентов и тегов в рецепт."""
        ingredients = validated_data.pop('recipeingredients', False)
        tags = validated_data.pop('tags', False)
        recipe = Recipe.objects.create(**validated_data)
        create_ingredients(ingredients=ingredients, recipe=recipe)
        recipe.tags.set(tags)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        """Изменение рецепта."""

        new_ingredients = validated_data.pop('recipeingredients', False)
        new_tags = validated_data.pop('tags', False)
        instance.ingredients.clear()
        instance.tags.clear()
        create_ingredients(recipe=instance, ingredients=new_ingredients)
        instance.tags.set(new_tags)
        super().update(instance, validated_data)
        return instance

    # def to_representation(self, instance):
    #     self.context
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return RecipeListRetriveSerializer(instance, context=context).data
