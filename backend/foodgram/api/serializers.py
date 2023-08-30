import base64

from colorfield.serializers import ColorField
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Recipe, Tag, RecipeIngredients, Ingredients,
                            FavoriteRecipe, Subscription, ShoppingCart)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    color = ColorField()

    class Meta:
        model = Tag
        fields = '__all__'


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


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)

        extra_kwargs = {'email': {'required': True, 'allow_blank': False},
                        'username': {'required': True, 'allow_blank': False},
                        'first_name': {'required': True, 'allow_blank': False},
                        'last_name': {'required': True, 'allow_blank': False},
                        'password': {'required': True, 'allow_blank': False},
                        }


class CustomUserSerializer(UserSerializer):
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
        # FIXME: Количество запросов в БД равно количеству пользователей.
        """
        # -------------------------Просмотр запросов в БД----------------------
        # TODO: Удалить.
        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        print('--------------------------------------------------------------')
        # ---------------------------------------------------------------------
        requesting_user = self.context.get('request').user
        return requesting_user.subscriptions.filter(
            target_user=obj.id).exists()


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
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
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients', many=True)
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tags', 'cooking_time', 'text',
                  'ingredients', 'author', 'image',
                  )


class HalfFieldsRecipeSerializer(serializers.ModelSerializer):
    """Вывод нескольких полей рецепта."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


# --------------------------------Избранное------------------------------------

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления в избранное."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='Уже добавлено в избранное'
            )
        ]

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = HalfFieldsRecipeSerializer(instance.recipe)
            return serializer.data
        return super().to_representation(instance)


# --------------------------------Подписки-------------------------------------

class SubscriptionResponseSerializer(serializers.Serializer):
    """Мои подписки."""
    email = serializers.EmailField(source='target_user.email')
    id = serializers.IntegerField(source='target_user.id')
    username = serializers.CharField(source='target_user.username')
    first_name = serializers.CharField(source='target_user.first_name')
    last_name = serializers.CharField(source='target_user.last_name')
    is_subscribed = serializers.BooleanField(source='target_user')
    recipes = HalfFieldsRecipeSerializer(source='target_user.recipe.all',
                                         many=True)
    recipes_count = serializers.IntegerField(source='target_user.recipe.count')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Создание и удалеине подписок."""
    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('subscriber', 'target_user')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('subscriber', 'target_user'),
                message='Вы уже подписались на этого пользователя.'
            )
        ]

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = CustomUserSerializer(
                instance.target_user, context=self.context)
            return serializer.data
        return super().to_representation(instance)


# --------------------------Список покупок-------------------------------------

class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавили этот рецепт в список покупок.'
            )
        ]

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            serializer = HalfFieldsRecipeSerializer(
                instance.recipe, context=self.context)
            return serializer.data
        return super().to_representation(instance)
