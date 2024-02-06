# Описание приложения

Пример реализации регистрации и авторизации пользователя с использованием почты или номера телефона в качестве юзернейма. Авторизация реализована с использованием JWT-токенов.

Использованые фреймвоки и библиотеки Django, Django Rest Framework, Djoser, Simple JWT.

Зависимости находятся в файле `requirements.txt`, а так же в файле `pyproject.toml` и `poetry.lock`.

Все данные, утечка которых нежелательна, должны храниться в файле `.env`, пример которого находится в репозитории.

# Запуск приложения

## Docker

Предпочитаемым способом запуска является использование файла `docker-compose.yml`.

    gitclone
    docker compose up --build

Если же у вас уже есть postgresql, то вы можете использовать обычный `Dockerfile`, прописав данные, необхоодимые для подключения к базе данных, в файле `.env`.

    gitclone
    docker build . -t us_app
    docker run -d --name us_app_container us_app

Миграции применяются автоматически при первом успешном запуске контейнера. Команда для применения миграций прописана в файле `entrypoint.sh`.

Суперпоьзователь создается автоматически при первом запуске контейнера. Для этого используется команда `python manage.py admininit`, которая прописана в файле `entrypoint.sh`.

## Django development server

Так же возможен запуск с использование обычного сервера для разработки из Django. Перед этим необходимо отредактировать файл `.env` внеся в него необходимые данныу для подключения в базе данных и перенеся в директорию с файлом manage.py.

    gitclone
    python us/manage.py makemigrations
    python us/manage.py migrate
    python us/manage.py runserver

# Описание эндпоинтов

## Реистрация пользователя

`POST /api/auth/users/`

| Method | Request            | Responce                                       |
| ------ | ------------------ | ---------------------------------------------- |
| POST   | email</br>password | **HTTP_201_CREATED</br> HTTP_400_BAD_REQUEST** |
| POST   | phone</br>password | **HTTP_201_CREATED</br> HTTP_400_BAD_REQUEST** |

<details>
<summary>Примеры запросов и ответов</summary>

### Request.

    curl -i -X POST -H 'Content-Type: application/json' -d '{"email": "user@mail.com", "password": "strong_password"}' http://localhost:8000/api/auth/users/

### Responce

    HTTP/1.1 201 Created
    Date: Mon, 05 Feb 2024 14:59:39 GMT
    Server: WSGIServer/0.2 CPython/3.10.12
    Content-Type: application/json
    Vary: Accept, Cookie
    Allow: GET, POST, HEAD, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 110
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"id":2,"username":"user@mail.com","email":"user@mail.com","phone":null,"is_active":true,"is_superuser":false}

### Request

    curl -i -X POST -H 'Content-Type: application/json' -d '{"phone": "+71234567890", "password": "strong_password"}' http://localhost:8000/api/auth/users/

### Responce

    HTTP/1.1 201 Created
    Date: Tue, 06 Feb 2024 04:41:27 GMT
    Server: WSGIServer/0.2 CPython/3.12.1
    Content-Type: application/json
    Vary: Accept, Cookie
    Allow: GET, POST, HEAD, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 108
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"id":3,"username":"+71234567890","email":null,"phone":"+71234567890","is_active":true,"is_superuser":false}

</details>

## Получение JWT токенов

`POST /api/auth/jwt/create/`

| Method | Request               | Responce                                   |
| ------ | --------------------- | ------------------------------------------ |
| POST   | username</br>password | **HTTP_200_OK</br> HTTP_401_UNAUTHORIZED** |

<details>
<summary>Примеры запросов и ответов</summary>

### Request

    curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "user@mail.com", "password": "strong_password"}' http://localhost:8000/api/auth/jwt/create/

### Responce

    HTTP/1.1 200 OK
    Date: Tue, 06 Feb 2024 05:07:26 GMT
    Server: WSGIServer/0.2 CPython/3.12.1
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 483
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"refresh":"<refresh_token>","access":"<access_token>"}

### Request

    curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "+71234567890", "password": "strong_password"}' http://localhost:8000/api/auth/jwt/create/

### Responce

    HTTP/1.1 200 OK
    Date: Tue, 06 Feb 2024 05:08:42 GMT
    Server: WSGIServer/0.2 CPython/3.12.1
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 483
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"refresh":"<refresh_token>","access":"<access_token>"}

</details>

## Обновление access токена

`POST /api/auth/jwt/refresh/`

| Method | Request       | Responce status code                       |
| ------ | ------------- | ------------------------------------------ |
| POST   | refresh_token | **HTTP_200_OK</br> HTTP_401_UNAUTHORIZED** |

<details>
<summary>Примеры запросов и ответов</summary>

### Request

    curl -i -X POST -H 'Content-Type: application/json' -d '{"refresh": "<refresh_token>"}' http://localhost:8000/api/auth/jwt/refresh/

### Responce

    HTTP/1.1 200 OK
    Date: Tue, 06 Feb 2024 05:19:24 GMT
    Server: WSGIServer/0.2 CPython/3.12.1
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 241
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {"access":"<access_token>"}

</details>

## обнуление? refresh токена

`POST /api/auth/logout/`

| Method | Request       | Responce        |
| ------ | ------------- | --------------- |
| POST   | refresh_token | **HTTP_200_OK** |

<details>
<summary>Примеры запросов и ответов</summary>

### Request

    curl -i -X POST -H 'Content-Type: application/json' -d '{"refresh": "<refresh_token>"}' http://localhost:8000/api/auth/logout/

### Responce

    HTTP/1.1 200 OK
    Date: Tue, 06 Feb 2024 05:21:50 GMT
    Server: WSGIServer/0.2 CPython/3.12.1
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 2
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin
    Cross-Origin-Opener-Policy: same-origin

    {}

</details>
