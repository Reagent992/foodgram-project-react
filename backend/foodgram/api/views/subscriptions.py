from djoser.views import UserViewSet as UserViewSetDjoser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.serializers.api.subscriptions import (SubscriptionResponseSerializer,
                                               SubscriptionSerializer)
from users.models import Subscription


class UserViewSet(UserViewSetDjoser):
    """Пользователи."""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Доступ к users/me только у авторизованого пользователя."""

        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(methods=('get',), detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Отображение списка подписок."""

        queryset = request.user.subscription.all().prefetch_related('recipe')
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionResponseSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=('post',), detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        """Подписка на пользователя."""
        data = {
            'subscriber': request.user.id,
            'author': id,
        }
        serializer = SubscriptionSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """Отписаться от пользователя."""

        user = request.user
        try:
            instance = Subscription.objects.get(subscriber=user, author=id)
        except Subscription.DoesNotExist:
            return Response({'errors': 'Этой записи не существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
