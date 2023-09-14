from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers.api.tags import TagSerializer
from recipes.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
