from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.filters import FilterRecipeSet, FilterIngredientsSet
from api.permissions import TagsPermission
from api.serializers.api.favorite import FavoriteRecipeSerializer
from api.serializers.api.ingredients import IngredientsSerializer
from api.serializers.api.recipe import (RecipeListRetriveSerializer,
                                        RecipeCreateEditSerializer)
from api.serializers.api.shopping_cart import ShoppingCartSerializer
from api.serializers.api.subscriptions import (SubscriptionResponseSerializer,
                                               SubscriptionSerializer)
from api.serializers.api.tags import TagSerializer
from api.viewsets_templates import (CreateDestroyViewSet,
                                    ListCreateDestroyViewSet)
from recipes.models import (Recipe, Tag, Ingredients, FavoriteRecipe,
                            ShoppingCart)
from users.models import Subscription


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Список покупок."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def create(self, request, *args, **kwargs):
        recipe = self.kwargs.get('recipe_id')
        request.data['recipe'] = recipe
        return super().create(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def delete(self, request, recipe_id):
        user = self.request.user
        instance = get_object_or_404(
            ShoppingCart, user=user, recipe=recipe_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateDestoySubscriptionViewSet(ListCreateDestroyViewSet):
    """Подписки."""

    def get_queryset(self):
        queryset = self.request.user.subscriptions.select_related(
            'target_user').all()
        return queryset.prefetch_related('target_user__recipe')

    def get_serializer_class(self):
        if self.action == 'list':
            return SubscriptionResponseSerializer
        return SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        recipe = self.kwargs.get('target_user')
        request.data['target_user'] = recipe
        return super().create(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def delete(self, request, target_user):
        user = self.request.user
        instance = get_object_or_404(
            Subscription, subscriber=user, target_user=target_user)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res


class FavoriteViewSet(CreateDestroyViewSet):
    """Добавление и Удаление из избранного."""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        recipe = self.kwargs.get('recipe_id')
        request.data['recipe'] = recipe
        return super().create(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def delete(self, request, recipe_id):
        user = self.request.user
        instance = get_object_or_404(
            FavoriteRecipe, user_id=user, recipe_id=recipe_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.prefetch_related(
        'recipeingredients__ingredient', 'tags',
        'recipeingredients__ingredient__measurement_unit',
    ).select_related(
        'author',
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterRecipeSet
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticatedOrReadOnly]  # TODO: написать свой.

    def perform_create(self, serializer):
        """Добавление автора при создании рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action in ['list', 'retrieve']:
            return RecipeListRetriveSerializer
        else:
            return RecipeCreateEditSerializer

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в виде txt-файла."""
        if request.method == 'GET':
            user = request.user
            queryset = ShoppingCart.objects.filter(user=user).prefetch_related(
                'recipe__recipeingredients__ingredient',
                'recipe__recipeingredients__ingredient__measurement_unit'
            )
            # Словарь ингредиент: количество
            ingredients = dict()
            for shopping_cart_obj in queryset:
                for item in shopping_cart_obj.recipe.recipeingredients.all():
                    if ingredients.get(item.ingredient.name):
                        ingredients[item.ingredient] += item.amount
                    else:
                        ingredients[item.ingredient] = item.amount
            # Список Ингредиент - количество - единица измерения.
            formatted_ingredients = [
                f'{key.name} - {value}{key.measurement_unit.name}' for
                key, value
                in
                ingredients.items()]

            return HttpResponse('\n'.join(formatted_ingredients),
                                content_type='text/plain')

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagsPermission]
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингредиенты."""
    queryset = Ingredients.objects.prefetch_related('measurement_unit').all()
    serializer_class = IngredientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterIngredientsSet
    pagination_class = None
