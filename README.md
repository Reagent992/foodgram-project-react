# praktikum_new_diplom

## Запуск добавление ингредиентов и единиц измерения в БД.

##### Скрипт находится в

`recipes/management/commands/csv_import.py`

##### Запуск:

```commandline
python manage.py csv_import
```

###### Передача CSV-файла:

```commandline
python manage.py csv_import /path_to_file/file.csv
```

Ожидаемая форма csv файла:

```text
абрикосовое варенье,г
абрикосовое пюре,г
абрикосовый джем,г
```