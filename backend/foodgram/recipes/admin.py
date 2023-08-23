from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

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


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline]
    readonly_fields = ('recipes_added_to_favorite_count',)
    list_display = (
        'name', 'author', 'recipes_added_to_favorite_count', 'pub_date')
    list_filter = 'author', 'name', 'tags'

    def recipes_added_to_favorite_count(self, obj):
        return obj.recipes_added_to_favorite.count()

    recipes_added_to_favorite_count.short_description = (
        'Количество добавлений в избранное')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'date_joined', 'last_login')

    list_filter = ('email', 'username')


@admin.register(Ingredients)
class CustomIngredientsAdmin(admin.ModelAdmin):
    list_display = 'name', 'measurement_unit'
    list_filter = ('name',)


@admin.register(Tag)
class CustomTagAdmin(admin.ModelAdmin):
    list_display = 'name', 'color', 'slug'
    list_filter = 'name', 'color'
