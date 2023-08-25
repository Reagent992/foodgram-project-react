from django_filters import ModelMultipleChoiceFilter, ModelChoiceFilter, \
    CharFilter
from django_filters.rest_framework import FilterSet

from recipes.models import Recipe, Tag, Ingredients


class FilterRecipeSet(FilterSet):
    # Это как работает вообще? mind-break...
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ['author']


class FilterIngredientsSet(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredients
        fields = {'name'}
