from api.filters import FilterIngredientsSet
from api.serializers.api.ingredients import IngredientsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredients
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Ингредиенты."""
    queryset = Ingredients.objects.prefetch_related('measurement_unit').all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterIngredientsSet
    pagination_class = None
    permission_classes = [AllowAny]
