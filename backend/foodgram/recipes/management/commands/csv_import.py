import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredients, Tag


def read(file_path):
    """Получение информации из файла."""

    try:
        with open(file_path, encoding='UTF-8') as csvfile:
            tags = list()
            for row in csv.reader(csvfile):
                tags.append(row)
    except FileNotFoundError:
        print(f"Файл не найден по пути {file_path}")

    return tags


def write_ingredients(ingredients_array):
    """Запись ингредиентов."""

    counter = 0
    for name, measurement_unit in ingredients_array:
        obj, status = Ingredients.objects.get_or_create(
            name=name,
            measurement_unit=measurement_unit
        )
        if status:
            counter += 1

    return counter


def write_tags(tags_array):
    """Запись тегов."""

    counter = 0
    for name, color, slug in tags_array:
        obj, status = Tag.objects.get_or_create(
            name=name,
            color=color,
            slug=slug
        )
        if status:
            counter += 1

    return counter


class Command(BaseCommand):
    help = 'Загрузка ингредиентов и единиц измерения из CSV-файла'

    def handle(self, *args, **options):
        ingredients_csv_file_path = os.path.join(
            settings.BASE_DIR.parent, 'data/ingredients.csv')
        tags_csv_file_path = os.path.join(
            settings.BASE_DIR.parent, 'data/tags.csv')
        ingredients_array = read(ingredients_csv_file_path)
        tags_array = read(tags_csv_file_path)
        ingredients_write_result = write_ingredients(ingredients_array)
        tags_write_result = write_tags(tags_array)
        print('---------------------------Итог-------------------------------')
        print(f'Введено {ingredients_write_result} ингредиентов')
        print(f'Введено {tags_write_result} тегов')
