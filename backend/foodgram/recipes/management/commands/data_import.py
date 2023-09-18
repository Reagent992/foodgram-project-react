import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredients, Tag

DATA = {
    'tags': {
        'model': Tag,
        'file_path': os.path.join(
            settings.BASE_DIR, 'data/tags.json'),
    },
    'ingredients': {
        'model': Ingredients,
        'file_path': os.path.join(
            settings.BASE_DIR, 'data/ingredients.json')
    }
}


def read(file_path):
    """Получение информации из файла."""
    try:
        with open(file_path, 'r', encoding='UTF-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f'Файл не найден по пути {file_path}')

    return data


def write(array, model):
    """Запись полученной информации."""
    [model.objects.get_or_create(**item) for item in array]


class Command(BaseCommand):
    """Загрузка ингредиентов и тегов."""

    help = 'Загрузка ингредиентов и тегов.'

    def handle(self, *args, **options):
        """Запуск загрузки."""
        for item in DATA.values():
            write(array=read(item.get('file_path')),
                  model=item.get('model'))
