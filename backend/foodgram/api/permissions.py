from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class TagsPermission(BasePermission):
    """
    Права доступа для Тегов:
    * SAFE_METHODS разрешены.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True


class RecipePermission(BasePermission):
    """
    Права доступа для рецептов:
    * Список рецептов, получение рецепта - доступно всем.
    * Создание - авторизованным пользователям.
    * Обновление и удалеине - автору и админу.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_superuser or request.user.is_staff))
