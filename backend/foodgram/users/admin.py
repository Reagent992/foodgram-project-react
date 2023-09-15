from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.models import Subscription, User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Пользователь."""

    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'last_login', 'subscribers', 'recipes')
    search_fields = ('email', 'username')

    @admin.display(description='Подписчиков')
    def subscribers(self, user):
        """Количество подписчиков."""

        return user.author.count()

    @admin.display(description='Рецептов')
    def recipes(self, user):
        """Количество рецептов."""

        return user.recipe.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Подписки."""

    list_display = ('subscriber', 'author', 'created_at')
    search_fields = ('subscriber', 'author')
