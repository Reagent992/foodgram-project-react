from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Теги."""
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    SUPPER = 'supper'
    CHOICES = (
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (SUPPER, 'Ужин'),
    )
    name = models.CharField(max_length=50, choices=CHOICES, null=False)
    color = models.CharField(max_length=16, null=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ингредиенты."""
    name = models.CharField(max_length=200)
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
    tag = models.ManyToManyField(
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
            MinValueValidator(1, 'Время не может быть меньше 1')
        ]
    )
    text = models.TextField(blank=False)

    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipe',
        verbose_name='Ингредиент',
        blank=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Подписка на пользователя"""
    # User - Подписывается.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        blank=False,
    )
    # Author - тот на кого подписываются.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        blank=False,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='uq_user_author'
            )
        ]
