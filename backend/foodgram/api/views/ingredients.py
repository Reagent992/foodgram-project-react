from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import FilterIngredientsSet
from api.serializers.api.ingredients import IngredientsSerializer
from recipes.models import Ingredients


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Ингредиенты."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterIngredientsSet
    pagination_class = None
    permission_classes = [AllowAny]
