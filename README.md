# API_YaMDb

### Описание


API_YaMDb – это то REST API сервис, который собирает отзывы (Review) пользователей на произведения (Title) из предустановленных категорий (при необходимости список категорий (Category) может быть расширен).
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

### Запуск приложения

Для запуска приложения вам потребуется установить git ([Установка git](https://git-scm.com/book/ru/v2/Введение-Установка-Git))  и docker ([Установка docker](https://www.docker.com/get-started)) на ваш компьютер.


Склонируйте приложение из репозитория на GitHUB. Для этого в терминале перейдите в директорию, в которую хотите скопировать приложение и выполните команду:

```bash
$ git clone https://github.com/YNMatveev/infra_sp2.git
```

Из корневой директории проекта (там где находится файл **manage.py**) и
выполните в терминале команду:

```bash
$ docker compose up -d
```

Докер соберет необходимые образы и запустит контейнеры в фоновом режиме.

### Подготовка базы данных

Для подготовки базы данных в терминале выполните команды:
```bash
$ docker compose exec web python manage.py makemigrations --noinput
$ docker compose exec web python manage.py migrate --noinput
```

### Создание суперпользователя и доступ к админке
Для создания суперпользователя в терминале выполните команду (заменив username, you_password и admin@email.fake на нужные):

```bash
$ docker compose exec web bash -c \
"DJANGO_SUPERUSER_USERNAME=your_username \
DJANGO_SUPERUSER_PASSWORD=your_password \
DJANGO_SUPERUSER_EMAIL=admin@email.fake \
python manage.py createsuperuser --noinput"
```
или с вводом нужных вам данных в терминале

```bash
$ docker compose exec web python manage.py createsuperuser
```

Чтобы удобнее было работать через админку необходимо собрать статику проекта. Для этого выполните команду:

```bash
$ docker compose exec web python manage.py collectstatic --noinput
```


Теперь можно зайти в админку по адресу:
[http://localhost/admin/](http://localhost/admin/) или [http://127.0.0.1/admin/](http://127.0.0.1/admin/)

### Заполнение БД начальными данными
Для проекта подготовлены тестовые данные (_3 категории_, _5 комментариев_,_15 жанров_,_75 ревью_,_32 тайтла_,_5 пользователей_).

Для того чтобы добавить эти данные в базу данных в терминале выполните команду:

```bash
$ docker compose exec web python manage.py loaddata fixtures.json
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
