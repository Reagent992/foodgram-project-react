from api.mixins.mixins import ListCreateDestroyViewSet
from api.serializers.api.subscriptions import (SubscriptionResponseSerializer,
                                               SubscriptionSerializer)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import Subscription


class ListCreateDestoySubscriptionViewSet(ListCreateDestroyViewSet):
    """Подписки."""

    def get_queryset(self):
        return self.request.user.subscriptions.select_related(
            'author').prefetch_related('author__recipe').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SubscriptionResponseSerializer
        return SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        recipe = self.kwargs.get('author')
        request.data['author'] = recipe
        return super().create(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def delete(self, request, author):
        user = self.request.user
        instance = get_object_or_404(
            Subscription, subscriber=user, author=author)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
