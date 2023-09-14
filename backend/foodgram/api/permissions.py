from rest_framework.permissions import BasePermission, SAFE_METHODS


class RecipePermission(BasePermission):
    """
    Права доступа для рецептов:
    * Список рецептов, получение рецепта - доступно всем.
    * Создание - авторизованным пользователям.
    * Обновление и удаление - автору и админу.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and obj.author == request.user))
