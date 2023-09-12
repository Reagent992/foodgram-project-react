from django.db import models

from users.models import User


class AbstractModel(models.Model):
    """Абстрактная модель, для полей пользователя, рецепта и даты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
