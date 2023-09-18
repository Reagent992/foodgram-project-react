from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def validate_username_me_restricted(username):
    """Никнейм me - запрещен."""
    if username.lower() == 'me':
        raise ValidationError(
            {'error': 'Имя пользователя не может быть "me".'})


username_validator = UnicodeUsernameValidator()
