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


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепт."""
    inlines = [RecipeIngredientsInline]
    readonly_fields = ('recipes_added_to_favorite_count',)
    list_display = (
        'name', 'author', 'recipes_added_to_favorite_count', 'pub_date')
    list_filter = 'author', 'name', 'tags'
    search_fields = ('name', 'author',)
    autocomplete_fields = ('author',)
    filter_horizontal = ('tags',)

    def recipes_added_to_favorite_count(self, obj):
        """Подсчет кол-ва добавлений рецепта в избранное."""
        return obj.faved_recipies

    recipes_added_to_favorite_count.short_description = (
        'Количество добавлений в избранное')

    def get_queryset(self, request):
        """
        Попытка оптимизации запроса в БД.
        Кол-во запросов: 7 * на кол-во рецептов.
        """
        queryset = Recipe.objects.annotate(
            faved_recipies=Count('recipes_added_to_favorite')
        )
        return queryset


@admin.register(User)
class UserAdmin(UserAdmin):
    """Пользователь."""
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'date_joined', 'last_login')

    list_filter = ('email', 'username')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    """Ингредиенты."""
    list_display = 'name', 'measurement_unit'
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги."""
    list_display = 'name', 'color', 'slug'
    list_filter = 'name', 'color'
    search_fields = ('name__icontains',)
