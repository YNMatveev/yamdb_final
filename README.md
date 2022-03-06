# API_YaMDb

![Yamdb Workflow Status](https://github.com/ynmatveev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

### Описание


API_YaMDb – это REST API сервис, который собирает отзывы (Review) пользователей на произведения (Title) из предустановленных категорий (при необходимости список категорий (Category) может быть расширен).
Произведению может быть присвоен жанр (Genre) из списка предустановленных (новые жанры может создавать только администратор).
Пользователи могут оставить текстовые отзывы (Review) и выставлять произведению рейтинг (оценку в диапазоне от одного до десяти). На основании этих рейтингов высчитывается средняя оценка произведения.
Другие пользователи могут добавлять комментарии (Comments) к отзывам.
Кроме того, пользователям можно назначать роли (Role).

### Технологии
- python 3.8.7
- django 3.0.5
- django rest framework 3.11.0
- simplejwt 4.6.0
- PostgreSQL 12.4
- nginx 1.19.3
- docker

### Демо приложения

 Приложение развернуто по адресу: http://yamdb.ynm-project.online/api/v1/ и можно проверить его функциональность.

 Детальное описание эндпоинтов и разрешенных методов доступно по адресу: http://yamdb.ynm-project.online/redoc/

 Для GET запросов аутенфикация не нужна, и можно получить данные по следующим эндпоинтам:

 - http://yamdb.ynm-project.online/api/v1/titles/1/reviews/
 - http://yamdb.ynm-project.online/api/v1/categories/
 - http://yamdb.ynm-project.online/api/v1/genres/
 - http://yamdb.ynm-project.online/api/v1/titles/

Для методов POST, PATCH, DELETE необходимо получение JWT-токена. Для этого нужно отправить
POST запрос на адрес http://yamdb.ynm-project.online/api/v1/auth/email/ с указание email в теле запроса.

```json
{
    "email" : "my@email.com"
}
```

На указанный email придет сообщение с кодом подтверждения.
Для получения JWT-токена нужно отправить POST запрос с кодом подтверждения и email в теле на адрес http://yamdb.ynm-project.online/api/v1/auth/token/

```json
{
    "email": "my@email.com",
    "confirmation_code": "your confirmation code"
}
```

В ответе в ключе "token" придет сгенерированный JWT-токен.


### Переменные окружения

Часть настроек для проекта должны быть переданы как переменные окружения. Для этого создайте в корне проекта файл .env
В нем должны быть определены следующие переменные:
```txt
# Настройки проекта
DJANGO_SECRET_KEY
DJANGO_ALLOWED_HOSTS

# Настройки базы данных
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT

# Настройки для почтового сервера
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

### Запуск приложения

Для запуска приложения вам потребуется установить git ([Установка git](https://git-scm.com/book/ru/v2/Введение-Установка-Git))  и docker ([Установка docker](https://www.docker.com/get-started)) на ваш компьютер.


Склонируйте приложение из репозитория на GitHUB. Для этого в терминале перейдите в директорию, в которую хотите скопировать приложение и выполните команду:

```bash
$ git clone https://github.com/YNMatveev/infra_sp2.git
```

Из корневой директории проекта (там где находится файл **manage.py**) и
выполните в терминале команду:

```bash
$ sudo docker-compose up -d
```

Докер соберет необходимые образы и запустит контейнеры в фоновом режиме.

### Подготовка базы данных

Для подготовки базы данных в терминале выполните команды:
```bash
$ sudo docker-compose exec web python manage.py makemigrations --noinput
$ sudo docker-compose exec web python manage.py migrate --noinput
```

### Создание суперпользователя и доступ к админке
Для создания суперпользователя в терминале выполните команду (заменив username, you_password и admin@email.fake на нужные):

```bash
$ sudo docker-compose exec web bash -c \
"DJANGO_SUPERUSER_USERNAME=your_username \
DJANGO_SUPERUSER_PASSWORD=your_password \
DJANGO_SUPERUSER_EMAIL=admin@email.fake \
python manage.py createsuperuser --noinput"
```
или с вводом нужных вам данных в терминале

```bash
$ sudo docker-compose exec web python manage.py createsuperuser
```

Чтобы удобнее было работать через админку необходимо собрать статику проекта. Для этого выполните команду:

```bash
$ sudo docker-compose exec web python manage.py collectstatic --noinput
```


Теперь можно зайти в админку по адресу:
[http://localhost/admin/](http://localhost/admin/) или [http://127.0.0.1/admin/](http://127.0.0.1/admin/)

### Заполнение БД начальными данными
Для проекта подготовлены тестовые данные (_3 категории_, _5 комментариев_,_15 жанров_,_75 ревью_,_32 тайтла_,_5 пользователей_).

Для того чтобы добавить эти данные в базу данных в терминале выполните команду:

```bash
$ sudo docker-compose exec web python manage.py loaddata fixtures.json
```

Дополнительных манипуляций с базой данных делать не нужно. При формировании fixtures.json были исключены следующие таблицы:
- contenttypes
- auth.permission
- admin.logentry
- sessions.session

### Документация по проекту
После развертывания проекта документация будет доступна по адресу:
[http://localhost/redoc/](http://localhost/redoc/) или [http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)

В документации можно найти описание эндпоинтов, права доступа к ним и разрешенные методы.

### Над проектом работали:

* vbuoc ([профиль на github](https://github.com/vbuoc)) – категории (Categories), жанры (Genres) и произведения (Titles): эндпоинты, модели, view.

* enjef ([профиль на github](https://github.com/Enjef)) - отзывы (Review), комментарии (Comments): эндпоинты, модели, view. Права доступа к ресурсам и рейтинг произведений.

* ynmatveev - система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail.
