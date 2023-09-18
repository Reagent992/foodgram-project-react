# Foodgram, Дипломный проект [Яндекс Практикум](https://practicum.yandex.ru/backend-developer/).

![GitHub Actions](https://github.com/Reagent992/foodgram-project-react/actions/workflows/main.yml/badge.svg)\
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

## Адрес проекта:

* [foodrecipes.webhop.me](https://foodrecipes.webhop.me/)

### Проект представляет собой платформу для публикации кулинарных рецептов.

![main_page.png](docs/pictures/main_page.png)

##### На платформе реализованно:

* Авторизация пользователей.
* Пубилкация рецепта с картинкой, тегом, выбором ингредиентов, временем приготовления, названием и описанием.
* Редактирование рецепта.
* Просмотр общей ленты рецептов.
* Подписка на пользователя.
* Добавление рецепта в избранное.
* Создание списка покупок с возможностью загрузки списка необходимых ингредиентов.

## Запуск проекта через [docker](https://www.docker.com/):

### Заполнение .env файла
```text
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
SECRET_KEY='django-insecure-cg6*sdaf3#4!rasdfsdf3w8mo!4y-q*uq3fasdf3f3fd9$'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, localhost
USE_POSTGRESQL=False
```

Файлы

* `docker-compose.yml` - для сборки проекта локально.
* `docker-compose-production.yml` - для запуска проекта на сервере.

### Команды для запуска:

##### Для файла `docker-compose.yml`

```commandline
docker compose up
```

##### Для файла`docker-compose-production.yml`.

```commandline
docker compose -f docker-compose-production.yml up
```

##### Выполнение миграций

```commandline
docker compose exec backend python manage.py migrate
```

##### Для собра статики бэкенда.

```commandline
docker compose exec backend python manage.py collectstatic
```

##### Для копирования статики.

```commandline
docker compose exec backend cp -r /app/collected_static/. /static/static_backend/
```

### Managment-команда для добавления тегов, ингредиентов и единиц измерения в БД.

```commandline
python manage.py data_import
```

## ReDoc файл с OpenAPI specification будет доступен по адресу 
[http://localhost/api/docs/](http://localhost/api/docs/)

## Локальный запуск проекта для разработки backend:

* С помощью [docker](https://www.docker.com/) запустить frontend и Nginx через файл `docker-compose.yml` из папки infra

```commandline
docker compose up
```

* Запустить backend сервер(manage.py находится в backend/foodgram)

```commandline
 python manage.py runserver
```

### Автор backend:

* [Miron Sadykov](https://github.com/Reagent992)