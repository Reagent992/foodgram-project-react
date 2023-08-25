from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import FilterRecipeSet, FilterIngredientsSet
from api.permissions import TagsPermission
from api.serializers import (RecipeSerializer, TagSerializer, UserSerializer,
                             RecipeCreateEditSerializer,
                             IngredientsSerializer)
from api.viewsets_templates import CreateDestroyViewSet
from recipes.models import Recipe, Tag, Ingredients

User = get_user_model()


class FavoriteViewSet(CreateDestroyViewSet):
    """Добавление и Удаление из избранного."""
    pass

    # serializer_class =

    def perform_create(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related(
        'recipeingredients__ingredient', 'tags'
    ).all()
    # serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterRecipeSet

    # TODO: Добавление в избранное.
    # TODO: Список покупок.

    def perform_create(self, serializer):
        """Добавлеине автора при создании рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбор серилизатора в зависимости от запроса."""
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
