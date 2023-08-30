from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.filters import FilterRecipeSet, FilterIngredientsSet
from api.permissions import TagsPermission
from api.serializers import (RecipeSerializer, TagSerializer,
                             RecipeCreateEditSerializer,
                             IngredientsSerializer, FavoriteRecipeSerializer,
                             SubscriptionSerializer,
                             SubscriptionResponseSerializer,
                             ShoppingCartSerializer)
from api.viewsets_templates import (CreateDestroyViewSet,
                                    ListCreateDestroyViewSet)
from recipes.models import (Recipe, Tag, Ingredients, FavoriteRecipe,
                            Subscription, ShoppingCart)

User = get_user_model()


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
        # TODO: Удалить dispatch.
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

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch.
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""
    queryset = Recipe.objects.prefetch_related(
        'recipeingredients__ingredient', 'tags'
    ).all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # TODO: Фильтрация избранного.
    filterset_class = FilterRecipeSet

    def perform_create(self, serializer):
        """Добавление автора при создании рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        else:
            return RecipeCreateEditSerializer

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch.
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res


class TagViewSet(viewsets.ModelViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagsPermission]
    pagination_class = None

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch.
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингредиенты."""
    queryset = Ingredients.objects.prefetch_related('measurement_unit').all()
    serializer_class = IngredientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterIngredientsSet
    # TODO: Без AllowAny редактирование ингредиента на фронте не работает.
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def dispatch(self, request, *args, **kwargs):
        # TODO: Удалить dispatch.
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print('Количество запросов в БД:', len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])
        return res
