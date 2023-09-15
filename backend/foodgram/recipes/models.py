from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.abstract_models import AbstractModel
from users.models import User


class Tag(models.Model):
    """Теги."""

    name = models.CharField(
        'Тег',
        max_length=settings.LENGTH_200,
        unique=True
    )
    color = ColorField(
        'Hex-Цвет',
        max_length=settings.LENGTH_7,
        unique=True
    )
    slug = models.SlugField(
        'Текстовый идентификатор страницы',
        max_length=settings.LENGTH_200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ингредиенты."""

    name = models.CharField(
        'Название ингредиента',
        max_length=settings.LENGTH_200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.LENGTH_200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/',
        help_text='Загрузка картинки'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Тег',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                limit_value=settings.LENGTH_1,
                message=f'Время приготовления не может быть меньше:'
                        f'{settings.LENGTH_1}'),
            MaxValueValidator(
                limit_value=settings.LENGTH_1440,
                message=f'Время приготовления не может быть больше:'
                        f'{settings.LENGTH_1440}')
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
        ordering = ('-pub_date',)

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
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(MinValueValidator(
            limit_value=settings.LENGTH_1,
            message=f'Количество не может быть меньше {settings.LENGTH_1}.'),
            MaxValueValidator(
                limit_value=settings.LENGTH_9999,
                message=f'Количество не может быть больше:'
                        f'{settings.LENGTH_9999}.'
        )
        ),
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='uq_ingredient_recipe',
            ),
        )

    def __str__(self):
        return (f'Ингредиент "{self.ingredient.name}"'
                f' в количестве {self.amount}')


class FavoriteRecipe(AbstractModel):
    """Любимые рецепты."""

    class Meta(AbstractModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        default_related_name = 'favoriterecipe'

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class ShoppingCart(AbstractModel):
    """Список покупок."""

    class Meta(AbstractModel.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        default_related_name = 'shoppingcart'

    def __str__(self):
        return f'{self.user} добавил в корзину {self.recipe}'
