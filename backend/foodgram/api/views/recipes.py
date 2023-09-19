from django.db.models import Exists, OuterRef, Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import FilterRecipeSet
from api.permissions import RecipePermission
from api.serializers.api.favorite import FavoriteRecipeSerializer
from api.serializers.api.recipe import (RecipeCreateEditSerializer,
                                        RecipeListRetriveSerializer)
from api.serializers.api.shopping_cart import ShoppingCartSerializer
from recipes.models import (FavoriteRecipe, Recipe, RecipeIngredients,
                            ShoppingCart)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterRecipeSet
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = (RecipePermission,)

    def get_queryset(self):
        """Получение queryset и оптимизация запроса в БД."""
        user = self.request.user
        queryset = Recipe.objects.prefetch_related(
            'recipeingredients', 'tags',
        ).select_related(
            'author'
        ).all()
        if user.is_authenticated:
            return queryset.annotate(
                is_favorited=Exists(user.favoriterecipe.filter(
                    recipe=OuterRef('pk'))),
                is_in_shopping_cart=Exists(user.shoppingcart.filter(
                    recipe=OuterRef('pk'))),
            )
        return queryset

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action in ['list', 'retrieve']:
            return RecipeListRetriveSerializer
        return RecipeCreateEditSerializer

    @staticmethod
    def ingredients_to_text(queryset):
        """Вывод ингредиентов."""
        return '\n'.join([
            '{} {}{}'.format(
                row.get('ingredient__name'),
                row.get('total_amount'),
                row.get('ingredient__measurement_unit')
            )
            for row in queryset])

    @staticmethod
    def create_obj(serializer, request, pk):
        """Добавление в список покупок и избранное."""
        data = {
            'user': request.user.pk,
            'recipe': pk,
        }
        serializer_instance = serializer(data=data,
                                         context={'request': request})
        serializer_instance.is_valid(raise_exception=True)
        serializer_instance.save()
        return Response(serializer_instance.data,
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_obj(model, request, pk):
        """Удаление из покупок и избранного."""
        user = request.user
        instance = model.objects.filter(user=user, recipe=pk)
        if instance.exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Этой записи не существует'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Добавление в список покупок."""
        return self.create_obj(ShoppingCartSerializer, request, pk)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        """Удаление из списка покупок."""
        return self.delete_obj(ShoppingCart, request, pk)

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        """Добавление в избранное."""
        return self.create_obj(FavoriteRecipeSerializer, request, pk)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        """Удаление из избранного."""
        return self.delete_obj(FavoriteRecipe, request, pk)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в виде txt-файла."""
        user = request.user
        ingredients = RecipeIngredients.objects.filter(
            recipe__shoppingcart__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(total_amount=Sum('amount'))

        return FileResponse(self.ingredients_to_text(ingredients),
                            content_type='text/plain',
                            filename='shopping-list.txt')
