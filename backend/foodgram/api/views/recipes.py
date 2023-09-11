from api.filters import FilterRecipeSet
from api.permissions import RecipePermission
from api.serializers.api.favorite import FavoriteRecipeSerializer
from api.serializers.api.recipe import (RecipeCreateEditSerializer,
                                        RecipeListRetriveSerializer)
from api.serializers.api.shopping_cart import ShoppingCartSerializer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import FavoriteRecipe, Recipe, ShoppingCart
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def create_obj(serializer, request, pk):
    """Добавление в список покупок и избранное."""

    data = {
        'user': request.user.pk,
        'recipe': pk,
    }
    serializer_instance = serializer(data=data)

    if serializer_instance.is_valid():
        serializer_instance.save()
        return Response(serializer_instance.data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer_instance.errors,
                    status=status.HTTP_400_BAD_REQUEST)


def delete_obj(model, request, pk):
    user = request.user
    try:
        instance = model.objects.get(user=user, recipe=pk)
    except model.DoesNotExist:
        return Response({'errors': 'Этой записи не существует'},
                        status=status.HTTP_400_BAD_REQUEST)

    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(viewsets.ModelViewSet):
    """Рецепты."""

    queryset = Recipe.objects.prefetch_related(
        'recipeingredients__ingredient', 'tags',
    ).select_related(
        'author',
    ).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterRecipeSet
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = (RecipePermission,)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action in ['list', 'retrieve']:
            return RecipeListRetriveSerializer
        return RecipeCreateEditSerializer

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Добавление в список покупок."""

        return create_obj(ShoppingCartSerializer, request, pk)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        """Удаление из списка покупок."""

        return delete_obj(ShoppingCart, request, pk)

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        """Добавление в избранное."""

        return create_obj(FavoriteRecipeSerializer, request, pk)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        """Удаление из избранного."""

        return delete_obj(FavoriteRecipe, request, pk)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Загрузка списка покупок в виде txt-файла."""

        user = request.user
        if request.method == 'GET':
            queryset = ShoppingCart.objects.filter(user=user).prefetch_related(
                'recipe__recipeingredients__ingredient',
                'recipe__recipeingredients__ingredient__measurement_unit'
            )
            # Словарь {ингредиент: количество}.
            ingredients = dict()
            for shopping_cart_obj in queryset:
                for item in shopping_cart_obj.recipe.recipeingredients.all():
                    if ingredients.get(item.ingredient):
                        ingredients[item.ingredient] += item.amount
                    else:
                        ingredients[item.ingredient] = item.amount
            # Список [Ингредиент - количество - единица измерения].
            formatted_ingredients = [
                f'{ingredient.name} - '
                f'{amount}{ingredient.measurement_unit.name}'
                for
                ingredient, amount in ingredients.items()]

            return HttpResponse('\n'.join(formatted_ingredients),
                                content_type='text/plain')
