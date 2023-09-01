from django.db.transaction import atomic
from rest_framework import serializers

from api.serializers.nested.base64 import Base64ImageFieldSerializer
from api.serializers.nested.recipe import RecipeIngredientsSerializer
from api.serializers.api.tags import TagSerializer
from api.serializers.api.users import CustomUserSerializer
from recipes.models import Recipe, Ingredients, RecipeIngredients


class RecipeListRetriveSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    author = CustomUserSerializer()

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
    # TODO: не работает поле ingredients
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'image',)

    def get_ingredients(self):
        """Получение ингредиентов для рецепта."""
        # TODO: !
        print(self)
        print(self.data)
        print(self.ingredients)
        # Ingredients.objects.get(id=)

    @atomic
    def create(self, validated_data):
        """Запись ингредиентов и тегов в рецепт."""
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            print(ingredient)
            amount = ingredient.pop('amount')
            pk = ingredient.pop('ingredient')
            print(pk, amount)
            current_ingredient, status = Ingredients.objects.get_or_create(
                pk=pk
            )
            RecipeIngredients.objects.create(
                recipe=recipe, ingredient=current_ingredient, amount=amount
            )

        for tag in tags:
            print(tag)

        return recipe
