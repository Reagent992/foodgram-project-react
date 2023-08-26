from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.filters import FilterRecipeSet, FilterIngredientsSet
from api.permissions import TagsPermission
from api.serializers import (RecipeSerializer, TagSerializer, UserSerializer,
                             RecipeCreateEditSerializer,
                             IngredientsSerializer, FavoriteRecipeSerializer)
from api.viewsets_templates import CreateDestroyViewSet
from recipes.models import Recipe, Tag, Ingredients, FavoriteRecipe

User = get_user_model()


# TODO: Список покупок.

class FavoriteViewSet(CreateDestroyViewSet):
    """Добавление и Удаление из избранного."""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        recipe = self.kwargs.get('recipe_id')
        request.data['recipe'] = recipe
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Возвращается только словарь response
        return Response(serializer.data.pop('response'),
                        status=status.HTTP_201_CREATED, headers=headers)

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
        'recipeingredients__ingredient', 'tags'
    ).all()
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


class UserViewSetCustom(UserViewSet):
    """Добавление полей в Djoser-UserViewSet."""
    queryset = User.objects.prefetch_related(
        # TODO: Я не знаю как оптимизировать запрос тут.
    ).all()
    serializer_class = UserSerializer

    # TODO: Сделать подписки

    @action(detail=False, methods=['GET'], )
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

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
    # TODO: Без AllowAny редактирование рецепта на фронте не работает
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
