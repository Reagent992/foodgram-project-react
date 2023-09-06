from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Теги."""
    name = models.CharField(max_length=200, null=False, verbose_name='Тег')
    color = ColorField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    """Единицы измерения."""
    name = models.CharField(max_length=200, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ингредиенты."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Единица измерения',
        related_name='ingredients',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        blank=False,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название рецепта')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/',
        blank=True,
        null=True,
        default=None,
        help_text='Загрузите картинку'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Тег',
        blank=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время приготовления не может быть меньше 1'),
            MaxValueValidator(
                limit_value=1440,
                message='Время приготовления не может быть больше 1440')
        ]
    )
    text = models.TextField(blank=False, verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        to=Ingredients,
        through='RecipeIngredients',
        verbose_name='ингредиент',
        related_name='recipe'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Ингредиенты рецептов."""
    ingredient = models.ForeignKey(
        to=Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipeingredients'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='recipeingredients'
    )
    amount = models.PositiveIntegerField(
        validators=(MinValueValidator(
            limit_value=1,
            message='Количество не может быть меньше 1.'),
            MaxValueValidator(
            limit_value=9999,
            message='Количество не может быть больше 9999'
        )
        ),
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='uq_ingredient_recipe',
            )
        ]

    def __str__(self):
        return (f'Ингредиент "{self.ingredient.name}"'
                f' в количестве {self.amount}')


class FavoriteRecipe(models.Model):
    """Любимые рецепты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Добавляет в избранное',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_added_to_favorite',
        verbose_name='Рецепт',
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_at']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uq_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class ShoppingCart(models.Model):
    """Список покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Добавляет в корзину',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_added_to_cart',
        verbose_name='Рецепт',
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_at']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.user} добавил в корзину {self.recipe}'
