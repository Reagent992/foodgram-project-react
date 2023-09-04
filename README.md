# Foodgram, Дипломный проект [Яндекс Практикум](https://practicum.yandex.ru/backend-developer/).

## Проект представляет собой платформу для публикации кулинарных рецептов.

![main_page.png](docs/pictures/main_page.png)
На платформе реализованно:

* Пубилкация рецепта с картинкой, тегом, выбором ингредиентов, временем приготовления, названием и описанием.
* Редактирование рецепта.
* Просмотр общей ленты рецептов.
* Подписка на пользователя.
* Добавление рецепта в избранное.
* Создание списка покупок с возможностью загрузки списка необходимых ингредиентов.

## Локальный запуск проекта:

* С помощью [docker](https://www.docker.com/) запустить frontend и Nginx через файл `docker-compose.yml` из папки infra

```commandline
docker compose up
```

* Запустить backend сервер
  manage.py находится в backend/foodgram

```commandline
 python manage.py runserver
```

### managment-команды:

### 1. Добавление ингредиентов и единиц измерения в БД.

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

### 2. Создание группы с правами "admin".

##### Запуск:

```commandline
python manage.py create_admin_group
```