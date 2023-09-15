from django_filters import AllValuesMultipleFilter
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet)

from recipes.models import Ingredients, Recipe


class FilterRecipeSet(FilterSet):
    is_favorited = BooleanFilter(field_name='is_fav')
    is_in_shopping_cart = BooleanFilter(field_name='in_cart')
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ('author',)


class FilterIngredientsSet(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredients
        fields = ['name']
