from api.permissions import TagsPermission
from api.serializers.api.tags import TagSerializer
from recipes.models import Tag
from rest_framework.viewsets import ReadOnlyModelViewSet


class TagViewSet(ReadOnlyModelViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (TagsPermission,)
    pagination_class = None
