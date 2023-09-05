import re

from django.core.exceptions import ValidationError


def email_validator(email):
    """Проверка email на соотетсвие требованиям."""
    pattern = r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
    max_length = 150
    match = re.match(pattern, email, re.IGNORECASE)
    if match is None or len(email) > max_length:
        raise ValidationError(
            "Используйте корректный адрес электронной почты. Адрес должен "
            "быть не длиннее 150 символов."
            "Допускается использование латинских букв, цифр и символов "
            "@  .  +  -"
        )
