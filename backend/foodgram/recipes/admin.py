from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.db.models import Count

from recipes.models import (Tag, Recipe, Ingredients, Subscription,
                            FavoriteRecipe, MeasurementUnit, ShoppingCart,
                            RecipeIngredients)

User = get_user_model()

admin.site.unregister(User)

admin.site.register(Subscription)
admin.site.register(FavoriteRecipe)
admin.site.register(MeasurementUnit)
admin.site.register(ShoppingCart)


def create_admin_group():
    """Создание группы admin при первом запуске."""
    methods = ('add', 'change', 'view', 'delete')
    models = ('user', 'recipe', 'ingredients', 'tag',)
    group, created = Group.objects.get_or_create(name='admin')
    if created:
        str_permissions_list = []
        for model in models:
            str_permissions_list.extend(
                [f'{method}_{model}' for method in methods])
        id_permissoin_list = [Permission.objects.get(codename=str(permission))
                              for
                              permission in str_permissions_list]
        [group.permissions.add(permission) for permission in
         id_permissoin_list]
        group.save()


create_admin_group()


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепт."""
    inlines = [RecipeIngredientsInline]
    readonly_fields = ('recipes_added_to_favorite_count',)
    list_display = (
        'name', 'author', 'recipes_added_to_favorite_count', 'pub_date')
    list_filter = 'author', 'name', 'tags'

    def recipes_added_to_favorite_count(self, obj):
        return obj.faved_recipies

    recipes_added_to_favorite_count.short_description = (
        'Количество добавлений в избранное')

    def get_queryset(self, request):
        """
        Попытка оптимизации запроса в БД.
        Кол-во запросов 7 * на кол-во рецептов.
        """
        queryset = Recipe.objects.annotate(
            faved_recipies=Count('recipes_added_to_favorite')
        )
        return queryset


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Пользователь."""
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'date_joined', 'last_login')

    list_filter = ('email', 'username')


@admin.register(Ingredients)
class CustomIngredientsAdmin(admin.ModelAdmin):
    """Ингредиенты."""
    list_display = 'name', 'measurement_unit'
    list_filter = ('name',)


@admin.register(Tag)
class CustomTagAdmin(admin.ModelAdmin):
    """Теги."""
    list_display = 'name', 'color', 'slug'
    list_filter = 'name', 'color'
