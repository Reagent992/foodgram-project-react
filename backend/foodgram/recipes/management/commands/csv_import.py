# # flake8: noqa
# import csv
#
# from django.core.management import BaseCommand
#
# from recipes.models import Ingredients
#
# TODO: переписать
# class Command(BaseCommand):
#     help = 'Загрузка ингредиентов и единиц измерения из CSV-файла'
#
#     def add_arguments(self, parser):
#         parser.add_argument(
#             'csv_file_path',
#             nargs='?',
#             type=str,
#             default='recipes/management/commands/ingredients.csv')
#
#     def handle(self, *args, **options):
#         csv_file_path = options['csv_file_path']
#         with open(csv_file_path, encoding='UTF-8') as csvfile:
#             """
#             Скрипт добавления ингредиентов и
#             единиц измерения в БД из CSV-файла.
#             """
#             reader = csv.reader(csvfile)
#             counter_ingredients = 0
#             counter_measurment_units = 0
#             ingredient_already_in_db = 0
#             errors_list = []
#             for row in reader:
#                 if len(row) != 2:
#                     raise ValueError(
#                         f'Неверные данные в таблице, строка: {row}')
#
#                 csv_file_ingredient = row[0]
#                 csv_file_measurment_unit = row[1]
#
#                 # Добавление единицы измерения
#                 try:
#                     measurment_unit_obj, created_measurment_unit_status = (
#                         MeasurementUnit.objects.get_or_create(
#                             name=csv_file_measurment_unit
#                         ))
#                     if created_measurment_unit_status:
#                         counter_measurment_units += 1
#                 except Exception as e:
#                     errors_list.append(f'Ошибка {e} на строке {row}')
#
#                 # Добавление ингредиента
#                 try:
#                     ingredient_obj, created_ingredient_status = (
#                         Ingredients.objects.get_or_create(
#                             name=csv_file_ingredient,
#                             measurement_unit=measurment_unit_obj
#                         ))
#                     if created_ingredient_status:
#                         counter_ingredients += 1
#                     elif not created_ingredient_status:
#                         ingredient_already_in_db += 1
#                 except Exception as e:
#                     errors_list.append(f'Ошибка {e} на строке {row}')
#
#             self.stdout.write(
#                 '-------------------------Итог:----------------------------')
#             self.stdout.write(self.style.SUCCESS(
#                 f'Введено {counter_ingredients} ингредиентов'
#             ))
#             self.stdout.write(self.style.SUCCESS(
#                 f'Введено {counter_measurment_units} единиц измерения'
#             ))
#             self.stdout.write(self.style.WARNING(
#                 f'{ingredient_already_in_db} '
#                 f'ингредиентов уже было в БД.'
#             ))
#             print()
#             if errors_list:
#                 self.stdout.write(self.style.ERROR('Ошибки:'))
#                 for e in errors_list:
#                     print(e)
