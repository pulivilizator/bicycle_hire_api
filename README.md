# Проект API аренды велосипедов

В проекте была реализована авторизация по JWT токену, и соответствующие ручки для регистрации, входа, выхода, замены устаревшего токена и сброса пароля.
Так же, все необходимые конечные точки для получения списка велосипедов, для аренды, возврата, условной оплаты и получения истории аренд.

Для аренды, возврата, оплаты велосипеда необходима авторизация, либо отправка access токена в хэдере.

С помощью Celery реализована отправка писем на email при сбросе пароля и при завершении поездки.

В качестве CI CD системы был выбран gitlab.

В качестве облачного хранилища данных было выбрано Яндекс Облако.

С документацией, примерами запросов и ответов можно ознакомиться на сайте проекта: https://chervanev.ru/

Для теста API можно на сайте пройти полный цикл аренды: 
- Зарегистрироваться
- Залогиниться
- Получить список доступных велосипедов
- Арендовать один из них (Для этого и дальнейших действий необходима авторизация на самом сайте при помощи access токена полученого при входе в аккаунт, либо отправка access token в headers)
- Вернуть велосипед
- Оплатить
- Выйти из аккаунта

---

### Запуск проекта

#### В самом простом случае, для локального запуска будет достаточно:
- установить зависимости (`poetry install` либо `pip install -r requirements.txt`)
- заполнить .env.example файл своими данными
- переименовать .evn.example в .env
- в docker compose удалить сервисы nginx и certbot 
- в сервисе app раскомментировать env_file
- поднять docker compose


#### Для поднятия на сервере необходимо будет:
- указать свой демен в файле настроек nginx и добавить его в переменную окружения ALLOWED_HOSTS
- указать свои переменные окружения в переменных проекта на сервисе(в моем случае gitlab)(названия переменных окружения соответствуют их названиям в .env.example)
- создать сертификаты и настроить пути к ним в сервисах docker compose