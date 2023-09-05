from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import email_validator


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[email_validator],
        verbose_name="Электронная почта",
        blank=False)
    username = models.CharField(
        max_length=150,
        blank=False,
        verbose_name="Имя пользователя",
        unique=True)
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
        blank=False)
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
        blank=False)

    class Meta:
        ordering = ['id']
        db_table = 'auth_user'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Подписка на пользователя"""
    # subscriber - Подписывается.
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
    )
    # target_user  - тот на кого подписываются.
    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписан на'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания подписки'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'target_user'],
                name='uq_subscriber_target_user'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.target_user}'
