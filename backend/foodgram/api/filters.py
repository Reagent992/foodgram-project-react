from django_filters import AllValuesMultipleFilter
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet)

from recipes.models import Ingredients, Recipe


class FilterRecipeSet(FilterSet):
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ('author',)

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                favoriterecipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                shoppingcart__user=self.request.user)
        return queryset


class FilterIngredientsSet(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredients
        fields = ['name']
