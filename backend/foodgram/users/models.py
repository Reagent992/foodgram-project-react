from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import (username_validator,
                              validate_username_me_restricted)


class User(AbstractUser):
    """Пользователи."""

    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH_254,
        unique=True,
        verbose_name='Электронная почта')
    username = models.CharField(
        max_length=settings.LENGTH_150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=(validate_username_me_restricted, username_validator)
    )
    first_name = models.CharField(
        max_length=settings.LENGTH_150,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=settings.LENGTH_150,
        verbose_name='Фамилия')
    subscription = models.ManyToManyField(
        to='self',
        through='Subscription',
        related_name="following",
        symmetrical=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Подписки."""

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания подписки'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'author'),
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(subscriber=models.F("author")),
            ),
        )

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
