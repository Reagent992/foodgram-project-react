from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from recipes.models import (FavoriteRecipe, Ingredients, Recipe,
                            RecipeIngredients, ShoppingCart, Tag)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Избранное."""

    list_display = ('user', 'recipe', 'added_at')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Избранное."""

    list_display = ('user', 'recipe', 'added_at')
    search_fields = ('user', 'recipe')


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1
    min_num = 1
    autocomplete_fields = ('ingredient',)
    verbose_name = 'Список ингредиентов'
    verbose_name_plural = 'Список ингредиентов'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепт."""

    inlines = [RecipeIngredientsInline]
    readonly_fields = ('recipes_added_to_favorite_count',)
    list_display = (
        'name', 'author_link', 'ingredients_list',
        'recipes_added_to_favorite_count', 'pub_date', 'image_tumbnail')
    list_filter = 'author', 'name', 'tags'
    search_fields = ('name', 'author__username',)
    autocomplete_fields = ('author',)
    filter_horizontal = ('tags',)

    @admin.display(description='Картинка')
    def image_tumbnail(self, recipe):
        return mark_safe(f'<img src={recipe.image.url} width="80" height="60">')

    @admin.display(description='Автор')
    def author_link(self, recipe):
        """Поле автора - ссылка на пользователя."""

        link = reverse(
            'admin:users_user_change', args=[recipe.author.id]
        )
        return format_html('<a href="{}">{}</a>', link, recipe.author)

    @admin.display(description='В избранном')
    def recipes_added_to_favorite_count(self, recipe):
        """Подсчет кол-ва добавлений рецепта в избранное."""

        return recipe.favoriterecipe.count()

    @admin.display(description='Список ингредиентов')
    def ingredients_list(self, recipe):
        """Список ингредиентов рецепта."""

        return [ingredient.name for ingredient in recipe.ingredients.all()]

    def get_queryset(self, request):
        """
        Оптимизация запроса в БД.
        """

        return Recipe.objects.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )


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
    search_fields = ('name',)
